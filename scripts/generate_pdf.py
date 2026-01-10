"""
Generate PDF report with embedded figures for the Artist Productivity Study.
"""

import markdown
from weasyprint import HTML, CSS
from pathlib import Path
import base64

# Paths
OUTPUT_DIR = Path('/home/user/ClaudeCodeResearch/output')
FIGURES_DIR = OUTPUT_DIR / 'figures'

def image_to_base64(image_path):
    """Convert image to base64 for embedding in HTML."""
    with open(image_path, 'rb') as f:
        return base64.b64encode(f.read()).decode('utf-8')

def create_html_report():
    """Create HTML report with embedded figures."""

    # Get base64 encoded images
    b200_gap = image_to_base64(FIGURES_DIR / 'billboard_200_avg_gap_boxplot.png')
    b200_hits = image_to_base64(FIGURES_DIR / 'billboard_200_hits_10yr_boxplot.png')
    rnb_gap = image_to_base64(FIGURES_DIR / 'rnb_hiphop_avg_gap_boxplot.png')
    rnb_hits = image_to_base64(FIGURES_DIR / 'rnb_hiphop_hits_10yr_boxplot.png')
    combined = image_to_base64(FIGURES_DIR / 'combined_comparison.png')

    html_content = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Recording Artist Productivity Over Time</title>
    <style>
        @page {{
            size: letter;
            margin: 1in;
        }}
        body {{
            font-family: 'Helvetica Neue', Arial, sans-serif;
            font-size: 11pt;
            line-height: 1.5;
            color: #333;
            max-width: 100%;
        }}
        h1 {{
            color: #1a1a2e;
            font-size: 24pt;
            border-bottom: 3px solid #4a4a6a;
            padding-bottom: 10px;
            margin-top: 0;
        }}
        h2 {{
            color: #2d2d4a;
            font-size: 16pt;
            margin-top: 30px;
            border-bottom: 1px solid #ccc;
            padding-bottom: 5px;
        }}
        h3 {{
            color: #3d3d5a;
            font-size: 13pt;
            margin-top: 20px;
        }}
        h4 {{
            color: #4d4d6a;
            font-size: 11pt;
            margin-top: 15px;
        }}
        table {{
            border-collapse: collapse;
            width: 100%;
            margin: 15px 0;
            font-size: 10pt;
        }}
        th, td {{
            border: 1px solid #ddd;
            padding: 8px;
            text-align: left;
        }}
        th {{
            background-color: #4a4a6a;
            color: white;
        }}
        tr:nth-child(even) {{
            background-color: #f9f9f9;
        }}
        .figure {{
            text-align: center;
            margin: 25px 0;
            page-break-inside: avoid;
        }}
        .figure img {{
            max-width: 100%;
            height: auto;
        }}
        .figure-caption {{
            font-style: italic;
            color: #666;
            margin-top: 8px;
            font-size: 10pt;
        }}
        .executive-summary {{
            background-color: #f5f5f5;
            padding: 20px;
            border-left: 4px solid #4a4a6a;
            margin: 20px 0;
        }}
        .key-finding {{
            background-color: #e8f4e8;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        .limitation {{
            background-color: #fff8e8;
            padding: 15px;
            border-radius: 5px;
            margin: 15px 0;
        }}
        ul, ol {{
            margin-left: 20px;
        }}
        li {{
            margin-bottom: 5px;
        }}
        .page-break {{
            page-break-before: always;
        }}
        .stat-highlight {{
            font-weight: bold;
            color: #2d5a2d;
        }}
    </style>
</head>
<body>

<h1>Recording Artist Productivity Over Time</h1>
<p style="font-size: 12pt; color: #666;">Research Findings Report | January 2026</p>

<div class="executive-summary">
<h2 style="margin-top: 0; border: none;">Executive Summary</h2>
<p>This study analyzed Billboard chart data to investigate whether successful recording artists have become less productive over time. Using data from the Billboard 200 and Top R&B/Hip-Hop Albums charts (1963-2018), we found <strong>mixed evidence</strong> regarding productivity trends:</p>
<ul>
    <li><strong>Artists are producing fewer hit albums in their first 10 years</strong> — This trend is statistically significant for both charts</li>
    <li><strong>The gap between hit albums has not clearly increased</strong> — Results differ by chart, with no significant trend for Billboard 200 and a weak increasing trend for R&B/Hip-Hop</li>
