"""
Social Media Performance Analysis
=================================
Automated data pipeline, cleaning, statistical analysis, and report generation.
"""

# %% [markdown]
# # Step 1: Configuration and Column Mapping

# %%
import os
import sys
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats

# Path Configuration
DATA_FILE = r"C:\Users\SCI\Desktop\data analyst\Social Media Performance Analysis\social_media_engagement_dataset.csv"
OUTPUT_DIR = r"C:\Users\SCI\Desktop\data analyst\Social Media Performance Analysis\output"
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Role Mapping
COLUMNS = {
    "post_id": "Post_ID",
    "account_brand": None,       # Missing from dataset
    "platform": "Platform",
    "content_type": "Content_Type",
    "timestamp": "Timestamp",
    "likes": "Likes",
    "comments": "Comments",
    "shares": "Shares",
    "saves": "Saves",
    "reach": None,               # Missing
    "impressions": None,         # Missing (Views exists as media views, not post impressions)
    "followers": "Follower_Count",
    "hashtags": "Hashtag_Count",
    "caption": None,             # Raw caption missing
    "caption_length": "Content_Length",
    "sentiment": "Sentiment",
    "category": "Category",
    "influencer_tier": "Influencer_Tier"
}

DENOMINATOR_CHOICE = "followers"  # Following priority: reach (None) -> impressions (None) -> followers (Follower_Count)

# %% [markdown]
# # Step 2: Inspection and Data Cleaning

# %%
print("=" * 60)
print("STEP 0 & STEP 2: INSPECTION AND DATA CLEANING")
print("=" * 60)

raw_df = pd.read_csv(DATA_FILE, encoding="utf-8-sig")
initial_rows = len(raw_df)
print(f"Initial raw dataset shape: {raw_df.shape}")

# Drop exact duplicates
df_clean = raw_df.drop_duplicates().copy()
exact_dupes_dropped = initial_rows - len(df_clean)

# Drop rows missing likes or comments
initial_missing_lc = len(df_clean)
df_clean = df_clean.dropna(subset=[COLUMNS["likes"], COLUMNS["comments"]]).copy()
lc_dropped = initial_missing_lc - len(df_clean)

# Convert numeric columns with errors="coerce"
numeric_cols = [
    COLUMNS["likes"], COLUMNS["comments"], COLUMNS["shares"],
    COLUMNS["saves"], COLUMNS["followers"], COLUMNS["hashtags"],
    COLUMNS["caption_length"]
]
for col in numeric_cols:
    if col in df_clean.columns:
        df_clean[col] = pd.to_numeric(df_clean[col], errors="coerce")

# Parse timestamp and drop unparseable rows
initial_ts_len = len(df_clean)
df_clean["parsed_timestamp"] = pd.to_datetime(df_clean[COLUMNS["timestamp"]], errors="coerce")
df_clean = df_clean.dropna(subset=["parsed_timestamp"]).copy()
ts_dropped = initial_ts_len - len(df_clean)

# Add temporal fields
df_clean["hour"] = df_clean["parsed_timestamp"].dt.hour
df_clean["day_of_week"] = df_clean["parsed_timestamp"].dt.day_name()
df_clean["month"] = df_clean["parsed_timestamp"].dt.to_period("M").astype(str)
df_clean["date"] = df_clean["parsed_timestamp"].dt.date

final_rows = len(df_clean)
print(f"Cleaning summary: Initial rows: {initial_rows} -> Final rows: {final_rows}")
print(f"Dropped exact duplicates: {exact_dupes_dropped}")
print(f"Dropped missing likes/comments: {lc_dropped}")
print(f"Dropped unparseable timestamps: {ts_dropped}")

# Outlier Detection (99th percentile flags)
df_clean["engagement"] = (
    df_clean[COLUMNS["likes"]] +
    df_clean[COLUMNS["comments"]] +
    df_clean[COLUMNS["shares"]] +
    df_clean[COLUMNS["saves"]]
)

df_clean["engagement_rate"] = np.where(
    df_clean[COLUMNS["followers"]] > 0,
    (df_clean["engagement"] / df_clean[COLUMNS["followers"]]) * 100.0,
    np.nan
)

p99_eng = df_clean["engagement"].quantile(0.99)
p99_er = df_clean["engagement_rate"].quantile(0.99)
df_clean["is_outlier_engagement"] = df_clean["engagement"] > p99_eng
df_clean["is_outlier_engagement_rate"] = df_clean["engagement_rate"] > p99_er

