# Research Execution Plan: Recording Artist Productivity Over Time

## Overview

This plan outlines the methodology for investigating whether successful recording artists have become less productive over time by analyzing Billboard chart data across three major charts.

---

## Phase 1: Data Acquisition

### 1.1 Data Sources

**Primary Charts to Analyze:**
| Chart | Description | Expected Time Range |
|-------|-------------|---------------------|
| Billboard 200 | Main album chart (all genres) | 1960s-present |
| Hot Country Albums | Country music albums | 1960s-present |
| Top R&B/Hip-Hop Albums | R&B and Hip-Hop albums | 1960s-present |

**Potential Data Sources:**
1. **Billboard.com** - Official source, may require web scraping or API access
2. **Wikipedia Billboard archives** - Historical chart data compilations
3. **MusicBrainz** - For album metadata and release dates
4. **Discogs API** - Album type classification (studio vs. compilation)
5. **Kaggle datasets** - Pre-compiled Billboard chart datasets
6. **data.world** - Community-shared music datasets

### 1.2 Data Collection Strategy

**Option A: Web Scraping (if APIs unavailable)**
- Build scrapers for Billboard chart archives
- Collect weekly chart positions and dates
- Rate-limit requests appropriately

**Option B: Existing Datasets**
- Search for pre-compiled Billboard datasets on Kaggle, data.world, or GitHub
- Validate dataset completeness and accuracy
- Supplement with additional scraping if needed

**Option C: API Access**
- Investigate Billboard API availability
- Use Spotify API for supplementary album metadata
- Use MusicBrainz API for album classification

### 1.3 Required Data Fields

For each chart entry:
- Album title
- Artist name (standardized)
- Peak chart position
- Entry date / chart week
- Album type (studio, live, compilation, reissue, deluxe)
- Release date

---

## Phase 2: Data Processing

### 2.1 Data Cleaning

1. **Artist Name Standardization**
   - Handle variations (e.g., "Prince" vs "Prince & The Revolution")
   - Decide on featuring artists (include or exclude)
   - Create artist ID mapping

2. **Album Deduplication**
   - Identify and merge duplicate entries (recharting albums)
   - Use earliest chart appearance for dating

3. **Album Type Classification**
   - Categorize albums as: studio, live, compilation, reissue, deluxe
   - **Include**: Original studio albums, live albums
   - **Exclude**: Compilations, greatest hits, reissues, deluxe editions, EPs

### 2.2 Filtering Criteria

```
For each chart separately:
  Filter to albums with peak position <= 40
  Group by artist
  Keep artists where:
    - count(qualifying_albums) >= 3
    - min(first_hit_date).year <= 2022
```

### 2.3 Artist-Level Calculations

For each qualifying artist on each chart:

| Metric | Formula |
|--------|---------|
| First Hit Date | Date of first top-40 album |
| Last Hit Date | Date of most recent top-40 album |
| Total Hits | Count of top-40 albums |
| Career Span | Last Hit Date - First Hit Date |
| Avg Gap Between Hits | Career Span / (Total Hits - 1) |
| Hits in First 10 Years | Count where album_date <= first_hit_date + 10 years |
| Decade Cohort | Decade of first hit (1960s, 1970s, etc.) |

---

## Phase 3: Analysis

### 3.1 Cohort Aggregation

For each chart and decade cohort, calculate:
- Number of artists in cohort
- Mean average gap between hits
- Median average gap between hits
- Mean hits in first 10 years
- Median hits in first 10 years
- Standard deviation for each metric

### 3.2 Statistical Tests

- **Trend Analysis**: Linear regression of metrics over cohort decades
- **Significance Testing**: ANOVA or Kruskal-Wallis across cohorts
- **Effect Size**: Calculate to assess practical significance

---

## Phase 4: Visualization

### 4.1 Required Visualizations (6 total, 2 per chart)

**For each of the 3 charts:**

1. **Average Gap Between Hits by Decade Cohort**
   - Bar chart or box plot
   - X-axis: Decade cohort (1960s-2020s)
   - Y-axis: Average gap in years
   - Include error bars or quartile ranges
   - Annotate sample size per cohort