</ul>
</div>

<h2>Methodology</h2>

<h3>Data Sources</h3>
<ul>
    <li><strong>Billboard 200</strong>: Weekly chart data from August 1963 to December 2018</li>
    <li><strong>Top R&B/Hip-Hop Albums</strong>: Weekly chart data from January 1965 to December 2018</li>
    <li>Source: github.com/pdp2600/chartscraper</li>
</ul>

<h3>Artist Selection Criteria</h3>
<p>Artists were included if they:</p>
<ol>
    <li>Had at least 3 albums reach the top 40 on the respective chart</li>
    <li>Released their first top-40 album in 2018 or earlier</li>
</ol>

<p>Albums were filtered to exclude:</p>
<ul>
    <li>Greatest hits compilations</li>
    <li>Best-of collections and anthologies</li>
    <li>Soundtracks</li>
    <li>Remastered/deluxe/anniversary editions</li>
</ul>

<h3>Productivity Measures</h3>
<ol>
    <li><strong>Average gap between hits</strong>: (date of last hit − date of first hit) / (number of hit albums − 1)</li>
    <li><strong>Hit albums in first 10 years</strong>: Count of top-40 albums released within 10 years of artist's first hit</li>
</ol>

<h3>Cohort Assignment</h3>
<p>Artists were grouped by the decade of their first top-40 album (1960s, 1970s, 1980s, 1990s, 2000s, 2010s).</p>

<h2>Sample Characteristics</h2>

<table>
    <tr>
        <th>Chart</th>
        <th>Qualifying Artists</th>
        <th>Total Albums Analyzed</th>
    </tr>
    <tr>
        <td>Billboard 200</td>
        <td>1,359</td>
        <td>12,088</td>
    </tr>
    <tr>
        <td>R&B/Hip-Hop Albums</td>
        <td>881</td>
        <td>8,161</td>
    </tr>
</table>

<h3>Cohort Distribution</h3>
<table>
    <tr>
        <th>Decade</th>
        <th>Billboard 200</th>
        <th>R&B/Hip-Hop</th>
    </tr>
    <tr><td>1960s</td><td>140</td><td>95</td></tr>
    <tr><td>1970s</td><td>234</td><td>169</td></tr>
    <tr><td>1980s</td><td>146</td><td>124</td></tr>
    <tr><td>1990s</td><td>248</td><td>213</td></tr>
    <tr><td>2000s</td><td>416</td><td>176</td></tr>
    <tr><td>2010s</td><td>175</td><td>104</td></tr>
</table>

<div class="page-break"></div>

<h2>Results</h2>

<h3>Overview: Both Charts Compared</h3>

<div class="figure">
    <img src="data:image/png;base64,{combined}" alt="Combined Comparison">
    <p class="figure-caption">Figure 1: Artist productivity metrics across decade cohorts for both charts. Top row shows average years between hit albums; bottom row shows number of hit albums in first 10 years of career.</p>
</div>

<div class="page-break"></div>

<h3>Measure 1: Average Gap Between Hits</h3>

<h4>Billboard 200</h4>

<table>
    <tr>
        <th>Decade</th>
        <th>N</th>
        <th>Mean (years)</th>
        <th>Median (years)</th>
    </tr>
    <tr><td>1960s</td><td>140</td><td>2.16</td><td>1.21</td></tr>
    <tr><td>1970s</td><td>234</td><td>3.01</td><td>1.89</td></tr>
    <tr><td>1980s</td><td>146</td><td>3.73</td><td>2.77</td></tr>
    <tr><td>1990s</td><td>248</td><td>3.15</td><td>2.61</td></tr>
    <tr><td>2000s</td><td>416</td><td>2.57</td><td>2.44</td></tr>
    <tr><td>2010s</td><td>175</td><td>1.76</td><td>1.69</td></tr>
</table>

<p><strong>Trend</strong>: No significant linear trend (Spearman r = 0.026, p = 0.342)</p>

<div class="figure">
    <img src="data:image/png;base64,{b200_gap}" alt="Billboard 200 Average Gap">
    <p class="figure-caption">Figure 2: Distribution of average gap between hit albums by decade cohort (Billboard 200). Red line shows median trend.</p>
