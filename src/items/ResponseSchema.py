from pydantic import BaseModel, ConfigDict, Field

from src.items.Post import Post


class ScrapeResponse(BaseModel):
    model_config = ConfigDict(extra="forbid")

    links: list[str]
    limit: int
    count: int
    elapsed_ms: int
    posts: list[Post] = Field(default_factory=list)
