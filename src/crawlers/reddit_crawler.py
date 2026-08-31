import datetime as dt

from typing import AsyncGenerator, Optional

from src.items.Post import Post
from src.crawlers._private_crawler import PrivateCrawler
from src.crawlers._public_crawler import PublicCrawler


class RedditCrawler:
    private_crawler: PrivateCrawler = PrivateCrawler()
    public_crawler: PublicCrawler = PublicCrawler()

    def __init__(
        self,
        cookies: Optional[dict[str, str]],
        cookie_accounts: Optional[list[dict[str, str]]],
        proxy: Optional[str],
        timeout_seconds: int,
        deep_crawl: bool,
        include_comments: bool,
        include_removed_comments: bool,
        include_crossposts: bool,
        include_removed_posts: bool,
    ) -> None:
        self.cookies: Optional[dict[str, str]] = cookies
        self.cookie_accounts: Optional[list[dict[str, str]]] = cookie_accounts
        self.proxy: Optional[str] = proxy
        self.timeout_seconds: int = timeout_seconds
        self.deep_crawl: bool = deep_crawl
        self.include_comments: bool = include_comments
        self.include_removed_comments: bool = include_removed_comments
        self.include_crossposts: bool = include_crossposts
        self.include_removed_posts: bool = include_removed_posts

    def crawl(
        self,
        reddit_url: str,
        max_amount: int = 1000,
        stop_date: Optional[dt.datetime] = None,
    ) -> AsyncGenerator[Post, None]:
        raise NotImplementedError("Not implemented yet.")