</div>

<h4>R&B/Hip-Hop Albums</h4>

<table>
    <tr>
        <th>Decade</th>
        <th>N</th>
        <th>Mean (years)</th>
        <th>Median (years)</th>
    </tr>
    <tr><td>1960s</td><td>95</td><td>2.05</td><td>1.17</td></tr>
    <tr><td>1970s</td><td>169</td><td>2.08</td><td>1.43</td></tr>
    <tr><td>1980s</td><td>124</td><td>2.71</td><td>2.11</td></tr>
    <tr><td>1990s</td><td>213</td><td>3.02</td><td>2.66</td></tr>
    <tr><td>2000s</td><td>176</td><td>2.51</td><td>2.24</td></tr>
    <tr><td>2010s</td><td>104</td><td>1.46</td><td>1.36</td></tr>
</table>

<p><strong>Trend</strong>: Weak but significant increasing trend (Spearman r = 0.129, p = 0.0001)</p>

<div class="figure">
    <img src="data:image/png;base64,{rnb_gap}" alt="R&B/Hip-Hop Average Gap">
    <p class="figure-caption">Figure 3: Distribution of average gap between hit albums by decade cohort (R&B/Hip-Hop Albums). Red line shows median trend.</p>
</div>

<div class="page-break"></div>

<h3>Measure 2: Hit Albums in First 10 Years</h3>

<h4>Billboard 200</h4>

<table>
    <tr>
        <th>Decade</th>
        <th>N</th>
        <th>Mean</th>
        <th>Median</th>
    </tr>
    <tr><td>1960s</td><td>140</td><td>7.05</td><td>5.0</td></tr>
    <tr><td>1970s</td><td>234</td><td>5.16</td><td>5.0</td></tr>
    <tr><td>1980s</td><td>146</td><td>3.84</td><td>4.0</td></tr>
    <tr><td>1990s</td><td>248</td><td>4.29</td><td>4.0</td></tr>
    <tr><td>2000s</td><td>416</td><td>4.32</td><td>4.0</td></tr>
    <tr><td>2010s</td><td>175</td><td>3.71</td><td>3.0</td></tr>
</table>

<p><strong>Trend</strong>: <span class="stat-highlight">Significant decreasing trend (Spearman r = −0.228, p &lt; 0.0001)</span></p>

<div class="figure">
    <img src="data:image/png;base64,{b200_hits}" alt="Billboard 200 Hits in 10 Years">
    <p class="figure-caption">Figure 4: Distribution of hit albums in first 10 years by decade cohort (Billboard 200). Red line shows median trend.</p>
</div>

<h4>R&B/Hip-Hop Albums</h4>

<table>
    <tr>
        <th>Decade</th>
        <th>N</th>
        <th>Mean</th>
        <th>Median</th>
    </tr>
    <tr><td>1960s</td><td>95</td><td>7.71</td><td>6.0</td></tr>
    <tr><td>1970s</td><td>169</td><td>6.00</td><td>5.0</td></tr>
    <tr><td>1980s</td><td>124</td><td>3.96</td><td>4.0</td></tr>
    <tr><td>1990s</td><td>213</td><td>4.13</td><td>4.0</td></tr>
    <tr><td>2000s</td><td>176</td><td>4.43</td><td>4.0</td></tr>
    <tr><td>2010s</td><td>104</td><td>3.90</td><td>4.0</td></tr>
</table>

<p><strong>Trend</strong>: <span class="stat-highlight">Significant decreasing trend (Spearman r = −0.246, p &lt; 0.0001)</span></p>

<div class="figure">
    <img src="data:image/png;base64,{rnb_hits}" alt="R&B/Hip-Hop Hits in 10 Years">
    <p class="figure-caption">Figure 5: Distribution of hit albums in first 10 years by decade cohort (R&B/Hip-Hop Albums). Red line shows median trend.</p>
</div>

<div class="page-break"></div>

<h2>Key Findings</h2>

<div class="key-finding">
<h3 style="margin-top: 0;">1. Artists produce fewer hit albums early in their careers</h3>
<p>Both charts show a clear decline in the number of top-40 albums artists achieve in their first 10 years. 1960s artists averaged nearly <strong>twice as many</strong> early hits as 2010s artists.</p>
</div>

