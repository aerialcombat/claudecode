#!/usr/bin/env python3
"""
HTMX Template Analyzer

Analyzes existing HTML templates to find HTMX conversion opportunities.
Identifies forms, links, and content sections that could benefit from HTMX.

Usage:
    python analyze_templates.py --path /path/to/templates
    python analyze_templates.py --path /path/to/templates --priority
"""

import argparse
import os
import re
from pathlib import Path
from typing import List, Dict, Tuple

class HTMXOpportunity:
    def __init__(self, file_path, line_num, opp_type, element, suggestion, priority):
        self.file_path = file_path
        self.line_num = line_num
        self.opp_type = opp_type
        self.element = element
        self.suggestion = suggestion
        self.priority = priority

    def __repr__(self):
        priority_icon = {'high': '🔴', 'medium': '🟡', 'low': '🟢'}[self.priority]
        return f"{priority_icon} {self.opp_type:15} | {self.file_path}:{self.line_num}\n   └─ {self.suggestion}"

def analyze_template_file(file_path: Path) -> List[HTMXOpportunity]:
    """Analyze a single template file for HTMX opportunities"""
    opportunities = []

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
    except Exception as e:
        print(f"Warning: Could not read {file_path}: {e}")
        return opportunities

    for line_num, line in enumerate(lines, 1):
        line_lower = line.lower()

        # Check for forms
        if '<form' in line_lower:
            # Traditional form submission
            if 'action=' in line_lower and 'method="get"' in line_lower:
                opportunities.append(HTMXOpportunity(
                    file_path=file_path,
                    line_num=line_num,
                    opp_type='Search Form',
                    element=line.strip(),
                    suggestion='Convert to live search with hx-get and hx-trigger="keyup changed delay:500ms"',
                    priority='high'
                ))
            elif 'action=' in line_lower and 'method="post"' in line_lower:
                opportunities.append(HTMXOpportunity(
                    file_path=file_path,
                    line_num=line_num,
                    opp_type='Form Submit',
                    element=line.strip(),
                    suggestion='Add hx-post for inline form submission without page reload',
                    priority='medium'
                ))

        # Check for navigation links
        if '<a href=' in line_lower and 'hx-' not in line_lower:
            # Skip external links
            if 'http://' not in line_lower and 'https://' not in line_lower:
                # Skip anchors
                if 'href="#' not in line_lower:
                    opportunities.append(HTMXOpportunity(
                        file_path=file_path,
                        line_num=line_num,
                        opp_type='Nav Link',
                        element=line.strip()[:80] + '...' if len(line.strip()) > 80 else line.strip(),
                        suggestion='Consider hx-boost="true" for progressive enhancement',
                        priority='low'
                    ))

        # Check for pagination
        if re.search(r'(next|prev|previous|page\s*\d+)', line_lower):
            if '<a href=' in line_lower or '<button' in line_lower:
                opportunities.append(HTMXOpportunity(
                    file_path=file_path,
                    line_num=line_num,
                    opp_type='Pagination',
                    element=line.strip(),
                    suggestion='Use hx-get to load next page without full reload',
                    priority='medium'
                ))

        # Check for potential infinite scroll
        if re.search(r'{{range\s+\.\w+}}', line) or re.search(r'{%\s*for\s+', line):
            # Look for list rendering
            opportunities.append(HTMXOpportunity(
                file_path=file_path,
                line_num=line_num,
                opp_type='Content List',
                element=line.strip(),
                suggestion='Consider infinite scroll with hx-trigger="revealed"',
                priority='high'
            ))

        # Check for delete buttons
        if re.search(r'delete|remove|삭제', line_lower):
            if '<button' in line_lower or '<a' in line_lower:
                opportunities.append(HTMXOpportunity(
                    file_path=file_path,
                    line_num=line_num,
                    opp_type='Delete Action',
                    element=line.strip(),
                    suggestion='Add hx-delete with confirmation using hx-confirm attribute',
                    priority='medium'
                ))

        # Check for modal triggers
        if re.search(r'modal|popup|dialog', line_lower):
            opportunities.append(HTMXOpportunity(
                file_path=file_path,
                line_num=line_num,
                opp_type='Modal Trigger',
                element=line.strip(),
                suggestion='Load modal content dynamically with hx-get and hx-target="#modal"',
                priority='medium'
            ))

        # Check for tabs
        if re.search(r'tab|탭', line_lower):
            if '<button' in line_lower or '<a' in line_lower:
                opportunities.append(HTMXOpportunity(
                    file_path=file_path,
                    line_num=line_num,
                    opp_type='Tab Navigation',
                    element=line.strip(),
                    suggestion='Load tab content dynamically with hx-get',
                    priority='low'
                ))

    return opportunities