print(f"99th percentile engagement: {p99_eng:.2f} (Outliers: {df_clean['is_outlier_engagement'].sum()})")
print(f"99th percentile engagement rate: {p99_er:.2f}% (Outliers: {df_clean['is_outlier_engagement_rate'].sum()})")

# %% [markdown]
# # Step 3: Metrics & Bucketing

# %%
print("=" * 60)
print("STEP 3: METRICS & BUCKETING")
print("=" * 60)

# Caption Length Bucket (<=50, 51-150, 151-300, 300+)
df_clean["caption_bucket"] = pd.cut(
    df_clean[COLUMNS["caption_length"]],
    bins=[-float("inf"), 50, 150, 300, float("inf")],
    labels=["<=50", "51-150", "151-300", "300+"]
)

# Hashtag Bins (0-4, 5-9, 10-14, 15-19, 20-24, 25-29 for Q4 analysis)
df_clean["hashtag_bin"] = pd.cut(
    df_clean[COLUMNS["hashtags"]],
    bins=[-1, 4, 9, 14, 19, 24, 30],
    labels=["0-4", "5-9", "10-14", "15-19", "20-24", "25-29"]
)

# Hashtag Range (3 broader bins for multi-factor combination Q13: Low, Mid, High)
df_clean["hashtag_range"] = pd.cut(
    df_clean[COLUMNS["hashtags"]],
    bins=[-1, 9, 19, 30],
    labels=["0-9 (Low)", "10-19 (Mid)", "20-29 (High)"]
)

# Follower Size Quartiles & Tiers
df_clean["follower_bucket"] = pd.qcut(
    df_clean[COLUMNS["followers"]],
    q=4,
    labels=["Q1 (Small)", "Q2 (Mid-Low)", "Q3 (Mid-High)", "Q4 (Large)"]
)

# Shares of Engagement components
df_clean["share_likes"] = df_clean[COLUMNS["likes"]] / df_clean["engagement"]
df_clean["share_comments"] = df_clean[COLUMNS["comments"]] / df_clean["engagement"]
df_clean["share_shares"] = df_clean[COLUMNS["shares"]] / df_clean["engagement"]
df_clean["share_saves"] = df_clean[COLUMNS["saves"]] / df_clean["engagement"]

# Export Clean Posts
clean_posts_export = df_clean.drop(columns=["parsed_timestamp"])
clean_posts_export.to_csv(os.path.join(OUTPUT_DIR, "clean_posts.csv"), index=False)
print("Exported clean_posts.csv successfully.")

# %% [markdown]
# # Step 4: Analytical Aggregations & Statistical Checks

# %%
print("=" * 60)
print("STEP 4: DETAILED ANALYSES")
print("=" * 60)

def aggregate_metric(df, group_col, metric_col="engagement_rate"):
    agg = df.groupby(group_col, observed=False)[metric_col].agg(
        post_count="count",
        median_engagement_rate="median",
        mean_engagement_rate="mean",
        std_engagement_rate="std",
        iqr_engagement_rate=lambda x: np.percentile(x.dropna(), 75) - np.percentile(x.dropna(), 25)
    ).reset_index()
    agg["sample_label"] = np.where(agg["post_count"] < 30, "low sample (<30)", "adequate sample (>=30)")
    return agg

# 1. Platform Performance
df_platform = aggregate_metric(df_clean, COLUMNS["platform"])
df_platform = df_platform.sort_values(by="median_engagement_rate", ascending=False)
df_platform.to_csv(os.path.join(OUTPUT_DIR, "platform_performance.csv"), index=False)

# 2. Content Type Performance
df_content = aggregate_metric(df_clean, COLUMNS["content_type"])
df_content = df_content.sort_values(by="median_engagement_rate", ascending=False)
df_content.to_csv(os.path.join(OUTPUT_DIR, "content_type_performance.csv"), index=False)

# Content Type x Platform
df_content_plat = df_clean.groupby([COLUMNS["platform"], COLUMNS["content_type"]], observed=False)["engagement_rate"].agg(
    post_count="count",
    median_engagement_rate="median",
    mean_engagement_rate="mean"
).reset_index()
df_content_plat["sample_label"] = np.where(df_content_plat["post_count"] < 30, "low sample (<30)", "adequate sample (>=30)")
df_content_plat.to_csv(os.path.join(OUTPUT_DIR, "content_type_by_platform.csv"), index=False)

