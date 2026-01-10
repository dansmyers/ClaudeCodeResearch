# Raw Data Sources

## Source Repository
Data downloaded from: https://github.com/pdp2600/chartscraper

## Files

### billboard_200.csv
- **Original filename**: `All_Billboard_200_from_1963-08-17_to_2018-12-31.csv`
- **Date range**: 1963-08-17 to 2018-12-29
- **Total rows**: 568,546
- **Unique artists**: 9,669
- **Unique albums**: 32,998
- **Chart positions**: 1-200

### rnb_hiphop_albums.csv
- **Original filename**: `All_Hip_Hop_Albums_from_1965-01-30_to_2018-12-31.csv`
- **Date range**: 1965-01-30 to 2018-12-29
- **Total rows**: 135,829
- **Unique artists**: 3,173
- **Unique albums**: 9,167
- **Chart positions**: 1-50 (varies by era, up to 75 in 1980s)

## Column Descriptions
| Column | Description |
|--------|-------------|
| ranking | Position on chart for that week |
| artist | Artist name |
| title | Album title |
| last_week_rank | Previous week's position (0 = new entry) |
| peak_position | Highest position achieved |
| weeks_on_chart | Cumulative weeks on chart |
| chart_date | Date of chart (YYYY-MM-DD) |

## Notes
- Data ends in December 2018
- Country Albums chart not included (deferred for later)
- Post-2018 data not included (deferred for later)
