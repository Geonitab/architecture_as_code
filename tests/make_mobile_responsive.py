#!/usr/bin/env python3
"""
Mobile responsiveness post-processor for pytest-html reports.

This script modifies generated HTML test reports to make them fully compatible
and visually appealing on iPhone and other mobile devices.
"""

import re
import sys
from pathlib import Path


def add_mobile_responsiveness(html_file_path):
    """
    Add mobile-responsive CSS and viewport meta tag to an HTML test report.
    
    Args:
        html_file_path (Path): Path to the HTML file to modify
        
    Returns:
        bool: True if successful, False otherwise
    """
    try:
        # Read the original HTML file
        with open(html_file_path, 'r', encoding='utf-8') as f:
            html_content = f.read()
        
        # Read the mobile CSS file
        css_file = Path(__file__).parent / 'mobile-responsive.css'
        with open(css_file, 'r', encoding='utf-8') as f:
            mobile_css = f.read()
        
        # Add viewport meta tag if not present
        if 'name="viewport"' not in html_content:
            viewport_tag = '<meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=yes"/>'
            html_content = html_content.replace(
                '<meta charset="utf-8"/>',
                f'<meta charset="utf-8"/>\n    {viewport_tag}'
            )
        
        # Add mobile CSS before the closing </style> tag
        mobile_css_block = f'\n\n/* === MOBILE RESPONSIVENESS OVERRIDES === */\n{mobile_css}\n'
        html_content = html_content.replace('</style>', f'{mobile_css_block}</style>')
        
        # Add data labels for responsive table display
        # This finds table cells and adds data-label attributes for mobile display
        html_content = add_table_data_labels(html_content)
        
        # Write the modified HTML back to the file
        with open(html_file_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print(f"✓ Mobile responsiveness added to {html_file_path.name}")
        return True
        
    except Exception as e:
        print(f"✗ Error processing {html_file_path}: {e}")
        return False


def add_table_data_labels(html_content):
    """
    Add data-label attributes to table cells for responsive display.
    
    Args:
        html_content (str): The HTML content to modify
        
    Returns:
        str: Modified HTML content with data-label attributes
    """
    # Define common table headers and their labels
    header_labels = {
        'Test': 'Test',
        'Result': 'Result', 
        'Duration': 'Duration',
        'Links': 'Links',
        'test': 'Test',
        'result': 'Result',
        'duration': 'Duration',
        'links': 'Links'
    }
    
    # Find the results table and add data labels
    table_pattern = r'<table id="results-table"[^>]*>(.*?)</table>'
    table_match = re.search(table_pattern, html_content, re.DOTALL)
    
    if table_match:
        table_content = table_match.group(1)
        
        # Extract header row to determine column labels
        header_pattern = r'<thead[^>]*>.*?<tr[^>]*>(.*?)</tr>.*?</thead>'
        header_match = re.search(header_pattern, table_content, re.DOTALL)
        
        if header_match:
            header_row = header_match.group(1)
            # Extract th text content
            th_pattern = r'<th[^>]*[^>]*>(.*?)</th>'
            headers = []
            for th_match in re.finditer(th_pattern, header_row, re.DOTALL):
                th_text = re.sub(r'<[^>]+>', '', th_match.group(1)).strip()
                headers.append(th_text)
            
            # Now add data-label attributes to td elements
            tbody_pattern = r'<tbody[^>]*>(.*?)</tbody>'
            tbody_match = re.search(tbody_pattern, table_content, re.DOTALL)
            
            if tbody_match:
                tbody_content = tbody_match.group(1)
                
                # Process each row
                row_pattern = r'<tr[^>]*>(.*?)</tr>'
                modified_tbody = tbody_content
                
                for row_match in re.finditer(row_pattern, tbody_content, re.DOTALL):
                    row_content = row_match.group(1)
                    td_pattern = r'<td[^>]*class="([^"]*)"[^>]*>(.*?)</td>'
                    
                    cell_index = 0
                    modified_row = row_content
                    
                    for td_match in re.finditer(td_pattern, row_content, re.DOTALL):
                        if cell_index < len(headers):
                            old_td = td_match.group(0)
                            class_attr = td_match.group(1)
                            cell_content = td_match.group(2)
                            
                            # Create new td with data-label
                            label = headers[cell_index] if cell_index < len(headers) else f'Column {cell_index + 1}'
                            new_td = f'<td class="{class_attr}" data-label="{label}">{cell_content}</td>'
                            modified_row = modified_row.replace(old_td, new_td)
                            
                        cell_index += 1
                    
                    modified_tbody = modified_tbody.replace(row_content, modified_row)
                
                # Replace the original tbody with the modified one
                table_content = table_content.replace(tbody_match.group(1), modified_tbody)
                html_content = html_content.replace(table_match.group(1), table_content)
    
    return html_content


def process_test_reports(report_dir=None):
    """
    Process all HTML test reports in the test-reports directory.
    
    Args:
        report_dir (Path, optional): Directory containing test reports.
                                   Defaults to test-reports/ in project root.
    
    Returns:
        int: Number of files successfully processed
    """
    if report_dir is None:
        script_dir = Path(__file__).parent
        project_root = script_dir.parent
        report_dir = project_root / "test-reports"
    
    if not report_dir.exists():
        print(f"Report directory {report_dir} does not exist")
        return 0
    
    html_files = list(report_dir.glob("*.html"))
    if not html_files:
        print(f"No HTML files found in {report_dir}")
        return 0
    
    success_count = 0
    print(f"Processing {len(html_files)} HTML test report(s)...")
    
    for html_file in html_files:
        if add_mobile_responsiveness(html_file):
            success_count += 1
    
    print(f"\n✓ Successfully processed {success_count}/{len(html_files)} test report(s)")
    return success_count


def main():
    """Main CLI entry point."""
    if len(sys.argv) > 1:
        # Process specific file
        html_file = Path(sys.argv[1])
        if html_file.exists():
            add_mobile_responsiveness(html_file)
        else:
            print(f"File {html_file} does not exist")
            sys.exit(1)
    else:
        # Process all reports in test-reports directory
        process_test_reports()


if __name__ == "__main__":
    main()