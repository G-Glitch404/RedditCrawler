import datetime as dt
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from src.items.Comment import Comment


class Thumbnail(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None


class Removal(BaseModel):
    model_config = ConfigDict(extra="ignore")

    reason: Optional[str] = None
    mod_reason_title: Optional[str] = None
    mod_note: Optional[str] = None
    removed_by_category: Optional[str] = None
    spam: Optional[bool] = None


class Media(BaseModel):
    model_config = ConfigDict(extra="ignore")

    url: Optional[str] = None
    type: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    duration_seconds: Optional[float] = None
    thumbnail: Optional[str] = None
    preview_url: Optional[str] = None
    is_external: bool = False


class Subreddit(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = None
    name: Optional[str] = None
    display_name: Optional[str] = None
    name_prefixed: Optional[str] = None
    title: Optional[str] = None
    description: Optional[str] = None
    subscribers: Optional[int] = None
    subreddit_type: Optional[str] = None
    over18: Optional[bool] = None
    quarantined: Optional[bool] = None
    nsfw: Optional[bool] = None


class Publisher(BaseModel):
    model_config = ConfigDict(extra="ignore")

    id: Optional[str] = None
    username: Optional[str] = None
    fullname: Optional[str] = None
    account_age_days: Optional[float] = None
    post_karma: Optional[int] = None
    comment_karma: Optional[int] = None
    total_karma: Optional[int] = None
    is_premium: Optional[bool] = None
    is_verified: Optional[bool] = None
    is_mod: Optional[bool] = None
    is_gold: Optional[bool] = None
    is_suspended: Optional[bool] = None


class Analytics(BaseModel):
    model_config = ConfigDict(extra="ignore")

    published_since_hours: Optional[float] = None
    age_at_scrape_hours: Optional[float] = None

    title_length: Optional[int] = None
    title_words: Optional[int] = None
    title_caps_ratio: Optional[float] = None
    title_question_score: Optional[float] = None
    title_exclamation_score: Optional[float] = None

    body_length: Optional[int] = None
    body_words: Optional[int] = None
    body_unique_words: Optional[int] = None
    average_word_length: Optional[float] = None
    text_length: Optional[int] = None
    text_words: Optional[int] = None

    url_count: Optional[int] = None
    mention_count: Optional[int] = None
    hashtag_count: Optional[int] = None
    emoji_count: Optional[int] = None
    code_block_count: Optional[int] = None
    punctuation_density: Optional[float] = None
    body_caps_ratio: Optional[float] = None

    score: Optional[int] = None
    upvotes: Optional[int] = None
    downvotes: Optional[int] = None
    upvote_ratio: Optional[float] = None

    total_comments: Optional[int] = None
    total_awards: Optional[int] = None
    total_crossposts: Optional[int] = None
    total_subreddit_subs: Optional[int] = None
    total_reports: Optional[int] = None

    comments_to_upvotes_ratio: Optional[float] = None
    comments_to_score_ratio: Optional[float] = None
    upvotes_to_score_ratio: Optional[float] = None
    downvotes_to_score_ratio: Optional[float] = None
    score_to_subscriber_ratio: Optional[float] = None
    comments_to_subscriber_ratio: Optional[float] = None
    engagement_to_subscriber_ratio: Optional[float] = None

    score_per_comment: Optional[float] = None
    upvotes_per_comment: Optional[float] = None
    downvotes_per_comment: Optional[float] = None
    awards_per_comment: Optional[float] = None
    crossposts_per_comment: Optional[float] = None

    comments_per_hour: Optional[float] = None
    comments_per_day: Optional[float] = None
    score_per_hour: Optional[float] = None
    score_per_day: Optional[float] = None
    upvotes_per_hour: Optional[float] = None
    upvotes_per_day: Optional[float] = None
    awards_per_hour: Optional[float] = None
    awards_per_day: Optional[float] = None
    crossposts_per_hour: Optional[float] = None
    crossposts_per_day: Optional[float] = None

    comment_velocity: Optional[float] = None
    vote_velocity: Optional[float] = None
    score_velocity: Optional[float] = None
    engagement_velocity: Optional[float] = None
    growth_score: Optional[float] = None
    momentum_score: Optional[float] = None
    virality_score: Optional[float] = None
    engagement_score: Optional[float] = None
    engagement_rate: Optional[float] = None
    comment_rate: Optional[float] = None
    vote_rate: Optional[float] = None
    discussion_score: Optional[float] = None
    controversy_score: Optional[float] = None
    popularity_score: Optional[float] = None
    social_signal_score: Optional[float] = None
    trend_score: Optional[float] = None
    virality_index: Optional[float] = None
    interaction_index: Optional[float] = None
    audience_response_index: Optional[float] = None
    content_quality_score: Optional[float] = None
    content_efficiency_score: Optional[float] = None

    sentiment: Optional[str] = None
    sentiment_score: Optional[float] = None
    sentiment_positive: Optional[float] = None
    sentiment_negative: Optional[float] = None
    sentiment_neutral: Optional[float] = None
    sentiment_compound: Optional[float] = None

    comment_sentiment_score: Optional[float] = None
    comment_sentiment_positive: Optional[float] = None
    comment_sentiment_negative: Optional[float] = None
    comment_sentiment_neutral: Optional[float] = None
    comment_sentiment_compound: Optional[float] = None

    positive_comment_ratio: Optional[float] = None
    negative_comment_ratio: Optional[float] = None
    neutral_comment_ratio: Optional[float] = None

    top_comment_score: Optional[int] = None
    average_comment_score: Optional[float] = None
    median_comment_score: Optional[float] = None
    comment_score_stddev: Optional[float] = None
    comment_depth_max: Optional[int] = None
    comment_depth_average: Optional[float] = None

    media_count: int = 0
    gallery_count: int = 0
    has_media: bool = False
    has_image: bool = False
    has_video: bool = False
    has_gallery: bool = False
    has_poll: bool = False
    has_external_link: bool = False


class Post(BaseModel):
    model_config = ConfigDict(extra="ignore")

    post_id: str
    title: str
    link: str
    published_at: dt.datetime

    body: Optional[str] = None
    type: Optional[str] = None
    post_hint: Optional[str] = None
    domain: Optional[str] = None
    post_flair: Optional[str] = None
    crosspost_parent: Optional[str] = None
    crosspost_parent_list: list[str] = Field(default_factory=list)

    publisher: Optional[Publisher] = None
    subreddit: Optional[Subreddit] = None
    thumbnail: Optional[Thumbnail] = None

    score: Optional[int] = None
    upvote_ratio: Optional[float] = None
    upvotes: Optional[int] = None
    downvotes: Optional[int] = None

    total_awards: Optional[int] = None
    total_crossposts: Optional[int] = None
    total_comments: Optional[int] = None
    total_subreddit_subs: Optional[int] = None
    total_reports: Optional[int] = None

    is_hidden: Optional[bool] = None
    is_crosspost: Optional[bool] = None
    is_pinned: Optional[bool] = None
    is_author_premium: Optional[bool] = None
    is_edited: Optional[bool] = None
    can_gild: Optional[bool] = None
    is_comments_still_active: Optional[bool] = None
    is_score_hidden: Optional[bool] = None
    is_over_18: Optional[bool] = None
    is_locked: Optional[bool] = None
    is_spoiler: Optional[bool] = None
    is_gallery: Optional[bool] = None
    is_video: Optional[bool] = None
    is_image: Optional[bool] = None
    is_poll: Optional[bool] = None
    is_self: Optional[bool] = None
    is_original_content: Optional[bool] = None
    is_crosspostable: Optional[bool] = None
    is_removed: Optional[bool] = None
    is_archived: Optional[bool] = None
    is_promoted: Optional[bool] = None
    is_quarantined: Optional[bool] = None
    is_spam: Optional[bool] = None
    is_unlisted: Optional[bool] = None
    is_approved: Optional[bool] = None
    is_meta: Optional[bool] = None
    is_multi_media: Optional[bool] = None

    distinguished: Optional[str] = None
    removed: Optional[Removal] = None

    media: list[Media] = Field(default_factory=list)
    found_media: list[str] = Field(default_factory=list)
    comments: list[Comment] = Field(default_factory=list)

    analytics: Optional[Analytics] = None