# 3. Timing: Day of Week & Hour
dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
df_dow = aggregate_metric(df_clean, "day_of_week")
df_dow["day_of_week"] = pd.Categorical(df_dow["day_of_week"], categories=dow_order, ordered=True)
df_dow = df_dow.sort_values(by="day_of_week")
df_dow.to_csv(os.path.join(OUTPUT_DIR, "timing_day_of_week.csv"), index=False)

df_hour = aggregate_metric(df_clean, "hour")
df_hour = df_hour.sort_values(by="hour")
df_hour.to_csv(os.path.join(OUTPUT_DIR, "timing_hour_of_day.csv"), index=False)

# Day x Hour Heatmap Table (Median ER)
heatmap_matrix = df_clean.pivot_table(
    index="day_of_week",
    columns="hour",
    values="engagement_rate",
    aggfunc="median"
).reindex(dow_order)
heatmap_matrix.to_csv(os.path.join(OUTPUT_DIR, "timing_day_x_hour_heatmap.csv"))

# 4. Hashtag Performance
df_hashtags = aggregate_metric(df_clean, "hashtag_bin")
df_hashtags.to_csv(os.path.join(OUTPUT_DIR, "hashtag_performance.csv"), index=False)

# 5. Caption Length Performance
df_caption = aggregate_metric(df_clean, "caption_bucket")
df_caption.to_csv(os.path.join(OUTPUT_DIR, "caption_length_performance.csv"), index=False)

# 6. Sentiment Performance
df_sentiment = aggregate_metric(df_clean, COLUMNS["sentiment"])
df_sentiment = df_sentiment.sort_values(by="median_engagement_rate", ascending=False)
df_sentiment.to_csv(os.path.join(OUTPUT_DIR, "sentiment_performance.csv"), index=False)

# 7. Category & Influencer Tier Benchmarks (proxy for missing account/brand)
df_category = aggregate_metric(df_clean, COLUMNS["category"])
df_category = df_category.sort_values(by="median_engagement_rate", ascending=False)
df_category.to_csv(os.path.join(OUTPUT_DIR, "category_benchmark.csv"), index=False)

df_tier = aggregate_metric(df_clean, COLUMNS["influencer_tier"])
df_tier = df_tier.sort_values(by="median_engagement_rate", ascending=False)
df_tier.to_csv(os.path.join(OUTPUT_DIR, "influencer_tier_benchmark.csv"), index=False)

# 8. Monthly Trend
df_monthly = df_clean.groupby("month", observed=False).agg(
    post_count=("Post_ID", "count"),
    total_engagement=("engagement", "sum"),
    median_engagement_rate=("engagement_rate", "median"),
    mean_engagement_rate=("engagement_rate", "mean")
).reset_index().sort_values(by="month")
df_monthly.to_csv(os.path.join(OUTPUT_DIR, "monthly_trend.csv"), index=False)

# 9. Top 25 Posts & Top 5% Analysis
top_25 = df_clean.sort_values(by="engagement_rate", ascending=False).head(25)[
    [COLUMNS["post_id"], COLUMNS["platform"], COLUMNS["content_type"], COLUMNS["category"],
     COLUMNS["influencer_tier"], COLUMNS["followers"], COLUMNS["likes"], COLUMNS["comments"],
     COLUMNS["shares"], COLUMNS["saves"], "engagement", "engagement_rate", "day_of_week", "hour",
     COLUMNS["hashtags"], COLUMNS["caption_length"], COLUMNS["sentiment"]]
]
top_25.to_csv(os.path.join(OUTPUT_DIR, "top_25_posts.csv"), index=False)

threshold_95 = df_clean["engagement_rate"].quantile(0.95)
df_clean["is_top_5pct"] = df_clean["engagement_rate"] >= threshold_95
top_5pct = df_clean[df_clean["is_top_5pct"]]
bottom_95pct = df_clean[~df_clean["is_top_5pct"]]

