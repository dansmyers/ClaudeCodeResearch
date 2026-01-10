"""
Data Processing Script for Billboard Artist Productivity Analysis

This script processes raw Billboard chart data to:
1. Filter to top-40 albums
2. Deduplicate to one entry per album
3. Exclude compilations, reissues, and deluxe editions
4. Identify qualifying artists (3+ top-40 albums)
5. Calculate productivity metrics
6. Assign decade cohorts
"""

import pandas as pd
import numpy as np
import re
from pathlib import Path

# Paths
RAW_DIR = Path('/home/user/ClaudeCodeResearch/data/raw')
PROCESSED_DIR = Path('/home/user/ClaudeCodeResearch/data/processed')

# Compilation/reissue patterns to exclude
EXCLUDE_PATTERNS = [
    r'\bgreatest\s+hits?\b',
    r'\bbest\s+of\b',
    r'\bhits\b.*\bcollection\b',
    r'\bcollected\b',
    r'\banthology\b',
    r'\bessential\b',
    r'\bultimate\b',
    r'\bcomplete\b.*\balbum',
    r'\bgold\b.*\bplatinum\b',
    r'\bremaster(ed)?\b',
    r'\bdeluxe\b.*\bedition\b',
    r'\bexpanded\b.*\bedition\b',
    r'\banniversary\b.*\bedition\b',
    r'\bspecial\b.*\bedition\b',
    r'\bcollector.?s?\b.*\bedition\b',
    r'\b20th\s+century\s+masters\b',
    r'\blegacy\b.*\bedition\b',
    r'\bdefinitive\b',
    r'\bvery\s+best\b',
    r'\ball[\s-]time\b.*\bhits\b',
    r'\bnumber\s+ones?\b',
    r'\b#1.?s\b',
    r'\bplatinum\b.*\bcollection\b',
    r'\bgold\b.*\bcollection\b',
    r'\bcompilation\b',
    r'\bsoundtrack\b',  # Exclude soundtracks as they're not studio albums
]

def is_likely_compilation(title):
    """Check if album title suggests it's a compilation/reissue."""
    title_lower = title.lower()
    for pattern in EXCLUDE_PATTERNS:
        if re.search(pattern, title_lower):
            return True
    return False

