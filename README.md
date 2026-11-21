# Social Media Performance Analysis

> **A portfolio-grade data analytics project evaluating multi-platform social media engagement, format efficacy, audience scale dynamics, and publishing timing across 5,000 posts.**

---

## 🎯 Executive Overview & Business Question

Social media marketing teams face continuous resource allocation decisions across platforms, content formats, caption lengths, hashtag volumes, and scheduling calendars. This analysis addresses the core business question:

> **How do platform selection, content format, text brevity, and account audience scale drive engagement rate, and what evidence-backed scheduling and format strategies maximize return on social media investment?**

Every metric, statistical test, insight statement, and recommendation in this project is strictly computed by code from the underlying dataset. No values are estimated, invented, or hard-coded.

---

## 📁 Dataset Profile

- **Source**: Workspace dataset `social_media_engagement_dataset.csv`.
- **Data Origin**: **Synthetic / Generated** (simulating cross-platform engagement across multi-tiered creators over a two-year period). Because the data is synthetic, all conclusions are evaluated using conservative non-parametric methods, and findings are interpreted with modest, empirical boundaries.
- **Records & Dimensions**: 5,000 posts, 20 attributes (0 missing values, 0 exact duplicates).
- **Date Range**: January 1, 2024 (01:42:00) to December 31, 2025 (21:56:00) — exactly 730 days (2 full calendar years).
- **Platforms Covered**: Instagram (1,283 posts), Twitter/X (994 posts), Facebook (984 posts), TikTok (758 posts), LinkedIn (502 posts), YouTube (479 posts).
- **Formats Covered**: 17 distinct content types (Video, Story, Poll, Post, Live, Carousel, Photo, Reel, Stitch, Retweet, Duet, Tweet, Thread, Community Post, Document, Short, Article).

---

## 📐 Analytical Approach & Engagement Rate Definition

### Engagement Rate Formula
In accordance with standard social media analytics hierarchy (Reach $\rightarrow$ Impressions $\rightarrow$ Followers), because Reach and Impressions columns are absent from the dataset, the robust denominator is **Follower Count**:

$$\text{Engagement} = \text{Likes} + \text{Comments} + \text{Shares} + \text{Saves}$$

$$\text{Engagement Rate (\%)} = \left( \frac{\text{Engagement}}{\text{Follower\_Count}} \right) \times 100 \quad \text{for } \text{Follower\_Count} > 0$$

### Methodological Principles
1. **Median as Primary Metric**: Social media engagement rates exhibit extreme positive skew (Skewness > 15; Mean = 12.87% vs. Median = 2.57%). All rankings, comparisons, and visualizations rely on the **Median**, accompanied by sample sizes ($n$) and interquartile ranges (IQR).
2. **Sample Size Threshold**: Groups with fewer than 30 posts ($n < 30$) are marked as "low sample" and excluded from rankings.
3. **Hypothesis Testing**: Group differences are tested non-parametrically using the Kruskal-Wallis $H$-test. Monotonic relationships are evaluated via Spearman rank correlation ($r$).
4. **Honest Reporting**: Where differences fail to reach statistical significance ($p \ge 0.05$) or where variables are missing, the report explicitly states that no clear difference exists. Correlation is never conflated with causation.

---

## 💡 Key Computed Findings