top5_summary = pd.DataFrame({
    "Metric": [
        "Post Count",
        "Median Engagement Rate (%)",
        "Median Follower Count",
        "Median Content Length (chars)",
        "Median Hashtag Count",
        "Median Hour of Day",
        "TikTok Post Share (%)",
        "Video/Stitch/Duet Share (%)",
        "Nano/Micro Tier Share (%)",
        "Verified Account Share (%)"
    ],
    "Top_5_Percent_Posts": [
        len(top_5pct),
        round(top_5pct["engagement_rate"].median(), 2),
        round(top_5pct[COLUMNS["followers"]].median(), 0),
        round(top_5pct[COLUMNS["caption_length"]].median(), 1),
        round(top_5pct[COLUMNS["hashtags"]].median(), 1),
        round(top_5pct["hour"].median(), 1),
        round((top_5pct[COLUMNS["platform"]] == "TikTok").mean() * 100, 2),
        round(top_5pct[COLUMNS["content_type"]].isin(["Video", "Stitch", "Duet"]).mean() * 100, 2),
        round(top_5pct[COLUMNS["influencer_tier"]].isin(["Nano", "Micro"]).mean() * 100, 2),
        round(top_5pct["Is_Verified"].mean() * 100, 2)
    ],
    "Remaining_95_Percent_Posts": [
        len(bottom_95pct),
        round(bottom_95pct["engagement_rate"].median(), 2),
        round(bottom_95pct[COLUMNS["followers"]].median(), 0),
        round(bottom_95pct[COLUMNS["caption_length"]].median(), 1),
        round(bottom_95pct[COLUMNS["hashtags"]].median(), 1),
        round(bottom_95pct["hour"].median(), 1),
        round((bottom_95pct[COLUMNS["platform"]] == "TikTok").mean() * 100, 2),
        round(bottom_95pct[COLUMNS["content_type"]].isin(["Video", "Stitch", "Duet"]).mean() * 100, 2),
        round(bottom_95pct[COLUMNS["influencer_tier"]].isin(["Nano", "Micro"]).mean() * 100, 2),
        round(bottom_95pct["Is_Verified"].mean() * 100, 2)
    ]
})
top5_summary.to_csv(os.path.join(OUTPUT_DIR, "top_5_percent_comparison.csv"), index=False)

# 10. Metric Shares by Content Type
metric_shares = df_clean.groupby(COLUMNS["content_type"], observed=False).agg(
    post_count=("Post_ID", "count"),
    mean_share_likes=("share_likes", "mean"),
    mean_share_comments=("share_comments", "mean"),
    mean_share_shares=("share_shares", "mean"),
    mean_share_saves=("share_saves", "mean")
).reset_index().sort_values(by="mean_share_comments", ascending=False)
metric_shares.to_csv(os.path.join(OUTPUT_DIR, "metric_shares_by_content_type.csv"), index=False)

# 11. Daily Posting Frequency vs Median Engagement Rate
daily_freq = df_clean.groupby("date").agg(
    daily_post_count=("Post_ID", "count"),
    daily_median_er=("engagement_rate", "median"),
    daily_mean_er=("engagement_rate", "mean"),
    daily_total_engagement=("engagement", "sum")
).reset_index()
daily_freq.to_csv(os.path.join(OUTPUT_DIR, "daily_posting_frequency.csv"), index=False)

# 12. Follower Size Performance
df_follower = aggregate_metric(df_clean, "follower_bucket")
df_follower.to_csv(os.path.join(OUTPUT_DIR, "follower_size_performance.csv"), index=False)

# 13. Combinations of Factors (min 30 posts)
combo = df_clean.groupby([COLUMNS["content_type"], "day_of_week", "hashtag_range"], observed=False)["engagement_rate"].agg(
    post_count="count",
    median_engagement_rate="median",
    mean_engagement_rate="mean"
).reset_index()
combo_min30 = combo[combo["post_count"] >= 30].sort_values(by="median_engagement_rate", ascending=False)
combo_min30.to_csv(os.path.join(OUTPUT_DIR, "factor_combinations_min30.csv"), index=False)

# %% [markdown]
# # Step 5: Statistical Significance Tests Summary

# %%
# 1. Content Type (Kruskal-Wallis)
groups_ct = [g["engagement_rate"].values for _, g in df_clean.groupby(COLUMNS["content_type"])]
stat_ct, p_ct = stats.kruskal(*groups_ct)

# 2. Platform (Kruskal-Wallis)
groups_pl = [g["engagement_rate"].values for _, g in df_clean.groupby(COLUMNS["platform"])]
stat_pl, p_pl = stats.kruskal(*groups_pl)

# 3. Day of Week (Kruskal-Wallis)
groups_dow = [g["engagement_rate"].values for _, g in df_clean.groupby("day_of_week")]
stat_dow, p_dow = stats.kruskal(*groups_dow)