def process_chart_data(df, chart_name):
    """Process a single chart's data."""
    print(f"\n{'='*60}")
    print(f"Processing {chart_name}")
    print(f"{'='*60}")

    # Convert date
    df['chart_date'] = pd.to_datetime(df['chart_date'])

    print(f"Total chart entries: {len(df):,}")

    # Step 1: Filter to top-40 peak position
    df_top40 = df[df['peak_position'] <= 40].copy()
    print(f"After top-40 filter: {len(df_top40):,} entries")

    # Step 2: Deduplicate - keep first chart appearance per album/artist
    # Group by artist and title, take the row with earliest chart_date
    df_albums = df_top40.sort_values('chart_date').groupby(
        ['artist', 'title'], as_index=False
    ).first()

    print(f"Unique albums (after dedup): {len(df_albums):,}")
    print(f"Unique artists with top-40 albums: {df_albums['artist'].nunique():,}")

    # Step 3: Exclude compilations
    df_albums['is_compilation'] = df_albums['title'].apply(is_likely_compilation)
    compilations_removed = df_albums['is_compilation'].sum()
    df_albums = df_albums[~df_albums['is_compilation']].drop(columns=['is_compilation'])

    print(f"Compilations/soundtracks removed: {compilations_removed:,}")
    print(f"Albums after exclusions: {len(df_albums):,}")

    # Step 4: Calculate artist statistics
    artist_stats = df_albums.groupby('artist').agg(
        num_albums=('title', 'count'),
        first_hit_date=('chart_date', 'min'),
        last_hit_date=('chart_date', 'max'),
        albums_list=('title', list)
    ).reset_index()

    # Step 5: Filter to artists with 3+ albums
    qualifying_artists = artist_stats[artist_stats['num_albums'] >= 3].copy()
    print(f"Artists with 3+ top-40 albums: {len(qualifying_artists):,}")

    # Step 6: Calculate productivity metrics
    # Average gap = (last - first) / (num_albums - 1)
    qualifying_artists['career_span_days'] = (
        qualifying_artists['last_hit_date'] - qualifying_artists['first_hit_date']
    ).dt.days

    qualifying_artists['avg_gap_years'] = (
        qualifying_artists['career_span_days'] / 365.25 /
        (qualifying_artists['num_albums'] - 1)
    )

    # Step 7: Calculate hits in first 10 years
    # Need to go back to album-level data for this
    artist_first_hit = qualifying_artists[['artist', 'first_hit_date']].copy()
    albums_with_first = df_albums.merge(artist_first_hit, on='artist', suffixes=('', '_artist'))

    albums_with_first['years_since_first'] = (
        albums_with_first['chart_date'] - albums_with_first['first_hit_date']
    ).dt.days / 365.25

    hits_first_10 = albums_with_first[albums_with_first['years_since_first'] <= 10].groupby(
        'artist'
    ).size().reset_index(name='hits_first_10_years')

    qualifying_artists = qualifying_artists.merge(hits_first_10, on='artist', how='left')
    qualifying_artists['hits_first_10_years'] = qualifying_artists['hits_first_10_years'].fillna(0).astype(int)

    # Step 8: Assign decade cohort
    qualifying_artists['first_hit_year'] = qualifying_artists['first_hit_date'].dt.year
    qualifying_artists['decade_cohort'] = (qualifying_artists['first_hit_year'] // 10) * 10
    qualifying_artists['decade_cohort_label'] = qualifying_artists['decade_cohort'].astype(str) + 's'

    # Clean up columns
    result = qualifying_artists[[
        'artist', 'num_albums', 'first_hit_date', 'last_hit_date',
        'first_hit_year', 'decade_cohort', 'decade_cohort_label',
        'career_span_days', 'avg_gap_years', 'hits_first_10_years'
    ]].copy()

    print(f"\n{chart_name} - Cohort distribution:")
    print(result.groupby('decade_cohort_label').size().to_string())

    return result, df_albums

def main():
    # Process Billboard 200
    b200_raw = pd.read_csv(RAW_DIR / 'billboard_200.csv')
    b200_artists, b200_albums = process_chart_data(b200_raw, 'Billboard 200')

    # Process R&B/Hip-Hop Albums
    rnb_raw = pd.read_csv(RAW_DIR / 'rnb_hiphop_albums.csv')
    rnb_artists, rnb_albums = process_chart_data(rnb_raw, 'R&B/Hip-Hop Albums')

    # Save processed data
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)

    b200_artists.to_csv(PROCESSED_DIR / 'billboard_200_artists.csv', index=False)
    b200_albums.to_csv(PROCESSED_DIR / 'billboard_200_albums.csv', index=False)
    rnb_artists.to_csv(PROCESSED_DIR / 'rnb_hiphop_artists.csv', index=False)
    rnb_albums.to_csv(PROCESSED_DIR / 'rnb_hiphop_albums.csv', index=False)

    print(f"\n{'='*60}")
    print("Processing complete! Files saved to data/processed/")
    print(f"{'='*60}")

    # Summary statistics
    print("\n=== SUMMARY ===")
    print(f"\nBillboard 200:")
    print(f"  Qualifying artists: {len(b200_artists)}")
    print(f"  Total albums analyzed: {len(b200_albums)}")
    print(f"  Avg gap (mean): {b200_artists['avg_gap_years'].mean():.2f} years")
    print(f"  Hits in first 10 years (mean): {b200_artists['hits_first_10_years'].mean():.2f}")

    print(f"\nR&B/Hip-Hop Albums:")
    print(f"  Qualifying artists: {len(rnb_artists)}")
    print(f"  Total albums analyzed: {len(rnb_albums)}")
    print(f"  Avg gap (mean): {rnb_artists['avg_gap_years'].mean():.2f} years")
    print(f"  Hits in first 10 years (mean): {rnb_artists['hits_first_10_years'].mean():.2f}")

if __name__ == '__main__':
    main()