1. **Platform Hierarchy**: **TikTok** dominates cross-platform engagement with a median ER of **11.62%** ($n=758$), followed by **YouTube** (**5.24%**, $n=479$), **Instagram** (**2.33%**, $n=1,283$), **Facebook** (**2.16%**, $n=984$), **Twitter** (**1.52%**, $n=994$), and **LinkedIn** (**0.63%**, $n=502$) ($H = 1,760.36, p < 0.001$).
2. **Format Disparity**: Interactive short-form video features lead all formats: **Duet** achieves **12.11%** median ER ($n=248$) and **Stitch** achieves **11.48%** ($n=259$), followed by standard **Video** (**5.16%**, $n=616$). Static long-form formats lag significantly: **Article** (**0.64%**, $n=116$) and **Document** (**0.63%**, $n=132$) ($H = 1,390.34, p < 0.001$).
3. **Audience Scale Inverse Law**: Follower count exhibits a massive negative correlation with engagement rate ($r = -0.602, p < 0.001$). **Nano influencers** ($<5,000$ followers) achieve **95.39%** median ER ($n=97$), **Micro** ($5,000-50,000$) achieve **19.31%** ($n=427$), **Mid-tier** ($50,000-200,000$) achieve **7.39%** ($n=483$), while **Macro** ($200,000+$) achieve **1.93%** ($n=3,993$).
4. **Text Brevity Advantage**: Captions $\le 50$ characters deliver **5.67%** median ER ($n=113$), compared to **2.26%** for captions $300+$ characters ($n=3,659$). Spearman correlation confirms an inverse relationship ($r = -0.246, p < 0.001$).
5. **Null Timing & Hashtag Effects**:
   - Day of week medians range between **2.27%** (Saturday) and **2.86%** (Thursday), but differences are statistically insignificant ($p = 0.617$).
   - Hourly medians range from **2.19%** (9 AM) to **2.89%** (7 AM), with differences statistically indistinguishable from random chance ($p = 0.562$).
   - Hashtag volume has zero correlation with engagement rate ($r = -0.007, p = 0.608$).

---

## ❓ Questions & Answers (Q1 – Q14)

Every question below is answered exclusively using numbers computed directly from the dataset, classified under strict confidence labels:
- **Clear difference**: $p < 0.05$ and a meaningful practical effect size.
- **Weak or unclear**: $p \ge 0.05$ or negligible practical effect.
- **Not enough data**: Dataset lacks the required schema or variable.

