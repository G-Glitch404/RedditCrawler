import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict


class Comment(BaseModel):
    model_config = ConfigDict(extra="ignore")

    comment_id: str
    body: str
    link: str
    published_at: dt.datetime

    author: Optional[str] = None
    author_id: Optional[str] = None
    parent_id: Optional[str] = None
    link_id: Optional[str] = None
    subreddit_id: Optional[str] = None
    subreddit: Optional[str] = None

    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None

    score: Optional[int] = None
    upvotes: Optional[int] = None
    downvotes: Optional[int] = None
    upvotes_ratio: Optional[float] = None

    type: Optional[str] = None
    unrepliable_reason: Optional[str] = None

    can_send_replies: Optional[bool] = None
    is_removed: Optional[bool] = None
    is_post_comment: Optional[bool] = None
    is_reply: Optional[bool] = None
    is_score_hidden: Optional[bool] = None
    is_over_18: Optional[bool] = None
    is_edited: Optional[bool] = None
    is_author_blocked: Optional[bool] = None
