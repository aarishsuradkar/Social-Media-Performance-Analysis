# Dashboard Visual Captures & Verification Views

This folder contains automated and recommended visual captures of the interactive Streamlit dashboard (`dashboard/app.py`).

## Captured & Recommended Views

### 1. Tab 1: Overview & Longitudinal Trends (`01_tab_overview.png`)
- **Key Visual Elements**:
  - Executive KPI cards: Total Posts (5,000), Total Engagement (47,325,606), Robust Median Engagement Rate (2.57%), Mean Engagement Rate (12.87%).
  - Platform Performance Bar Chart: Visualizing median engagement rate across TikTok (11.62%), YouTube (5.24%), Instagram (2.33%), Facebook (2.16%), Twitter (1.52%), and LinkedIn (0.63%).
  - Dynamic code-generated insight callout highlighting TikTok's dominance.
  - 24-Month Longitudinal Trend: Dual-axis Plotly chart displaying monthly median engagement rates alongside post publication volumes.

### 2. Tab 2: Content Formats & Text Optimization (`02_tab_content.png`)
- **Key Visual Elements**:
  - Content Format Ranking: Horizontal bar chart comparing 17 distinct formats, highlighting Duet (12.11%) and Stitch (11.48%) vs Article (0.64%) and Document (0.63%).
  - Hashtag Count Bar Chart: Depicting uniform medians across 0-29 hashtags, corroborating the null correlation (r = -0.007, p = 0.608).
  - Caption Length Bucket Comparison: Showing the sharp decline in median engagement rate from ultra-short copy <=50 characters (5.67%) to lengthy posts 300+ characters (2.26%).

### 3. Tab 3: Timing Matrix & Benchmarks (`03_tab_timing_benchmarks.png`)
- **Key Visual Elements**:
  - Day of Week × Hour of Day Heatmap: 7x24 grid illustrating median engagement rates across every hour/day window (highlighting lack of statistical timing effect).
  - Influencer Scale / Tier Benchmark: Visual proof of the audience size inverse power law (Nano: 95.39% vs Macro: 1.93%).
  - Category Peer Benchmark: 12-niche comparison led by Gaming (2.88%) and Entertainment (2.87%).
  - Top 25 Posts Table: Interactive data view with CSV export functionality.

### 4. Interactive Slicer Demonstration (`04_filtered_view.png`)
- **Key Visual Elements**:
  - Slicers set to `Platform = TikTok` and `Influencer_Tier = Micro`.
  - Dynamic KPI cards recomputing automatically in real-time.

## Instructions for High-DPI Manual Captures
1. Launch the local Streamlit server:
   ```bash
   streamlit run dashboard/app.py
   ```
2. Navigate to `http://localhost:8501` in your browser.
3. Switch between each of the three tabs ("Overview & Trends", "Content & Formats", "Timing & Benchmarks").
4. Take full-resolution browser screenshots (e.g. using browser developer tools: `Ctrl+Shift+P` -> "Capture full size screenshot") and save them directly into this folder.