2. **Hit Albums in First 10 Years by Decade Cohort**
   - Bar chart or box plot
   - X-axis: Decade cohort (1960s-2020s)
   - Y-axis: Number of hit albums
   - Include error bars or quartile ranges
   - Annotate sample size per cohort

### 4.2 Supplementary Visualizations (Optional)

- Scatter plots of individual artist data points
- Trend lines overlaid on cohort summaries
- Comparison across all three charts on single figure
- Sample size / data coverage over time

---

## Phase 5: Reporting

### 5.1 Methodology Summary
- Data sources used
- Time period covered
- Sample sizes achieved
- Filtering and classification criteria

### 5.2 Findings by Chart

For each chart:
- Cohort statistics table
- Key visualizations
- Observed trends
- Notable outliers

### 5.3 Cross-Chart Comparison
- Similarities and differences across genres
- Overall productivity trend assessment

### 5.4 Limitations and Caveats

Document the following:
1. **Data Limitations**
   - Missing historical data
   - Album classification accuracy
   - Chart methodology changes over time

2. **Methodological Caveats**
   - Survivorship bias (only analyzing artists who achieved hits)
   - Censoring issues for recent cohorts (2010s/2020s haven't had 10 years yet)
   - Artist name disambiguation challenges
   - Definition of "original album" vs. variants

3. **Interpretation Considerations**
   - Industry changes (streaming era, album bundles)
   - Changing role of albums in music consumption
   - Economic factors affecting release strategies

---

## Implementation Timeline

### Step 1: Data Source Investigation
- Research available Billboard datasets
- Evaluate API options
- Determine scraping feasibility

### Step 2: Data Collection
- Acquire chart data for all three charts
- Collect album metadata for classification

### Step 3: Data Processing
- Clean and standardize data
- Classify albums by type
- Filter to qualifying artists

### Step 4: Analysis
- Calculate productivity metrics
- Aggregate by cohort
- Perform statistical tests

### Step 5: Visualization
- Create required charts (6 minimum)
- Generate supplementary visuals

### Step 6: Documentation
- Write methodology section
- Document findings
- Discuss limitations

---

## Technical Requirements

### Tools and Libraries

**Python (Recommended)**
```
pandas          # Data manipulation
numpy           # Numerical operations
matplotlib      # Basic plotting
seaborn         # Statistical visualization
requests        # API/web requests
beautifulsoup4  # Web scraping (if needed)
scipy           # Statistical tests
```

**Alternative: R**
```
tidyverse       # Data manipulation and visualization
ggplot2         # Plotting
lubridate       # Date handling
```

### File Structure

```
ClaudeCodeResearch/
├── claude.md              # Original research prompt
├── research_plan.md       # This plan
├── data/
│   ├── raw/               # Original data files
│   └── processed/         # Cleaned data files
├── scripts/
│   ├── collect_data.py    # Data collection scripts
│   ├── process_data.py    # Data cleaning and filtering
│   ├── analyze.py         # Metric calculations
│   └── visualize.py       # Chart generation
├── output/
│   ├── figures/           # Generated visualizations
│   └── tables/            # Summary statistics
└── report/
    └── findings.md        # Final research report
```

---

## Key Decisions Needed

1. **Data Source Selection**: Which Billboard data source provides the best coverage?
2. **Artist Disambiguation**: How to handle artist name variations and collaborations?
3. **Album Classification**: Manual review vs. automated classification for album types?
4. **Cohort Handling for 2020s**: Include with caveat or exclude due to incomplete data?

---

## Success Criteria

The research will be considered successful if:
- [ ] Data collected for all three charts with reasonable historical coverage
- [ ] At least 50+ qualifying artists per chart
- [ ] Both productivity metrics calculated for all qualifying artists
- [ ] 6 visualizations created (2 per chart)
- [ ] Trends identified and statistical significance assessed
- [ ] Limitations clearly documented

---

## Next Steps

1. Begin data source investigation - search for existing Billboard datasets
2. Evaluate the most feasible data collection approach
3. Start with one chart (Billboard 200) as proof of concept
4. Expand to other charts once pipeline is validated
