import uvicorn
import asyncio
import os
import time
import datetime as dt

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from typing import Optional, Union, Any, AsyncGenerator

from src.crawlers.reddit_crawler import RedditCrawler
from src.items.RequestSchema import ScrapeRequest
from src.items.ResponseSchema import ScrapeResponse
from src.items import Post


HOST: str = os.getenv("HOST", "0.0.0.0")
PORT: int = int(os.getenv("PORT", "9091"))

MAX_CONCURRENT_SCRAPES: int = int(os.getenv("MAX_CONCURRENT_SCRAPES", "2"))
DEFAULT_TIMEOUT_SECONDS: int = int(os.getenv("DEFAULT_TIMEOUT_SECONDS", "120"))
MAX_TIMEOUT_SECONDS: int = int(os.getenv("MAX_TIMEOUT_SECONDS", "600"))
WEBSOCKET_RECEIVE_TIMEOUT_SECONDS: int = int(os.getenv("WEBSOCKET_RECEIVE_TIMEOUT_SECONDS", "30"))
WEBSOCKET_IDLE_TIMEOUT_SECONDS: int = int(os.getenv("WEBSOCKET_IDLE_TIMEOUT_SECONDS", "120"))

scrape_gate = asyncio.Semaphore(MAX_CONCURRENT_SCRAPES)

app = FastAPI(
    title="reddit scraper",
    version="2.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)


def _normalize_stop_date(value: Optional[Union[dt.datetime, dt.date]]) -> Optional[dt.datetime]:
    """ normalize stop date to an utc datetime """
    if value is None: return None

    if isinstance(value, dt.datetime):
        if value.tzinfo is None:
            return value.replace(tzinfo=dt.timezone.utc)
        return value.astimezone(dt.timezone.utc)

    return dt.datetime.combine(
        value,
        dt.time.min,
        tzinfo=dt.timezone.utc,
    )


def _normalize_timeout(timeout_seconds: Optional[int]) -> int:
    """ normalize and validate a scrape timeout """
    timeout: int = timeout_seconds or DEFAULT_TIMEOUT_SECONDS

    if timeout < 1:
        raise HTTPException(
            status_code=422,
            detail="timeout_seconds must be greater than zero",
        )

    if timeout > MAX_TIMEOUT_SECONDS:
        raise HTTPException(
            status_code=422,
            detail=f"timeout_seconds cannot exceed {MAX_TIMEOUT_SECONDS}",
        )

    return timeout


async def _crawl_request(req: ScrapeRequest) -> AsyncGenerator[Post, None]:
    """ crawl all requested reddit links with the configured concurrency gate """
    timeout_seconds: int = _normalize_timeout(req.timeout_seconds)
    stop_date: dt.datetime | None = _normalize_stop_date(req.stop_date)

    async with scrape_gate:
        crawler = RedditCrawler(
            cookies=req.cookies,
            cookie_accounts=req.cookie_accounts,
            proxy=req.proxy,
            timeout_seconds=timeout_seconds,
            deep_crawl=req.deep_crawl,
            include_comments=req.include_comments,
            include_removed_comments=req.include_removed_comments,
            include_crossposts=req.include_crossposts,
            include_removed_posts=req.include_removed_posts,
        )

        deadline: float = time.monotonic() + timeout_seconds

        for url in req.links:
            if time.monotonic() >= deadline:
                raise TimeoutError("scrape operation timed out")

            remaining: float = deadline - time.monotonic()
            if remaining <= 0:
                raise TimeoutError("scrape operation timed out")

            generator = crawler.crawl(
                reddit_url=url,
                max_amount=req.limit,
                stop_date=stop_date,
            )

            while True:
                remaining: float = deadline - time.monotonic()

                if remaining <= 0:
                    raise TimeoutError("scrape operation timed out")

                try:
                    post: Post = await asyncio.wait_for(
                        generator.__anext__(),
                        timeout=remaining,
                    )
                except StopAsyncIteration:
                    break

                yield post


async def _collect(
    generator: AsyncGenerator[Post, None],
) -> list[Post]:
    """ collect posts from an async generator """
    return [post async for post in generator]


async def _send_error(
    websocket: WebSocket,
    status_code: int,
    detail: str,
) -> None:
    """ send a normalized websocket error response """
    await websocket.send_json(
        {
            "type": "error",
            "status_code": status_code,
            "detail": detail,
        }
    )


async def _stream(
    websocket: WebSocket,
    generator: AsyncGenerator[Post, None],
) -> int:
    """ stream scraped posts to a websocket client """
    count: int = 0

    async for post in generator:
        await websocket.send_json({
            "type": "item",
            "data": post.model_dump(mode="json"),
        })
        count += 1

    await websocket.send_json({
        "type": "done",
        "count": count,
    })

    return count


@app.get("/health")
async def health() -> dict[str, Any]:
    """ return the liveness state of the service """
    return {
        "status": "healthy",
        "service": "reddit-scraper",
        "version": app.version,
    }


@app.get("/ready")
async def ready() -> dict[str, Any]:
    """ return whether the service is ready to accept requests """
    return {
        "status": "ready",
        "host": HOST,
        "port": PORT,
        "available_slots": scrape_gate._value,
        "max_concurrent_scrapes": MAX_CONCURRENT_SCRAPES,
        "default_timeout_seconds": DEFAULT_TIMEOUT_SECONDS,
        "max_timeout_seconds": MAX_TIMEOUT_SECONDS,
    }


@app.post("/v1/scrape", response_model=ScrapeResponse)
async def scrape(req: ScrapeRequest) -> ScrapeResponse:
    """ scrape reddit posts from the requested links """
    started: float = time.perf_counter()

    try: posts: list[Post] = await _collect(_crawl_request(req))
    except TimeoutError as exc:
        raise HTTPException(
            status_code=504,
            detail=str(exc),
        ) from exc
    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=str(exc),
        ) from exc

    elapsed_ms: int = int((time.perf_counter() - started) * 1000)

    return ScrapeResponse(
        links=req.links,
        limit=req.limit,
        count=len(posts),
        elapsed_ms=elapsed_ms,
        posts=posts,
    )


@app.websocket("/v1/ws/scrape")
async def websocket_scrape(websocket: WebSocket) -> None:
    """ stream reddit posts over websocket """
    await websocket.accept()

    try:
        payload: dict[str, Any] = await asyncio.wait_for(
            websocket.receive_json(),
            timeout=WEBSOCKET_RECEIVE_TIMEOUT_SECONDS,
        )

        req: ScrapeRequest = ScrapeRequest.model_validate(payload)

        await asyncio.wait_for(
            _stream(websocket, _crawl_request(req)),
            timeout=min(
                _normalize_timeout(req.timeout_seconds),
                WEBSOCKET_IDLE_TIMEOUT_SECONDS,
            )
            if req.timeout_seconds
            else min(
                DEFAULT_TIMEOUT_SECONDS,
                WEBSOCKET_IDLE_TIMEOUT_SECONDS,
            ),
        )

    except asyncio.TimeoutError:
        await _send_error(
            websocket,
            504,
            "websocket or scrape operation timed out",
        )
    except WebSocketDisconnect:
        return
    except ValueError as exc:
        await _send_error(
            websocket,
            422,
            str(exc),
        )
    except Exception as exc:
        await _send_error(
            websocket,
            500,
            str(exc),
        )
    finally:
        await websocket.close()


if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host=HOST,
        port=PORT,
        reload=False,
    )
