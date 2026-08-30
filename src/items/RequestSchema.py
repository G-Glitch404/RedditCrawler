import re
import datetime as dt

from typing import Any, Optional
from urllib.parse import parse_qs, urlsplit

from pydantic import BaseModel, ConfigDict, Field, field_validator


REDDIT_HOSTS: tuple[str, ...] = (
    "reddit.com",
    "www.reddit.com",
    "old.reddit.com",
    "new.reddit.com",
)

REDDIT_PATH_RE: re.Pattern[str] = re.compile(
    r"^"
    r"(?:"
    r"/r/[A-Za-z0-9_+-]+(?:/.*)?"
    r"|/user/[A-Za-z0-9_-]+(?:/.*)?"
    r"|/u/[A-Za-z0-9_-]+(?:/.*)?"
    r"|/comments/[A-Za-z0-9]+(?:/.*)?"
    r"|/search"
    r")"
    r"$",
    re.IGNORECASE,
)


class ScrapeRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    links: list[str] = Field(min_length=1, max_length=100)
    limit: int = Field(default=100, ge=1, le=10_000)

    cookies: Optional[dict[str, str]] = None
    cookie_accounts: Optional[list[dict[str, str]]] = None

    timeout_seconds: int = Field(default=120, ge=10, le=600)
    stop_date: Optional[dt.datetime] = None

    deep_crawl: bool = False
    include_comments: bool = True
    include_removed_comments: bool = False
    include_crossposts: bool = True
    include_removed_posts: bool = False

    keywords: list[str] = Field(default_factory=list, max_length=100)
    filter_fields: list[str] = Field(default_factory=list, max_length=100)

    proxy: Optional[str] = Field(default=None, min_length=1, max_length=2048)

    @field_validator("links")
    @classmethod
    def normalize_links(cls, value: list[str]) -> list[str]:
        """ validate and normalize reddit urls """
        normalized: list[str] = []

        for url in value:
            url = url.strip()

            if not url:
                raise ValueError("url cannot be empty")

            parsed: Any = urlsplit(url)

            if parsed.scheme != "https" or parsed.hostname not in REDDIT_HOSTS:
                raise ValueError("only supported https reddit urls are allowed")

            if parsed.username or parsed.password or parsed.port:
                raise ValueError("invalid reddit url")

            path: str = parsed.path.rstrip("/") or "/"

            if path == "/search":
                query: dict[str, list[str]] = parse_qs(parsed.query)
                search_query: str = query.get("q", [""])[0].strip()

                if not search_query:
                    raise ValueError("search url must contain a non-empty q parameter")
            elif not REDDIT_PATH_RE.fullmatch(path):
                raise ValueError("unsupported reddit url")

            normalized.append(f"https://{parsed.hostname}{path}")

        return normalized

    @field_validator("keywords")
    @classmethod
    def normalize_keywords(cls, value: list[str]) -> list[str]:
        """ normalize keyword filters """
        return list(dict.fromkeys(
            keyword.strip().lower()
            for keyword in value
            if keyword and keyword.strip()
        ))

    @field_validator("filter_fields")
    @classmethod
    def normalize_filter_fields(cls, value: list[str]) -> list[str]:
        """ normalize post filter fields """
        return list(dict.fromkeys(
            field.strip()
            for field in value
            if field and field.strip()
        ))

    @field_validator("cookies")
    @classmethod
    def validate_cookies(
        cls,
        value: Optional[dict[str, str]],
    ) -> Optional[dict[str, str]]:
        """ validate reddit authentication cookies """
        if value is None:
            return None

        normalized: dict[str, str] = {
            str(key).strip().lower(): str(cookie).strip()
            for key, cookie in value.items()
            if str(key).strip() and str(cookie).strip()
        }

        if not normalized:
            return None

        if "reddit_session" not in normalized:
            raise ValueError("cookies must contain reddit_session")

        if "loid" not in normalized:
            raise ValueError("cookies must contain loid")

        return normalized

    @field_validator("cookie_accounts")
    @classmethod
    def validate_cookie_accounts(
        cls,
        value: Optional[list[dict[str, str]]],
    ) -> Optional[list[dict[str, str]]]:
        """ validate reddit authentication accounts """
        if value is None:
            return None

        if not value:
            return None

        accounts: list[dict[str, str]] = []

        for account in value:
            normalized: dict[str, str] = {
                str(key).strip().lower(): str(cookie).strip()
                for key, cookie in account.items()
                if str(key).strip() and str(cookie).strip()
            }

            if "reddit_session" not in normalized:
                raise ValueError("every cookie account must contain reddit_session")

            if "loid" not in normalized:
                raise ValueError("every cookie account must contain loid")

            accounts.append(normalized)

        return accounts
