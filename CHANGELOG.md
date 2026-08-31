# Changelog

All notable changes to RedditScraper will be documented in this file.

This project follows semantic versioning where practical.

## [Unreleased]

### Added

* Initial refactor of the RedditScraper architecture
* Pydantic v2 models introduced as the canonical data representation
* Dedicated `Post` model for Reddit submissions
* Dedicated `Comment` model for comments embedded inside posts
* Dedicated `Thumbnail` model for thumbnail metadata
* Dedicated `Removal` model for moderation and removal metadata
* Dedicated `Media` model for media metadata
* Dedicated `Subreddit` model for subreddit information
* Dedicated `Publisher` model for Reddit author information
* Dedicated `Analytics` model for post, comment, engagement, sentiment, velocity, momentum, virality, and trend metrics
* Typed relationships between `Post`, `Comment`, `Publisher`, `Subreddit`, `Thumbnail`, `Media`, `Removal`, and `Analytics`
* Nested comments through `Post.comments`
* Typed media collection through `Post.media`
* Typed media URL collection through `Post.found_media`
* Optional sentiment and analytical metadata through `Post.analytics`

### API

* FastAPI introduced as the HTTP API framework
* Pydantic request validation introduced for scraping requests
* Pydantic response models introduced for scraping responses
* `POST /v1/scrape` endpoint introduced
* WebSocket scraping endpoint introduced at `/v1/ws/scrape`
* `/health` endpoint introduced
* `/ready` endpoint introduced
* WebSocket item streaming introduced
* WebSocket completion events introduced
* WebSocket error responses introduced
* Configurable API `HOST`
* Configurable API `PORT`
* Configurable scrape concurrency
* Configurable scrape timeout
* Configurable maximum scrape timeout
* Configurable WebSocket request timeout
* Configurable WebSocket idle timeout
* Request validation for Reddit URLs
* Request validation for scrape limits
* Request validation for timeout values
* Request validation for cookie configuration
* Request validation for cookie account pools
* Support for multiple Reddit links in one scrape request
* Support for optional proxy configuration
* Support for configurable comment and crosspost behavior
* Support for removed post and comment filtering options
* Support for keyword filtering configuration
* Support for field filtering configuration
* Support for stop-date based scraping

### Authentication and Scraping Architecture

* Public scraping path designed for requests without authentication cookies
* Private scraping path designed for authenticated Reddit requests
* Optional Reddit authentication cookies
* Optional multiple authenticated Reddit cookie accounts
* Account-pool architecture prepared for authenticated session rotation
* Explicit separation between public and private scraping
* Authentication no longer required for public Reddit content
* Private content designed to return an explicit authentication error when no authenticated session is available
* Rate-limit-aware account rotation architecture introduced
* Scraper configuration decoupled from global authentication state
* Per-request scraper configuration introduced

### Crawler

* New `RedditCrawler` orchestration layer introduced
* Separate public and private crawler implementations
* Async generator based post crawling
* Configurable maximum crawl size
* Configurable stop date
* Configurable deep comment crawling
* Configurable comment inclusion
* Configurable removed-comment inclusion
* Configurable crosspost inclusion
* Configurable removed-post inclusion
* Typed `Post` output from crawler operations
* Typed `Comment` output nested within posts

### Analytics

* Post age analytics
* Published-since analytics
* Title length analytics
* Title word count
* Body length analytics
* Body word count
* Unique word count
* Average word length
* Total text length
* URL counting
* Mention counting
* Hashtag counting
* Emoji counting
* Code block counting
* Capitalization ratios
* Punctuation density
* Score analytics
* Upvote analytics
* Downvote analytics
* Upvote ratio analytics
* Comment-to-score ratio
* Comment-to-upvote ratio
* Upvote-to-score ratio
* Downvote-to-score ratio
* Score-per-comment metrics
* Upvote-per-comment metrics
* Downvote-per-comment metrics
* Award-per-comment metrics
* Crosspost-per-comment metrics
* Score-per-hour metrics
* Score-per-day metrics
* Comment-per-hour metrics
* Comment-per-day metrics
* Upvote-per-hour metrics
* Upvote-per-day metrics
* Award-per-hour metrics
* Award-per-day metrics
* Crosspost-per-hour metrics
* Crosspost-per-day metrics
* Comment velocity
* Vote velocity
* Score velocity
* Engagement velocity
* Growth score
* Momentum score
* Virality score
* Engagement score
* Engagement rate
* Comment rate
* Vote rate
* Discussion score
* Controversy score
* Popularity score
* Social signal score
* Trend score
* Virality index
* Interaction index
* Audience response index
* Content quality score
* Content efficiency score
* Subscriber-normalized engagement metrics
* Comment sentiment aggregation
* Positive comment ratio
* Negative comment ratio
* Neutral comment ratio
* Top comment score
* Average comment score
* Median comment score
* Comment score standard deviation
* Maximum comment depth
* Average comment depth
* Media count
* Gallery count
* Media presence detection
* Image detection
* Video detection
* Gallery detection
* Poll detection
* External-link detection

### Sentiment Analysis

* VADER-based sentiment analysis retained for the refactor
* Post sentiment support
* Post compound sentiment score
* Positive sentiment score
* Negative sentiment score
* Neutral sentiment score
* Comment sentiment support
* Aggregated comment sentiment analytics
* Sentiment data separated from the raw Reddit model structure

### Docker

* Python 3.12 Bookworm Slim base image introduced
* `uv` used for dependency installation and execution
* Production dependency installation with locked `uv.lock`
* `tini` introduced as the container init process
* Python bytecode optimization configuration enabled
* Unbuffered Python output enabled
* Deterministic Python hash seed configuration enabled
* RedditScraper production container introduced
* Containerized FastAPI/Uvicorn application introduced
* Healthcheck added to the container
* Readiness endpoint exposed to container orchestration
* Existing `crawlers-network` external Docker network retained
* Configurable container host and port
* Configurable concurrency and timeout environment variables

### Validation and Data Quality

* Pydantic validation introduced throughout the public request/response boundary
* Reddit URL normalization and validation
* Cookie validation
* Cookie account validation
* Scrape limit validation
* Timeout validation
* Stop-date normalization
* Duplicate keyword normalization
* Duplicate filter-field normalization
* Unknown Reddit payload fields ignored by domain models to improve forward compatibility

### Removed

* Legacy generic `Item` abstraction
* Dataclass-based Reddit domain models
* Dictionary-based comments embedded in posts
* Database insertion logic from domain models
* Model mutation helpers used to merge partial dataclass instances
* Flask API architecture
* Global mutable request-specific authentication state
* Implicit fallback to globally configured Reddit cookies
* Direct coupling between `Post` and PostgreSQL
* Direct coupling between Reddit models and crawler persistence logic

### Changed

* `Post` is now a Pydantic model
* `Comment` is now a Pydantic model
* Comments are now typed objects owned by `Post`
* Media is now represented using typed models
* Subreddit metadata is now represented using a typed model
* Publisher metadata is now represented using a typed model
* Removal information is now represented using a typed model
* Thumbnail metadata is now represented using a typed model
* Analytics are now grouped into a dedicated typed model
* `upvote_ratio` changed to a floating-point representation
* Sentiment scores use floating-point representations
* `found_media` is now a deterministic list
* API input is validated before reaching the crawler
* API output is returned through typed response models
* Scraping configuration is passed explicitly to crawler instances
* Runtime configuration is moving away from global mutable state
* Scraping responsibilities are being separated from API responsibilities
* Persistence responsibilities are being separated from domain models
* Public and authenticated scraping paths are being separated