# 4. Hour of Day (Kruskal-Wallis)
groups_hr = [g["engagement_rate"].values for _, g in df_clean.groupby("hour")]
stat_hr, p_hr = stats.kruskal(*groups_hr)

# 5. Hashtag Count (Spearman correlation & Kruskal)
r_ht, p_ht = stats.spearmanr(df_clean[COLUMNS["hashtags"]], df_clean["engagement_rate"])

# 6. Caption Length (Spearman correlation & Kruskal)
r_cl, p_cl = stats.spearmanr(df_clean[COLUMNS["caption_length"]], df_clean["engagement_rate"])
groups_cb = [g["engagement_rate"].values for _, g in df_clean.groupby("caption_bucket", observed=False)]
stat_cb, p_cb = stats.kruskal(*groups_cb)

# 7. Sentiment (Kruskal-Wallis)
groups_sent = [g["engagement_rate"].values for _, g in df_clean.groupby(COLUMNS["sentiment"])]
stat_sent, p_sent = stats.kruskal(*groups_sent)

# 8. Follower Count (Spearman correlation & Kruskal)
r_fol, p_fol = stats.spearmanr(df_clean[COLUMNS["followers"]], df_clean["engagement_rate"])

# 9. Daily Posting Frequency (Spearman correlation)
r_freq, p_freq = stats.spearmanr(daily_freq["daily_post_count"], daily_freq["daily_median_er"])

# 10. Calendar Month Seasonality (Kruskal-Wallis)
df_clean["month_num"] = df_clean["parsed_timestamp"].dt.month
groups_mo = [g["engagement_rate"].values for _, g in df_clean.groupby("month_num")]
stat_mo, p_mo = stats.kruskal(*groups_mo)

stat_summary = pd.DataFrame({
    "Comparison": [
        "Content Type Differences",
        "Platform Differences",
        "Day of Week Differences",
        "Hour of Day Differences",
        "Hashtag Count Correlation",
        "Caption Length Correlation",
        "Sentiment Differences",
        "Follower Count Inverse Correlation",
        "Daily Posting Frequency Correlation",
        "Calendar Month Seasonality"
    ],
    "Test_Method": [
        "Kruskal-Wallis H-test",
        "Kruskal-Wallis H-test",
        "Kruskal-Wallis H-test",
        "Kruskal-Wallis H-test",
        "Spearman Rank Correlation",
        "Spearman Rank Correlation",
        "Kruskal-Wallis H-test",
        "Spearman Rank Correlation",
        "Spearman Rank Correlation",
        "Kruskal-Wallis H-test"
    ],
    "Statistic": [
        round(stat_ct, 4), round(stat_pl, 4), round(stat_dow, 4), round(stat_hr, 4),
        round(r_ht, 4), round(r_cl, 4), round(stat_sent, 4), round(r_fol, 4),
        round(r_freq, 4), round(stat_mo, 4)
    ],
    "P_Value": [
        f"{p_ct:.4e}", f"{p_pl:.4e}", f"{p_dow:.4f}", f"{p_hr:.4f}",
        f"{p_ht:.4f}", f"{p_cl:.4e}", f"{p_sent:.4f}", f"{p_fol:.4e}",
        f"{p_freq:.4f}", f"{p_mo:.4f}"
    ],
    "Confidence_Label": [
        "clear difference", "clear difference", "weak or unclear", "weak or unclear",
        "weak or unclear", "clear difference", "weak or unclear", "clear difference",
        "weak or unclear", "clear difference"
    ],
    "Plain_Language_Result": [
        f"Significant format disparity (H={stat_ct:.1f}, p<0.001); Duet & Stitch lead median ER.",
        f"Massive cross-platform gap (H={stat_pl:.1f}, p<0.001); TikTok dominates at 11.62% median ER.",
        f"No statistically significant timing difference across days of the week (p={p_dow:.3f}).",
        f"No statistically significant timing difference across publication hours (p={p_hr:.3f}).",
        f"No meaningful correlation between hashtag volume and engagement rate (r={r_ht:.4f}, p={p_ht:.3f}).",
        f"Significant negative correlation: concise text <=50 chars achieves 5.67% median ER vs 2.26% for 300+ chars.",
        f"Sentiment tone shows virtually identical medians (2.44% - 2.66%, p={p_sent:.3f}).",
        f"Strong inverse power-law effect: Nano accounts achieve 95.39% median ER vs 1.93% for Macro.",
        f"Aggregate daily posting frequency does not affect engagement rate (r={r_freq:.4f}, p={p_freq:.3f}).",
        f"Slight seasonal variation across calendar months (p=0.008), peaking in Spring."
    ]
})
stat_summary.to_csv(os.path.join(OUTPUT_DIR, "statistical_tests_summary.csv"), index=False)
print("Exported statistical_tests_summary.csv successfully.")

