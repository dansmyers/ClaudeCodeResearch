#!/usr/bin/env python3
"""Convert Markdown report to PDF using Weasyprint."""

import markdown
from weasyprint import HTML, CSS

# Read the markdown file
with open('housing_affordability_report.md', 'r', encoding='utf-8') as f:
    md_content = f.read()

# Convert markdown to HTML
md = markdown.Markdown(extensions=['tables', 'toc'])
html_content = md.convert(md_content)

# Wrap in full HTML document with styling
full_html = f"""
<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8">
    <title>Housing Affordability and Young Male Wages</title>
</head>
<body>
{html_content}
</body>
</html>
"""

# CSS for academic styling
css = CSS(string="""
    @page {{
        size: letter;
        margin: 1in;
        @bottom-center {{
            content: counter(page);
            font-family: "Times New Roman", Times, serif;
            font-size: 10pt;
        }}
    }}

    body {{
        font-family: "Times New Roman", Times, serif;
        font-size: 12pt;
        line-height: 1.6;
        text-align: justify;
        color: #000;
    }}

    h1 {{
        font-size: 16pt;
        font-weight: bold;
        text-align: center;
        margin-top: 0;
        margin-bottom: 24pt;
        page-break-after: avoid;
    }}

    h2 {{
        font-size: 14pt;
        font-weight: bold;
        margin-top: 18pt;
        margin-bottom: 12pt;
        page-break-after: avoid;
    }}

    h3 {{
        font-size: 12pt;
        font-weight: bold;
        font-style: italic;
        margin-top: 12pt;
        margin-bottom: 6pt;
        page-break-after: avoid;
    }}

    p {{
        margin-bottom: 12pt;
        text-indent: 0.5in;
    }}

    p:first-of-type {{
        text-indent: 0;
    }}

    h2 + p, h3 + p {{
        text-indent: 0;
    }}

    table {{
        width: 100%;
        border-collapse: collapse;
        margin: 18pt 0;
        font-size: 10pt;
        page-break-inside: avoid;
    }}

    th, td {{
        border: 1px solid #000;
        padding: 6pt 8pt;
        text-align: left;
    }}

    th {{
        background-color: #f0f0f0;
        font-weight: bold;
    }}

    td:first-child {{
        font-weight: normal;
    }}

    tr:nth-child(even) {{
        background-color: #fafafa;
    }}

    hr {{
        border: none;
        border-top: 1px solid #ccc;
        margin: 24pt 0;
    }}

    em {{
        font-style: italic;
    }}

    strong {{
        font-weight: bold;
    }}

    ul, ol {{
        margin-left: 0.5in;
        margin-bottom: 12pt;
    }}

    li {{
        margin-bottom: 6pt;
    }}

    /* References section styling */
    h2:contains("References") + p {{
        text-indent: -0.5in;
        padding-left: 0.5in;
    }}
""")

# Generate PDF
html = HTML(string=full_html)
html.write_pdf('housing_affordability_report.pdf', stylesheets=[css])

print("PDF generated successfully: housing_affordability_report.pdf")
