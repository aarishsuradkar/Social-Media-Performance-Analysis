# Data Source Documentation

## File Information
- **Original File Name**: `social_media_engagement_dataset.csv`
- **Location**: Provided in the workspace root: `C:\Users\SCI\Desktop\data analyst\Social Media Performance Analysis\social_media_engagement_dataset.csv`
- **Origin**: **Synthetic / Generated** dataset simulating multi-platform social media metrics.
- **Date Range**: January 1, 2024 01:42:00 to December 31, 2025 21:56:00 (730 days, 2 full calendar years).
- **Total Records**: 5,000 posts across 6 platforms (Instagram, Twitter, Facebook, TikTok, LinkedIn, YouTube).

## Repository Data Policy
In accordance with portfolio best practices and project instructions, the raw CSV file (`social_media_engagement_dataset.csv`) is excluded from git version control via `.gitignore`. All processed and aggregated data are exported to the `output/` directory and tracked version-controlled.

## Schema Definition
The dataset contains 20 columns:
1. `Post_ID` (string): Unique identifier for each post (`POST_00000` - `POST_04999`).
2. `Timestamp` (datetime string): Timestamp of post publication (`YYYY-MM-DD HH:MM:SS`).
3. `Platform` (string): Social media network (`Instagram`, `Twitter`, `Facebook`, `TikTok`, `LinkedIn`, `YouTube`).
4. `Content_Type` (string): Content format (17 unique formats: Video, Story, Poll, Post, Live, Carousel, Photo, Reel, Stitch, Retweet, Duet, Tweet, Thread, Community Post, Document, Short, Article).
5. `Category` (string): Content industry niche (12 categories: Gaming, Technology, Lifestyle, Entertainment, Fashion, Education, Food, Sports, Travel, Health, Fitness, Business).
6. `Likes` (integer): Total likes received (min: 18, max: 49,949).
7. `Comments` (integer): Total comments received (min: 1, max: 1,999).
8. `Shares` (integer): Total shares/retweets received (min: 2, max: 4,997).
9. `Views` (integer): Total video/media views (min: 527, max: 999,256).
10. `Saves` (integer): Total post bookmarks/saves (min: 5, max: 4,985).
11. `Follower_Count` (integer): Total followers of the posting account (min: 543, max: 499,815).
12. `Engagement_Rate` (float): Pre-calculated baseline engagement rate in the dataset.
13. `Hour_of_Day` (integer): Extracted publication hour (0 to 23).
14. `Day_of_Week` (string): Day of publication (`Monday` - `Sunday`).
15. `Hashtag_Count` (integer): Number of hashtags included (0 to 29).
16. `Content_Length` (integer): Caption length in characters (15 to 1,999).
17. `Sentiment` (string): Tone/sentiment tag (`Positive`, `Neutral`, `Negative`).
18. `Influencer_Tier` (string): Account scale tier (`Nano`, `Micro`, `Mid-tier`, `Macro`).
19. `Has_Media` (boolean): Flag indicating presence of media attachment.
20. `Is_Verified` (boolean): Flag indicating account verification status.