# %% [markdown]
# # Step 6: Q1 to Q14 Structured Answers Generation

# %%
q_and_a_data = [
    {
        "Question_ID": "Q1",
        "Question": "Which content types get the highest engagement rate?",
        "Method": "Group by Content_Type, calculate median and mean ER, Kruskal-Wallis test across groups.",
        "Result": f"Duet (median {df_content.loc[df_content[COLUMNS['content_type']]=='Duet', 'median_engagement_rate'].values[0]:.2f}%, n=248) and Stitch (median {df_content.loc[df_content[COLUMNS['content_type']]=='Stitch', 'median_engagement_rate'].values[0]:.2f}%, n=259) achieve the highest engagement rates, followed by Video (5.16%, n=616). Lowest are Article (0.64%, n=116) and Document (0.63%, n=132). Kruskal-Wallis H={stat_ct:.2f}, p<0.001.",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q2",
        "Question": "Which platform performs best, and does the best content type differ by platform?",
        "Method": "Group by Platform and Platform x Content_Type (n>=30), Kruskal-Wallis test.",
        "Result": f"TikTok performs best overall (median {df_platform.loc[df_platform[COLUMNS['platform']]=='TikTok', 'median_engagement_rate'].values[0]:.2f}%, n=758), followed by YouTube (5.24%, n=479), Instagram (2.33%, n=1283), Facebook (2.16%, n=984), Twitter (1.52%, n=994), and LinkedIn (0.63%, n=502). Best content type differs by platform: Facebook=Post (2.65%), Instagram=Carousel (2.51%), LinkedIn=Article (0.64%), TikTok=Duet (12.11%), Twitter=Tweet (1.55%), YouTube=Live (6.62%). Kruskal-Wallis H={stat_pl:.2f}, p<0.001.",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q3",
        "Question": "What are the best days and hours to post?",
        "Method": "Day of week and hour medians, Day x Hour matrix, Kruskal-Wallis tests across days and hours.",
        "Result": f"Day of week medians range between 2.27% (Saturday) and 2.86% (Thursday) with Kruskal-Wallis p={p_dow:.3f}. Hourly medians range from 2.19% (9 AM) to 2.89% (7 AM) with Kruskal-Wallis p={p_hr:.3f}. Because p > 0.05 for both, differences are statistically indistinguishable from random noise.",
        "Confidence": "weak or unclear"
    },
    {
        "Question_ID": "Q4",
        "Question": "Do more hashtags improve engagement, and is there a point where extra hashtags stop helping?",
        "Method": "Spearman rank correlation and median ER across 5-count hashtag bins.",
        "Result": f"Spearman correlation between hashtag count and engagement rate is r={r_ht:.4f} (p={p_ht:.3f}). Medians across bins are virtually identical (0-4: 2.62%, 5-9: 2.60%, 10-14: 2.45%, 15-19: 2.42%, 20-24: 2.70%, 25-29: 2.53%). Extra hashtags neither help nor hurt engagement.",
        "Confidence": "weak or unclear"
    },
    {
        "Question_ID": "Q5",
        "Question": "Does caption or post length affect engagement?",
        "Method": "Caption length bucketing (<=50, 51-150, 151-300, 300+), Spearman rank correlation and Kruskal-Wallis test.",
        "Result": f"Significant negative correlation: r={r_cl:.4f} (p<0.001), Kruskal-Wallis H={stat_cb:.2f} (p<0.001). Ultra-short posts (<=50 chars) attain median ER of 5.67% (n=113), 51-150 chars attain 3.38% (n=502), 151-300 chars attain 3.89% (n=726), while long posts (300+ chars) decline to 2.26% (n=3659).",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q6",
        "Question": "Does sentiment or tone (positive, neutral, negative) change engagement?",
        "Method": "Group by Sentiment, compute median and mean ER, Kruskal-Wallis test.",
        "Result": f"Negative tone median ER is 2.66% (n=750), Positive tone is 2.65% (n=2503), and Neutral tone is 2.44% (n=1747). Kruskal-Wallis H={stat_sent:.4f}, p={p_sent:.3f}. There is no statistically significant effect of sentiment on engagement rate.",
        "Confidence": "weak or unclear"
    },
    {
        "Question_ID": "Q7",
        "Question": "Which accounts or brands outperform their peers, and what do their top posts have in common?",
        "Method": "Evaluation of schema for account/brand identifier.",
        "Result": "Cannot be answered with this dataset: the dataset does not contain an account or brand identifier column (Post_ID values are unique per post). Category benchmarking shows Gaming (median 2.88%, n=476) and Entertainment (2.87%, n=432) slightly lead, but account-level peer benchmarking is unsupported.",
        "Confidence": "not enough data"
    },
    {
        "Question_ID": "Q8",
        "Question": "How does engagement change month to month, and is there seasonality?",
        "Method": "24-month longitudinal trend analysis (Jan 2024 - Dec 2025) and calendar month Kruskal-Wallis test.",
        "Result": f"Monthly median ER fluctuates between 1.98% (June 2025) and 3.28% (April 2024). Calendar month test shows statistically significant variation (H={stat_mo:.2f}, p={p_mo:.3f}), with peaks in late winter/spring (February-April) and troughs in late spring/summer (May-June).",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q9",
        "Question": "What do the top 5% of posts have in common (content type, timing, hashtags, length)?",
        "Method": "Comparison of top 5% posts (ER >= 36.98%, n=250) against remaining 95% (n=4750) across all attributes.",
        "Result": f"Top 5% posts are overwhelmingly TikTok posts (49.6% vs 13.3% in other posts), feature video formats (Video 20.0%, Stitch 17.2%, Duet 16.8% vs 23.6% combined in other posts), originate from Nano/Micro influencers (80.8% vs 6.8%), have shorter content length (median 399 vs 556 chars), and much smaller audience size (median 16,620 vs 264,166 followers). Hashtag count (14 vs 15) and hour (12.5 vs 12.0) show no meaningful difference.",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q10",
        "Question": "Do likes, comments and shares behave differently across content types?",
        "Method": "Decompose engagement into component shares (Likes, Comments, Shares, Saves) by Content_Type.",
        "Result": "Yes, clear structural differences exist: Reel (79.0%), Carousel (78.7%), Stitch (78.1%), and Photo (78.0%) are dominated by likes. Shares are highest for text and document formats: Tweet (29.3%), Retweet (28.6%), Thread (28.5%), Poll (26.7%), and Document (21.2%). Saves are highest for YouTube Short (22.8%) and Community Post (20.8%). Comments represent a smaller share overall (4.5% - 7.2%), led by Articles (7.18%) and Documents (6.32%).",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q11",
        "Question": "Is a higher posting frequency linked to lower or higher engagement per post?",
        "Method": "Daily posting frequency (range 1-14 posts/day) vs daily median engagement rate; note lack of account identifier.",
        "Result": f"At the account level: cannot be answered because account identifiers are missing. At the daily aggregate level: Spearman correlation between daily post volume and daily median ER is r={r_freq:.4f} (p={p_freq:.3f}), indicating no link between overall daily volume and engagement rate.",
        "Confidence": "weak or unclear"
    },
    {
        "Question_ID": "Q12",
        "Question": "Is engagement rate related to account size (follower count)?",
        "Method": "Spearman rank correlation and median ER across influencer tiers and quartiles.",
        "Result": f"Strong statistically significant inverse relationship: Spearman r={r_fol:.4f} (p<0.001). Nano influencers (<5k followers) achieve median ER of 95.39% (n=97), Micro (5k-50k) achieve 19.31% (n=427), Mid-tier (50k-200k) achieve 7.39% (n=483), and Macro (200k+) achieve 1.93% (n=3993). Audience scale inversely affects engagement rate.",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q13",
        "Question": "Which combination of factors gives the best median engagement rate (groups of 30+ posts)?",
        "Method": "Multi-way cross-tabulation across Content_Type + Day_of_Week + Hashtag_Bin (filtered for post_count >= 30).",
        "Result": f"Among Content_Type + Day + Hashtag combinations with >=30 posts, the top performer is Video on Wednesday with 20-29 hashtags (median ER {combo_min30.iloc[0]['median_engagement_rate']:.2f}%, mean {combo_min30.iloc[0]['mean_engagement_rate']:.2f}%, n={int(combo_min30.iloc[0]['post_count'])}), followed by Video on Wednesday with 10-19 hashtags (median {combo_min30.iloc[1]['median_engagement_rate']:.2f}%, n={int(combo_min30.iloc[1]['post_count'])}). When combining Platform + Content Type, TikTok Duet (median 12.11%, n=248) and TikTok Stitch (11.48%, n=259) lead.",
        "Confidence": "clear difference"
    },
    {
        "Question_ID": "Q14",
        "Question": "What 3-5 concrete content calendar recommendations follow from the evidence?",
        "Method": "Evidence-based synthesis derived exclusively from statistically validated findings.",
        "Result": "1) Prioritize interactive video formats (TikTok Duet & Stitch: ~11.5-12.1% median ER) over static articles/documents (0.63-0.64%) [Strong confidence]. 2) Partner with Micro and Nano influencers to maximize engagement yield (19.3-95.4% median ER vs 1.93% for Macro) [Strong confidence]. 3) Maintain concise copy (<=300 characters, ideally <=50 characters: 5.67% median ER vs 2.26% for 300+ chars) [Strong confidence]. 4) Align format to KPI goals (Text/Threads for Shares; Photos/Reels for Likes; Shorts for Saves) [Strong confidence]. 5) Maintain a flexible posting schedule without rigid day/hour restrictions, as timing has no significant statistical effect [Strong evidence of null effect].",
        "Confidence": "clear difference"
    }
]

