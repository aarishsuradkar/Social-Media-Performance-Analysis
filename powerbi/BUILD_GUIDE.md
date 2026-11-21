# Power BI Desktop Build Guide: Social Media Performance Analysis

A complete, production-ready blueprint for replicating the Social Media Performance Analysis dashboard inside **Power BI Desktop**. This guide details data modeling, DAX measure creation, visual configurations across three report pages, matrix heatmap formatting, and best practices.

---

## 1. Data Ingestion & Model Architecture

### 1.1 Files to Import
Open Power BI Desktop, select **Get Data > Text/CSV**, and import the following precomputed files from the `output/` directory:
1. `clean_posts.csv` (Primary Fact Table, 5,000 rows)
2. `monthly_trend.csv` (Aggregated monthly dimension/trend)
3. `timing_day_x_hour_heatmap.csv` (Matrix staging table for 2D heatmap)
4. `statistical_tests_summary.csv` (Reference table for statistical test outcomes)

### 1.2 Data Types & Column Transformations (Power Query Editor)
In **Power Query Editor**, verify and explicitly set data types:

| Table | Column | Power Query Data Type | Formatting in Report View |
| :--- | :--- | :--- | :--- |
| `clean_posts` | `Post_ID` | Text | Text |
| `clean_posts` | `Timestamp` | Date/Time | `yyyy-mm-dd hh:nn:ss` |
| `clean_posts` | `Platform` | Text | Text |
| `clean_posts` | `Content_Type` | Text | Text |
| `clean_posts` | `Category` | Text | Text |
| `clean_posts` | `Likes`, `Comments`, `Shares`, `Saves` | Whole Number | Whole Number with commas (`#,0`) |
| `clean_posts` | `Follower_Count` | Whole Number | Whole Number with commas (`#,0`) |
| `clean_posts` | `engagement` | Whole Number | Whole Number with commas (`#,0`) |
| `clean_posts` | `engagement_rate` | Decimal Number | Percentage (`0.00%`) |
| `clean_posts` | `hour` | Text | Text (Crucial for discrete axis ordering: `"00"`, `"01"`, etc.) |
| `clean_posts` | `day_of_week` | Text | Text (Sort by `day_of_week_num` 1-7) |
| `clean_posts` | `month` | Text | Text |
| `clean_posts` | `caption_bucket` | Text | Text |
| `clean_posts` | `hashtag_bin` | Text | Text |
| `clean_posts` | `Influencer_Tier` | Text | Text |

> [!IMPORTANT]
> **Sort by Column Configuration:** In the `clean_posts` table, select the `day_of_week` column, click **Column Tools > Sort by Column**, and choose an integer weekday index (Monday=1, Sunday=7) so days appear chronologically instead of alphabetically.

---

## 2. Core DAX Measures

To prevent improper summation of percentage rates, define explicit DAX measures inside a dedicated `_Measures` table:

```dax
// 1. Post Volume
Total_Posts = COUNTROWS('clean_posts')

// 2. Total Cumulative Engagement
Total_Engagement = SUM('clean_posts'[engagement])

// 3. Robust Median Engagement Rate (Primary Metric)
Median_Engagement_Rate = MEDIAN('clean_posts'[engagement_rate])

// 4. Mean Engagement Rate (For Skew Reference)
Mean_Engagement_Rate = AVERAGE('clean_posts'[engagement_rate])

// 5. Interquartile Range (Dispersion Measure)
IQR_Engagement_Rate = 
    PERCENTILE.INC('clean_posts'[engagement_rate], 0.75) - 
    PERCENTILE.INC('clean_posts'[engagement_rate], 0.25)

// 6. Dynamic Sample Size Warning Label
Sample_Size_Status = 
    IF(
        [Total_Posts] < 30, 
        "⚠️ Low Sample (<30 posts) - Do not rank", 
        "✅ Statistically Valid Sample (n=" & FORMAT([Total_Posts], "#,0") & ")"
    )
```

---

## 3. Report Page Specifications

### Page 1: Overview & Longitudinal Trends