<div class="key-finding">
<h3 style="margin-top: 0;">2. The gap between hits shows no clear long-term trend</h3>
<p>While both charts show gaps peaked in the 1980s-1990s and have since declined, there is no consistent long-term increase. Recent cohorts actually show the <strong>shortest gaps</strong> between hits.</p>
</div>

<div class="key-finding">
<h3 style="margin-top: 0;">3. Patterns are consistent across charts</h3>
<p>The Billboard 200 (all genres) and R&B/Hip-Hop Albums chart show remarkably similar patterns, suggesting these trends reflect <strong>industry-wide changes</strong> rather than genre-specific factors.</p>
</div>

<div class="key-finding">
<h3 style="margin-top: 0;">4. Recent cohorts appear more productive (with caveats)</h3>
<p>The 2010s cohort shows short gaps between hits, but this likely reflects <strong>survivorship bias</strong>—we only observe artists who achieved 3+ hits quickly, as slower artists haven't had time to qualify.</p>
</div>

<h2>Limitations and Caveats</h2>

<div class="limitation">
<h3 style="margin-top: 0;">Data Limitations</h3>
<ul>
    <li><strong>Temporal cutoff</strong>: Data ends in December 2018, limiting analysis of 2010s artists and excluding 2020s entirely</li>
    <li><strong>Album classification</strong>: Compilation identification relied on title pattern matching; some errors are likely</li>
    <li><strong>Missing Country Albums data</strong>: The Hot Country Albums chart was not analyzed due to lack of available historical data</li>
    <li><strong>Chart methodology changes</strong>: Billboard has changed its methodology multiple times, which may affect comparability across eras</li>
</ul>
</div>

<div class="limitation">
<h3 style="margin-top: 0;">Methodological Caveats</h3>
<ul>
    <li><strong>Survivorship bias</strong>: Analysis only includes artists who achieved 3+ top-40 albums; less successful artists are excluded</li>
    <li><strong>Censoring for recent cohorts</strong>: 2010s artists have only had 0-8 years since first appearing; many haven't had opportunity for full 10-year measurement</li>
    <li><strong>Artist disambiguation</strong>: Artists with name variations may be counted multiple times or have albums misattributed</li>
</ul>
</div>

<div class="limitation">
<h3 style="margin-top: 0;">Interpretation Considerations</h3>
<ul>
    <li><strong>Industry changes</strong>: Album release strategies have evolved (1960s-70s: 1-2 albums/year common; modern era: 2-4 year cycles standard)</li>
    <li><strong>Album definition evolution</strong>: What constitutes an "album" has changed (mixtapes, EPs, deluxe editions)</li>
    <li><strong>Chart access changes</strong>: Eligibility rules have changed over time</li>
</ul>
</div>

<h2>Conclusions</h2>

<p>The data provides <strong>partial support</strong> for the hypothesis that artists have become less productive:</p>

<ul>
    <li><strong>Supported</strong>: Artists clearly produce fewer hit albums in their first 10 years compared to earlier decades</li>
    <li><strong>Not supported</strong>: The gap between hit albums has not consistently increased; if anything, recent cohorts show shorter gaps</li>
</ul>

<p>The decline in early-career hits is substantial and statistically robust. However, interpretation is complicated by changing industry dynamics, chart methodology, and the inherent limitations of analyzing recent cohorts with incomplete career data.</p>

<p style="margin-top: 30px; padding-top: 20px; border-top: 1px solid #ccc; font-size: 10pt; color: #666;">
<strong>Data source:</strong> github.com/pdp2600/chartscraper<br>
<strong>Analysis completed:</strong> January 2026
</p>

</body>
</html>
"""
    return html_content

def main():
    print("Generating PDF report...")

    # Create HTML content
    html_content = create_html_report()

    # Save HTML for reference
    html_path = OUTPUT_DIR / 'findings_report.html'
    with open(html_path, 'w') as f:
        f.write(html_content)
    print(f"HTML saved to: {html_path}")

    # Convert to PDF
    pdf_path = OUTPUT_DIR / 'Artist_Productivity_Research_Report.pdf'
    HTML(string=html_content).write_pdf(pdf_path)
    print(f"PDF saved to: {pdf_path}")

if __name__ == '__main__':
    main()
