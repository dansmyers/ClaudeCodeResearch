"""
Analysis and Visualization Script for Billboard Artist Productivity Study

This script:
1. Aggregates productivity metrics by decade cohort
2. Performs statistical tests for trends
3. Creates visualizations for each chart
4. Outputs summary tables
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

# Paths
PROCESSED_DIR = Path('/home/user/ClaudeCodeResearch/data/processed')
FIGURES_DIR = Path('/home/user/ClaudeCodeResearch/output/figures')
TABLES_DIR = Path('/home/user/ClaudeCodeResearch/output/tables')

# Ensure output directories exist
FIGURES_DIR.mkdir(parents=True, exist_ok=True)
TABLES_DIR.mkdir(parents=True, exist_ok=True)

# Set style
plt.style.use('seaborn-v0_8-whitegrid')
sns.set_palette("husl")

def load_data():
    """Load processed artist data."""
    b200 = pd.read_csv(PROCESSED_DIR / 'billboard_200_artists.csv')
    rnb = pd.read_csv(PROCESSED_DIR / 'rnb_hiphop_artists.csv')
    return b200, rnb

def compute_cohort_stats(df, metric_col):
    """Compute statistics by decade cohort for a given metric."""
    stats_df = df.groupby('decade_cohort_label').agg(
        n=('artist', 'count'),
        mean=(metric_col, 'mean'),
        median=(metric_col, 'median'),
        std=(metric_col, 'std'),
        q25=(metric_col, lambda x: x.quantile(0.25)),
        q75=(metric_col, lambda x: x.quantile(0.75))
    ).reset_index()

    # Sort by decade
    stats_df['sort_key'] = stats_df['decade_cohort_label'].str[:4].astype(int)
    stats_df = stats_df.sort_values('sort_key').drop(columns=['sort_key'])

    return stats_df

def test_trend(df, metric_col):
    """Test for linear trend across decades using Spearman correlation."""
    # Use decade as numeric for correlation
    result = stats.spearmanr(df['decade_cohort'], df[metric_col])
    return result.correlation, result.pvalue

def create_boxplot(df, metric_col, ylabel, title, filename, chart_name):
    """Create a box plot showing metric distribution by decade cohort."""
    fig, ax = plt.subplots(figsize=(10, 6))

    # Sort decades
    decade_order = sorted(df['decade_cohort_label'].unique(),
                          key=lambda x: int(x[:4]))

    # Create boxplot
    box = sns.boxplot(
        data=df,
        x='decade_cohort_label',
        y=metric_col,
        order=decade_order,
        ax=ax,
        palette='Blues_d'
    )

    # Add sample sizes
    cohort_counts = df.groupby('decade_cohort_label').size()
    for i, decade in enumerate(decade_order):
        n = cohort_counts.get(decade, 0)
        ax.text(i, ax.get_ylim()[1], f'n={n}', ha='center', va='bottom', fontsize=9)

    ax.set_xlabel('Decade of First Hit', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f'{chart_name}: {title}', fontsize=14, fontweight='bold')

    # Add trend line (median by decade)
    medians = df.groupby('decade_cohort_label')[metric_col].median()
    medians = medians.reindex(decade_order)
    ax.plot(range(len(decade_order)), medians.values, 'ro-',
            linewidth=2, markersize=8, label='Median')
    ax.legend(loc='upper right')

    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")

def create_bar_chart(stats_df, metric_name, ylabel, title, filename, chart_name):
    """Create a bar chart with error bars showing cohort statistics."""
    fig, ax = plt.subplots(figsize=(10, 6))

    x = range(len(stats_df))
    bars = ax.bar(x, stats_df['mean'],
                  yerr=[stats_df['mean'] - stats_df['q25'],
                        stats_df['q75'] - stats_df['mean']],
                  capsize=5, color='steelblue', alpha=0.8)

    # Add median markers
    ax.scatter(x, stats_df['median'], color='red', s=100, zorder=5,
               label='Median', marker='_', linewidths=3)

    ax.set_xticks(x)
    ax.set_xticklabels(stats_df['decade_cohort_label'])
    ax.set_xlabel('Decade of First Hit', fontsize=12)
    ax.set_ylabel(ylabel, fontsize=12)
    ax.set_title(f'{chart_name}: {title}', fontsize=14, fontweight='bold')

    # Add sample sizes
    for i, (_, row) in enumerate(stats_df.iterrows()):
        ax.text(i, ax.get_ylim()[0] - 0.05 * (ax.get_ylim()[1] - ax.get_ylim()[0]),
                f'n={int(row["n"])}', ha='center', va='top', fontsize=9)

    ax.legend(loc='upper right')
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / filename, dpi=150, bbox_inches='tight')
    plt.close()
    print(f"  Saved: {filename}")

def analyze_chart(df, chart_name, prefix):
    """Run full analysis for a single chart."""
    print(f"\n{'='*60}")
    print(f"Analyzing: {chart_name}")
    print(f"{'='*60}")

    # Compute cohort statistics for both metrics
    gap_stats = compute_cohort_stats(df, 'avg_gap_years')
    hits_stats = compute_cohort_stats(df, 'hits_first_10_years')

    print(f"\nAverage Gap Between Hits (years) by Cohort:")
    print(gap_stats.to_string(index=False))

    print(f"\nHits in First 10 Years by Cohort:")
    print(hits_stats.to_string(index=False))

    # Statistical tests
    gap_corr, gap_pval = test_trend(df, 'avg_gap_years')
    hits_corr, hits_pval = test_trend(df, 'hits_first_10_years')

    print(f"\nTrend Analysis (Spearman correlation with decade):")
    print(f"  Avg Gap: r = {gap_corr:.3f}, p = {gap_pval:.4f}")
    print(f"  Hits in 10 Years: r = {hits_corr:.3f}, p = {hits_pval:.4f}")

    # Create visualizations
    print(f"\nGenerating visualizations...")

    create_boxplot(
        df, 'avg_gap_years',
        'Average Years Between Hit Albums',
        'Average Gap Between Hits by Decade Cohort',
        f'{prefix}_avg_gap_boxplot.png',
        chart_name
    )

    create_boxplot(
        df, 'hits_first_10_years',
        'Number of Hit Albums',
        'Hit Albums in First 10 Years by Decade Cohort',
        f'{prefix}_hits_10yr_boxplot.png',
        chart_name
    )

    # Save statistics tables
    gap_stats.to_csv(TABLES_DIR / f'{prefix}_avg_gap_stats.csv', index=False)
    hits_stats.to_csv(TABLES_DIR / f'{prefix}_hits_10yr_stats.csv', index=False)

    return {
        'chart': chart_name,
        'n_artists': len(df),
        'gap_stats': gap_stats,
        'hits_stats': hits_stats,
        'gap_trend': (gap_corr, gap_pval),
        'hits_trend': (hits_corr, hits_pval)
    }

def create_comparison_figure(b200_df, rnb_df):
    """Create a combined comparison figure for both charts."""
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    decade_order = ['1960s', '1970s', '1980s', '1990s', '2000s', '2010s']

    for col, (df, name, color) in enumerate([
        (b200_df, 'Billboard 200', 'Blues_d'),
        (rnb_df, 'R&B/Hip-Hop Albums', 'Oranges_d')
    ]):
        # Top row: Average gap
        ax = axes[0, col]
        available_decades = [d for d in decade_order if d in df['decade_cohort_label'].values]
        sns.boxplot(data=df, x='decade_cohort_label', y='avg_gap_years',
                    order=available_decades, ax=ax, palette=color)
        ax.set_xlabel('Decade of First Hit')
        ax.set_ylabel('Avg Years Between Hits')
        ax.set_title(f'{name}: Gap Between Hits')

        # Bottom row: Hits in 10 years
        ax = axes[1, col]
        sns.boxplot(data=df, x='decade_cohort_label', y='hits_first_10_years',
                    order=available_decades, ax=ax, palette=color)
        ax.set_xlabel('Decade of First Hit')
        ax.set_ylabel('Hit Albums')
        ax.set_title(f'{name}: Hits in First 10 Years')

    plt.suptitle('Artist Productivity by Decade Cohort', fontsize=16, fontweight='bold', y=1.02)
    plt.tight_layout()
    plt.savefig(FIGURES_DIR / 'combined_comparison.png', dpi=150, bbox_inches='tight')
    plt.close()
    print(f"\nSaved: combined_comparison.png")

def main():
    # Load data
    b200, rnb = load_data()

    # Analyze each chart
    b200_results = analyze_chart(b200, 'Billboard 200', 'billboard_200')
    rnb_results = analyze_chart(rnb, 'R&B/Hip-Hop Albums', 'rnb_hiphop')

    # Create comparison figure
    print("\nGenerating comparison figure...")
    create_comparison_figure(b200, rnb)

    # Summary
    print(f"\n{'='*60}")
    print("ANALYSIS COMPLETE")
    print(f"{'='*60}")
    print(f"\nFigures saved to: {FIGURES_DIR}")
    print(f"Tables saved to: {TABLES_DIR}")

    print("\n=== KEY FINDINGS ===")
    for results in [b200_results, rnb_results]:
        print(f"\n{results['chart']} ({results['n_artists']} artists):")
        gap_corr, gap_pval = results['gap_trend']
        hits_corr, hits_pval = results['hits_trend']

        gap_direction = "increasing" if gap_corr > 0 else "decreasing"
        hits_direction = "increasing" if hits_corr > 0 else "decreasing"
        gap_sig = "significant" if gap_pval < 0.05 else "not significant"
        hits_sig = "significant" if hits_pval < 0.05 else "not significant"

        print(f"  - Avg gap between hits: {gap_direction} trend ({gap_sig}, r={gap_corr:.3f})")
        print(f"  - Hits in first 10 years: {hits_direction} trend ({hits_sig}, r={hits_corr:.3f})")

if __name__ == '__main__':
    main()