#### Visual 1.1: KPI Summary Cards (Top Row)
- **Visual Type**: Card (New) or 4 Single Cards
- **Fields**:
  - Card 1: `[Total_Posts]` (Callout: `5,000`, Subtitle: "Total Posts Analyzed")
  - Card 2: `[Total_Engagement]` (Callout: `47.33M`, Subtitle: "Likes + Comments + Shares + Saves")
  - Card 3: `[Median_Engagement_Rate]` (Callout: `2.57%`, Subtitle: "Robust Primary Metric")
  - Card 4: `[Mean_Engagement_Rate]` (Callout: `12.87%`, Subtitle: "Positively Skewed by Nano Outliers")

#### Visual 1.2: Cross-Platform Performance Ranking
- **Visual Type**: Clustered Bar Chart
- **Y-Axis**: `clean_posts[Platform]`
- **X-Axis**: `[Median_Engagement_Rate]`
- **Tooltips**: `[Total_Posts]`, `[Mean_Engagement_Rate]`, `[Sample_Size_Status]`
- **Data Labels**: On (Format: `0.00%`)
- **Color**: Monochromatic Deep Blue (`#2563EB`)
- **Title**: *"Median Engagement Rate by Platform (n >= 30)"*

#### Visual 1.3: 24-Month Longitudinal Trend
- **Visual Type**: Line and Clustered Column Chart
- **Shared X-Axis**: `clean_posts[month]` (Sorted chronologically: `2024-01` to `2025-12`)
- **Column Y-Axis**: `[Total_Posts]` (Color: Light Gray `#CBD5E1`)
- **Line Y-Axis**: `[Median_Engagement_Rate]` (Color: Primary Blue `#1E40AF`, Width: 3px)
- **Title**: *"Monthly Median Engagement Rate vs. Post Publication Volume"*

#### Visual 1.4: Dynamic Executive Callout (Text Box)
Add a styled narrative box below the charts:
> **Executive Summary:** TikTok delivers a standout median engagement rate of **11.62%** (n=758), outperforming YouTube (**5.24%**), Instagram (**2.33%**), Facebook (**2.16%**), Twitter (**1.52%**), and LinkedIn (**0.63%**). Longitudinal tracking confirms cyclical peaks in early Spring (April 2024 at 3.28%), with overall volume stable between 180 and 240 posts/month.

---

### Page 2: Content Formats & Text Optimization

#### Visual 2.1: Content Format Leaderboard
- **Visual Type**: Clustered Bar Chart (Horizontal)
- **Y-Axis**: `clean_posts[Content_Type]` (Sorted descending by `[Median_Engagement_Rate]`)
- **X-Axis**: `[Median_Engagement_Rate]`
- **Tooltips**: `[Total_Posts]`, `[Mean_Engagement_Rate]`
- **Data Labels**: On (`0.00%`)
- **Title**: *"Median Engagement Rate by Content Format (n >= 30)"*

#### Visual 2.2: Hashtag Count Sensitivity
- **Visual Type**: Clustered Column Chart
- **X-Axis**: `clean_posts[hashtag_bin]` (`0-4`, `5-9`, `10-14`, `15-19`, `20-24`, `25-29`)
- **Y-Axis**: `[Median_Engagement_Rate]`
- **Data Labels**: On (`0.00%`)
- **Title**: *"Median Engagement Rate across Hashtag Volumes"*

#### Visual 2.3: Caption Character Length Performance
- **Visual Type**: Clustered Column Chart
- **X-Axis**: `clean_posts[caption_bucket]` (`<=50`, `51-150`, `151-300`, `300+`)
- **Y-Axis**: `[Median_Engagement_Rate]`
- **Data Labels**: On (`0.00%`)
- **Title**: *"Impact of Caption Length on Engagement Rate"*

#### Visual 2.4: Insight Callout (Text Box)
> **Key Finding:** Interactive TikTok-native video formats lead performance (Duet: **12.11%**, Stitch: **11.48%**). Text brevity is strongly rewarded: captions `<=50` characters achieve **5.67%** median ER vs. **2.26%** for captions `300+` characters. Hashtag count exhibits no correlation with engagement (r = -0.007, p = 0.608).