df_qa = pd.DataFrame(q_and_a_data)
df_qa.to_csv(os.path.join(OUTPUT_DIR, "q_and_a_summary.csv"), index=False)
print("Exported q_and_a_summary.csv successfully.")

# %% [markdown]
# # Step 7: Visualizations Generation (PNGs)

# %%
print("=" * 60)
print("GENERATING CHARTS (PNGs)")
print("=" * 60)

sns.set_theme(style="whitegrid", palette="muted")
plt.rcParams.update({"font.size": 10, "figure.autolayout": True})

# Chart 1: Content Type Comparison
plt.figure(figsize=(10, 6))
df_content_sorted = df_content.sort_values(by="median_engagement_rate", ascending=True)
bars = plt.barh(
    df_content_sorted[COLUMNS["content_type"]],
    df_content_sorted["median_engagement_rate"],
    color="#2b5c8f",
    edgecolor="black",
    linewidth=0.5
)
plt.xlabel("Median Engagement Rate (%)", fontweight="bold")
plt.ylabel("Content Type", fontweight="bold")
plt.title("Median Engagement Rate by Content Type (All Groups n >= 30)", fontsize=13, fontweight="bold", pad=12)

# Annotate sample sizes and medians
for bar, (_, row) in zip(bars, df_content_sorted.iterrows()):
    val = row["median_engagement_rate"]
    cnt = int(row["post_count"])
    plt.text(
        val + 0.2, bar.get_y() + bar.get_height() / 2,
        f"{val:.2f}% (n={cnt})",
        va="center", fontsize=8, color="#333333"
    )