| # | Question | Method & Evidence | Computed Result | Confidence |
| :--- | :--- | :--- | :--- | :--- |
| **Q1** | Which content types get the highest engagement rate? | Kruskal-Wallis across 17 formats ($H = 1,390.34, p < 0.001$). | **Duet** (median **12.11%**, $n=248$) and **Stitch** (median **11.48%**, $n=259$) lead, followed by **Video** (**5.16%**, $n=616$). Lowest are **Article** (**0.64%**, $n=116$) and **Document** (**0.63%**, $n=132$). | **Clear difference** |
| **Q2** | Which platform performs best, and does the best content type differ by platform? | Kruskal-Wallis cross-platform ($H = 1,760.36, p < 0.001$) and cross-tabulation ($n \ge 30$). | **TikTok** leads (**11.62%**, $n=758$). Best format differs by platform: Facebook = **Post** (**2.65%**), Instagram = **Carousel** (**2.51%**), LinkedIn = **Article** (**0.64%**), TikTok = **Duet** (**12.11%**), Twitter = **Tweet** (**1.55%**), YouTube = **Live** (**6.62%**). | **Clear difference** |
| **Q3** | What are the best days and hours to post? | Day of week and hourly medians, 7x24 heatmap, Kruskal-Wallis tests. | Day medians range **2.27% - 2.86%** ($p = 0.617$). Hour medians range **2.19% - 2.89%** ($p = 0.562$). Both tests show no statistically significant timing effect; variations are random noise. | **Weak or unclear** |
| **Q4** | Do more hashtags improve engagement, and is there a point where extra hashtags stop helping? | Spearman correlation and medians across 5-count hashtag bins. | Spearman $r = -0.0072$ ($p = 0.608$). Medians across bins remain flat (**2.42% to 2.70%**). Hashtag count has no discernible impact on engagement rate. | **Weak or unclear** |
| **Q5** | Does caption or post length affect engagement? | Caption length bucketing, Spearman correlation ($r = -0.246, p < 0.001$), Kruskal-Wallis ($H = 139.58, p < 0.001$). | Captions **$\le 50$ chars** achieve **5.67%** median ER ($n=113$), **51-150** achieve **3.38%** ($n=502$), **151-300** achieve **3.89%** ($n=726$), and **$300+$ chars** decline to **2.26%** ($n=3,659$). | **Clear difference** |
| **Q6** | Does sentiment or tone change engagement? | Kruskal-Wallis test across sentiment categories ($H = 1.4137, p = 0.493$). | Negative tone median ER is **2.66%** ($n=750$), Positive is **2.65%** ($n=2,503$), and Neutral is **2.44%** ($n=1,747$). Tone differences are not statistically significant. | **Weak or unclear** |
| **Q7** | Which accounts or brands outperform their peers, and what do their top posts have in common? | Schema audit for account/brand identifier column. | **Cannot be answered with this dataset**: Account and brand names are absent (`Post_ID` is unique per post). Category benchmarks show Gaming (**2.88%**) and Entertainment (**2.87%**) slightly lead. | **Not enough data** |
| **Q8** | How does engagement change month to month, and is there seasonality? | 24-month longitudinal time series and calendar month Kruskal-Wallis test. | Monthly medians range from **1.98%** (June 2025) to **3.28%** (April 2024). Calendar month test indicates significant seasonality ($H = 25.42, p = 0.008$), peaking in late winter/spring. | **Clear difference** |
| **Q9** | What do the top 5% of posts have in common? | Attribute comparison between Top 5% (ER $\ge 36.98\%$, $n=250$) and Bottom 95% ($n=4,750$). | Top 5% are concentrated on **TikTok** (**49.6%** vs **13.3%**), video formats (**54.0%** vs **23.6%**), **Nano/Micro** influencers (**80.8%** vs **6.8%**), shorter copy (**399** vs **556** chars), and smaller followers (**16,620** vs **264,166**). | **Clear difference** |
| **Q10** | Do likes, comments and shares behave differently across content types? | Metric share decomposition (component / total engagement). | Reel (**79.0%**), Carousel (**78.7%**), Stitch (**78.1%**), and Photo (**78.0%**) drive likes. Tweet (**29.3%**), Retweet (**28.6%**), Thread (**28.5%**), and Document (**21.2%**) drive shares. YouTube Short (**22.8%**) and Community Post (**20.8%**) drive saves. | **Clear difference** |
| **Q11** | Is a higher posting frequency linked to lower or higher engagement per post? | Daily post volume (1 to 14 posts/day) vs. daily median ER correlation. | Account-level frequency cannot be evaluated (no account column). Aggregate daily posting frequency exhibits no significant relationship with median ER ($r = -0.0541, p = 0.144$). | **Weak or unclear** |
| **Q12** | Is engagement rate related to account size (follower count)? | Spearman correlation and median ER by follower tier. | Strong negative power-law relationship ($r = -0.6024, p < 0.001$). Nano influencers reach **95.39%** median ER vs. **1.93%** for Macro influencers. | **Clear difference** |
| **Q13** | Which combination of factors gives the best median engagement rate ($n \ge 30$)? | Cross-tabulation across Content Type + Day of Week + Hashtag Range ($n \ge 30$). | **Video on Wednesday with 20-29 hashtags** leads at **6.95%** median ER ($n=37$, mean = 38.80%), followed by **Video on Wednesday with 10-19 hashtags** (**6.20%**, $n=32$). Combining Platform + Format, **TikTok Duet** (**12.11%**, $n=248$) leads. | **Clear difference** |
| **Q14** | What 3-5 concrete content calendar recommendations follow from the evidence? | Evidence synthesis across validated statistical findings. | 1) Prioritize interactive video (TikTok Duets/Stitches). 2) Partner with Nano/Micro creators. 3) Enforce concise copy ($\le 300$ chars). 4) Match format to objective (Text for shares, Video/Photo for likes, Shorts for saves). 5) Keep schedule flexible. | **Clear difference** |

---

## 📅 Actionable Content Calendar Recommendations