---

### Page 3: Timing Matrix & Benchmarks

#### Visual 3.1: Day of Week × Hour of Day Heatmap Matrix
- **Visual Type**: Matrix Visual
- **Rows**: `clean_posts[day_of_week]` (Sorted Monday through Sunday)
- **Columns**: `clean_posts[hour]` (0 to 23, formatted as text `"00"` to `"23"`)
- **Values**: `[Median_Engagement_Rate]`
- **Conditional Formatting**:
  - Select `[Median_Engagement_Rate]` in Values > **Conditional Formatting > Background Color**
  - Format Style: **Gradient**
  - Minimum: Lowest value (`#EFF6FF` soft light blue)
  - Center: 50th Percentile (`#93C5FD` mid sky blue)
  - Maximum: Highest value (`#1E3A8A` deep navy blue)
- **Title**: *"Timing Optimization Heatmap: Median Engagement Rate (%)"*

#### Visual 3.2: Influencer Scale / Account Tier Benchmark
- **Visual Type**: Clustered Bar Chart
- **Y-Axis**: `clean_posts[Influencer_Tier]` (`Nano`, `Micro`, `Mid-tier`, `Macro`)
- **X-Axis**: `[Median_Engagement_Rate]`
- **Data Labels**: On (`0.00%`)
- **Title**: *"Audience Scale Law: Median Engagement Rate by Account Tier"*

#### Visual 3.3: Category Benchmark
- **Visual Type**: Clustered Column Chart
- **X-Axis**: `clean_posts[Category]`
- **Y-Axis**: `[Median_Engagement_Rate]`
- **Title**: *"Median Engagement Rate by Content Category"*

#### Visual 3.4: Top 25 Posts Table
- **Visual Type**: Table Visual
- **Columns**: `Post_ID`, `Platform`, `Content_Type`, `Influencer_Tier`, `Follower_Count`, `Likes`, `Comments`, `Shares`, `Saves`, `[Median_Engagement_Rate]`
- **Sorting**: `[Median_Engagement_Rate]` Descending (Filtered to Top 25 via visual-level filter)
- **Title**: *"Top 25 Outperforming Posts"*

---

## 4. Global Slicers & Interactivity Settings

Add a uniform Slicer Panel on the left or top header of every page:
1. `clean_posts[Platform]` (Dropdown / Tile, Multi-select enabled)
2. `clean_posts[Influencer_Tier]` (Dropdown, Multi-select enabled)
3. `clean_posts[Category]` (Dropdown, Multi-select enabled)

> [!NOTE]
> **Pre-Publishing Checklist**: Always click **Clear all slicers** (or use a reset bookmark) before saving, exporting to PDF, or capturing portfolio screenshots.

---

## 5. Common Power BI Mistakes to Avoid

| Mistake | Risk / Impact | Correct Method |
| :--- | :--- | :--- |
| **Summing Engagement Rates (`SUM(engagement_rate)`)** | Yields meaningless percentages (e.g., thousands of percent). | Always aggregate rates using `MEDIAN()` or `AVERAGE()` via DAX. |
| **Using Default Mean instead of Median** | Distorts benchmarks due to extreme positive skew from Nano influencers. | Use `MEDIAN('clean_posts'[engagement_rate])` as the primary KPI. |
| **Alphabetical Day Ordering** | Displays Friday, Monday, Saturday, Sunday... ruining heatmap comprehension. | Apply **Sort by Column** on `day_of_week` using a numeric index (1 to 7). |
| **Treating Hour as Numeric Continuous Axis** | Power BI creates continuous scale gaps or averages hours. | Cast `hour` as formatted Text (`"00"`, `"01"`) or discrete category. |
| **Ranking Groups with Low Sample Size** | Claims false trends from formats with 2 or 3 total posts. | Filter visual-level display to `[Total_Posts] >= 30` or display sample warnings. |
| **Forgetting to Clear Slicers** | Reports captured while filtered by a single platform mislead executive readers. | Clear all slicers before taking screenshots or publishing. |