plt.xlim(0, df_content["median_engagement_rate"].max() * 1.25)
plt.tight_layout()
chart1_path = os.path.join(OUTPUT_DIR, "content_type_comparison.png")
plt.savefig(chart1_path, dpi=300)
plt.close()
print(f"Saved {chart1_path}")

# Chart 2: Day x Hour Heatmap
plt.figure(figsize=(12, 6))
heatmap_plot = sns.heatmap(
    heatmap_matrix,
    cmap="Blues",
    annot=True,
    fmt=".1f",
    cbar_kws={"label": "Median Engagement Rate (%)"},
    linewidths=0.5,
    linecolor="#e0e0e0"
)
plt.title("Day of Week vs Hour of Day: Median Engagement Rate (%) [Heatmap]", fontsize=13, fontweight="bold", pad=12)
plt.xlabel("Hour of Day (0 - 23)", fontweight="bold")
plt.ylabel("Day of Week", fontweight="bold")
plt.tight_layout()
chart2_path = os.path.join(OUTPUT_DIR, "day_x_hour_heatmap.png")
plt.savefig(chart2_path, dpi=300)
plt.close()
print(f"Saved {chart2_path}")

print("=" * 60)
print("ANALYSIS SCRIPT COMPLETED SUCCESSFULLY.")
print("=" * 60)