def analyze_templates(template_dir: Path) -> Dict[str, List[HTMXOpportunity]]:
    """Analyze all template files in directory"""
    all_opportunities = {}

    # Find all HTML template files
    html_files = list(template_dir.rglob('*.html')) + list(template_dir.rglob('*.tmpl'))

    print(f"Scanning {len(html_files)} template files...\n")

    for html_file in html_files:
        opportunities = analyze_template_file(html_file)
        if opportunities:
            all_opportunities[str(html_file)] = opportunities

    return all_opportunities

def print_opportunities(opportunities: Dict[str, List[HTMXOpportunity]], show_priority: bool = False):
    """Print found opportunities"""

    if not opportunities:
        print("✅ No HTMX conversion opportunities found.")
        print("   Your templates might already be using HTMX, or are simple static pages.")
        return

    # Group by type
    by_type = {}
    for file_path, opps in opportunities.items():
        for opp in opps:
            if opp.opp_type not in by_type:
                by_type[opp.opp_type] = []
            by_type[opp.opp_type].append(opp)

    print(f"{'='*80}")
    print(f"HTMX Conversion Opportunities Found: {sum(len(opps) for opps in opportunities.values())}")
    print(f"{'='*80}\n")

    # Print by type
    for opp_type, opps in sorted(by_type.items(), key=lambda x: len(x[1]), reverse=True):
        print(f"\n{opp_type} ({len(opps)} found)")
        print(f"{'-'*80}")

        # Group by priority if requested
        if show_priority:
            high = [o for o in opps if o.priority == 'high']
            medium = [o for o in opps if o.priority == 'medium']
            low = [o for o in opps if o.priority == 'low']

            if high:
                print(f"\n  🔴 High Priority ({len(high)})")
                for opp in high[:5]:  # Show first 5
                    print(f"     {opp.file_path}:{opp.line_num}")
                    print(f"     └─ {opp.suggestion}\n")

            if medium:
                print(f"\n  🟡 Medium Priority ({len(medium)})")
                for opp in medium[:3]:  # Show first 3
                    print(f"     {opp.file_path}:{opp.line_num}")
                    print(f"     └─ {opp.suggestion}\n")

            if low:
                print(f"\n  🟢 Low Priority ({len(low)})")
                print(f"     {len(low)} opportunities found (use --verbose to see all)\n")
        else:
            # Just show counts
            for opp in opps[:3]:
                print(f"  {opp}")

            if len(opps) > 3:
                print(f"  ... and {len(opps) - 3} more")

    # Summary and recommendations
    print(f"\n{'='*80}")
    print("Priority Recommendations")
    print(f"{'='*80}\n")

    # Count priorities
    high_priority = sum(1 for opps in opportunities.values() for o in opps if o.priority == 'high')
    medium_priority = sum(1 for opps in opportunities.values() for o in opps if o.priority == 'medium')
    low_priority = sum(1 for opps in opportunities.values() for o in opps if o.priority == 'low')

    print(f"🔴 High Priority:   {high_priority:3} - Start here for maximum impact")
    print(f"🟡 Medium Priority: {medium_priority:3} - Good value-to-effort ratio")
    print(f"🟢 Low Priority:    {low_priority:3} - Nice to have, low urgency\n")

    # Specific recommendations
    print("Suggested Implementation Order:")
    print("1. Convert search forms to live search (high user value)")
    print("2. Add infinite scroll to content lists (better UX)")
    print("3. Make forms submit inline (reduce page reloads)")
    print("4. Convert delete actions to HTMX (add confirmations)")
    print("5. Progressive enhancement for navigation (hx-boost)\n")

    print("Next Steps:")
    print("1. Pick highest priority opportunity")
    print("2. Generate component:")
    print("   python scripts/generate_component.py --type [type] --name [name] --korean --go-handler")
    print("3. Integrate into your template")
    print("4. Test and iterate\n")

def main():
    parser = argparse.ArgumentParser(
        description='Analyze templates for HTMX conversion opportunities',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  # Basic analysis
  python analyze_templates.py --path /path/to/templates

  # Show priority breakdown
  python analyze_templates.py --path /path/to/templates --priority

  # Verbose output
  python analyze_templates.py --path /path/to/templates --verbose
        '''
    )

    parser.add_argument('--path', required=True, type=str,
                        help='Path to templates directory')
    parser.add_argument('--priority', action='store_true',
                        help='Show priority breakdown')
    parser.add_argument('--verbose', action='store_true',
                        help='Show all opportunities (not just summary)')

    args = parser.parse_args()

    template_dir = Path(args.path)
    if not template_dir.exists():
        print(f"Error: Directory not found: {template_dir}")
        return 1

    if not template_dir.is_dir():
        print(f"Error: Not a directory: {template_dir}")
        return 1

    # Analyze templates
    opportunities = analyze_templates(template_dir)

    # Print results
    print_opportunities(opportunities, show_priority=args.priority)

    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main())