1. **Pivot Video Production Toward Interactive Remix Formats** (*Strong Confidence*):
   Prioritize Duet (**12.11%** median ER) and Stitch (**11.48%** median ER) on TikTok, and Live broadcasts on YouTube (**6.62%** median ER). Traditional static documents and text articles generate less than one-tenth of this engagement (**0.63% - 0.64%**).
2. **Reallocate Creator Budgets to Nano and Micro Tiers** (*Strong Confidence*):
   With an inverse correlation of $r = -0.602$, partnering with twenty Nano/Micro creators ($<50,000$ followers) yielding **19.31% - 95.39%** median ER provides vastly superior community engagement compared to a single Macro influencer (**1.93%** median ER).
3. **Impose Strict Caption Length Ceilings** (*Strong Confidence*):
   Restrict standard post captions to $\le 150$ characters (where median ER reaches **3.38% - 5.67%**). Avoid long-form text $300+$ characters (**2.26%** median ER) unless publishing specialized educational slides.
4. **Select Content Types Based on Specific Campaign Goals** (*Strong Confidence*):
   - **For Virality & Organic Distribution**: Deploy Tweets, Threads, or Polls (where shares account for **26.7% - 29.3%** of all engagements).
   - **For Content Retention & Recall**: Publish YouTube Shorts or Community Posts (saves comprise **20.8% - 22.8%** of engagements).
   - **For Surface-Level Brand Affinity**: Publish Carousels and Photos (likes comprise **78.0% - 78.7%** of engagements).
5. **Abandon Rigid Hourly/Daily Publishing Dogma** (*Strong Evidence of Null Effect*):
   Because day of week ($p = 0.617$) and hour of day ($p = 0.562$) show no statistically significant relationship with engagement rate, editorial teams should focus 100% of their bandwidth on creative format, hook brevity, and audience fit rather than rushing to meet an artificial "best hour to post."

---

## ⚠️ Limitations & Analytical Caveats

1. **Synthetic Data Origin**: The dataset was synthetically generated. Uniform distributions in posting timestamps and hashtag counts account for the null statistical findings in those categories. Conclusions should serve as comparative portfolio demonstrations rather than live commercial rules.
2. **Correlation vs. Causation**: Observational findings (e.g. short captions outperforming long captions) reflect correlation, not direct causation. Shorter captions may correlate with video formats that inherently drive higher engagement.
3. **Absence of Account / Brand Identifier**: Individual creators and brands cannot be benchmarked across multiple posts because the dataset lacks account usernames or handles.
4. **Missing Reach and Impression Telemetry**: Without true unique reach or impression metrics, engagement rates rely on follower counts, which inherently penalize larger legacy accounts.

---

## 🛠️ Tools & Technologies

- **Python 3.14**: Data cleaning, metric computation, statistical testing (`pandas`, `numpy`, `scipy`).
- **Interactive Dashboard**: `streamlit` (wide layout, dynamic metric cards, responsive layout), `plotly` (interactive charts).
- **Static Visualizations**: `matplotlib`, `seaborn` (300 DPI high-resolution figures).
- **Business Intelligence**: Power BI Desktop modeling blueprint and DAX measure framework (`powerbi/BUILD_GUIDE.md`).
- **Version Control**: Git & GitHub-ready repository architecture.

---

## 🚀 How to Run the Project

### 1. Environment Setup
Clone or enter the project directory and create a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # Windows
# source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 2. Run Data Pipeline & Export Analyses
Execute the automated analysis script to clean data, run tests, and regenerate output CSVs and charts:
```bash
python src/analysis.py
```

### 3. Launch the Streamlit Dashboard
Start the local interactive dashboard:
```bash
streamlit run dashboard/app.py
```
Open your browser at `http://localhost:8501`.

### 4. Independent Verification
Run the verification audit script to validate dashboard numbers against `output/clean_posts.csv`:
```bash
python scratch/verify_metrics.py
```

---

## 🤖 AI Disclosure
*Dashboard code, automated analysis scripts, and initial scaffolding were developed with an AI coding assistant and thoroughly reviewed, validated, and verified by the author.*
