#!/usr/bin/env python3
"""
CSS Extraction Script

Visits a live URL using Playwright and extracts design tokens:
- Color palette (all unique colors)
- Typography (fonts, sizes, weights)
- Spacing values (margins, padding)
- Layout patterns (flexbox, grid)
- CSS custom properties

Usage:
    python3 extract_css.py <url> [--output <file.json>]

Example:
    python3 extract_css.py https://example.com --output design_tokens.json
"""

import argparse
import json
import re
from collections import defaultdict
from urllib.parse import urlparse


def extract_design_tokens(page):
    """Extract design tokens from a Playwright page object"""

    # Execute JavaScript to analyze computed styles
    tokens = page.evaluate("""
        () => {
            const tokens = {
                colors: new Set(),
                fonts: new Set(),
                fontSizes: new Set(),
                fontWeights: new Set(),
                spacing: new Set(),
                borderRadius: new Set(),
                shadows: new Set(),
                cssVariables: {}
            };

            // Get all elements
            const elements = document.querySelectorAll('*');

            elements.forEach(el => {
                const styles = window.getComputedStyle(el);

                // Colors
                tokens.colors.add(styles.color);
                tokens.colors.add(styles.backgroundColor);
                tokens.colors.add(styles.borderColor);

                // Typography
                tokens.fonts.add(styles.fontFamily);
                tokens.fontSizes.add(styles.fontSize);
                tokens.fontWeights.add(styles.fontWeight);

                // Spacing
                tokens.spacing.add(styles.margin);
                tokens.spacing.add(styles.padding);
                tokens.spacing.add(styles.gap);

                // Border radius
                if (styles.borderRadius !== '0px') {
                    tokens.borderRadius.add(styles.borderRadius);
                }

                // Shadows
                if (styles.boxShadow !== 'none') {
                    tokens.shadows.add(styles.boxShadow);
                }
            });

            // Extract CSS variables from :root
            const rootStyles = window.getComputedStyle(document.documentElement);
            for (let i = 0; i < rootStyles.length; i++) {
                const prop = rootStyles[i];
                if (prop.startsWith('--')) {
                    tokens.cssVariables[prop] = rootStyles.getPropertyValue(prop).trim();
                }
            }

            // Convert Sets to Arrays for JSON
            return {
                colors: Array.from(tokens.colors).filter(c => c && c !== 'rgba(0, 0, 0, 0)'),
                fonts: Array.from(tokens.fonts),
                fontSizes: Array.from(tokens.fontSizes),
                fontWeights: Array.from(tokens.fontWeights),
                spacing: Array.from(tokens.spacing).filter(s => s && s !== '0px'),
                borderRadius: Array.from(tokens.borderRadius),
                shadows: Array.from(tokens.shadows),
                cssVariables: tokens.cssVariables
            };
        }
    """)

    # Clean up and organize tokens
    cleaned_tokens = {
        'colors': _clean_colors(tokens['colors']),
        'typography': {
            'fonts': _clean_fonts(tokens['fonts']),
            'sizes': _organize_sizes(tokens['fontSizes']),
            'weights': sorted(set(tokens['fontWeights']))
        },
        'spacing': _organize_spacing(tokens['spacing']),
        'borderRadius': _organize_sizes(tokens['borderRadius']),
        'shadows': tokens['shadows'][:10],  # Limit to most common
        'cssVariables': tokens['cssVariables']
    }

    return cleaned_tokens


def _clean_colors(colors):
    """Clean and deduplicate colors"""
    unique_colors = set()
    for color in colors:
        # Convert to hex if possible, or keep as is
        if color and color not in ['transparent', 'inherit', 'initial']:
            unique_colors.add(color)
    return sorted(list(unique_colors))[:20]  # Top 20 colors


def _clean_fonts(fonts):
    """Extract primary fonts from font families"""
    primary_fonts = set()
    for font_family in fonts:
        # Get first font in the stack
        first_font = font_family.split(',')[0].strip().strip('"\'')
        if first_font and first_font not in ['inherit', 'initial']:
            primary_fonts.add(first_font)
    return sorted(list(primary_fonts))


def _organize_sizes(sizes):
    """Organize sizes by converting to px and sorting"""
    px_sizes = []
    for size in sizes:
        if 'px' in size:
            try:
                px_val = float(size.replace('px', ''))
                px_sizes.append(size)
            except ValueError:
                continue
    return sorted(set(px_sizes), key=lambda x: float(x.replace('px', '')))


def _organize_spacing(spacing_values):
    """Extract unique spacing values"""
    unique_spacing = set()
    for value in spacing_values:
        # Split multi-value properties (e.g., "10px 20px")
        parts = value.split()
        for part in parts:
            if part and part != '0px':
                unique_spacing.add(part)
    return _organize_sizes(list(unique_spacing))


def analyze_layout(page):
    """Analyze layout patterns (grid, flexbox)"""
    layout_info = page.evaluate("""
        () => {
            const layouts = {
                flex: [],
                grid: [],
                containers: []
            };

            const elements = document.querySelectorAll('*');

            elements.forEach(el => {
                const styles = window.getComputedStyle(el);
                const rect = el.getBoundingClientRect();

                // Only analyze visible elements with significant size
                if (rect.width > 100 && rect.height > 50) {
                    const selector = el.tagName.toLowerCase() +
                                   (el.className ? '.' + el.className.split(' ')[0] : '');

                    if (styles.display === 'flex') {
                        layouts.flex.push({
                            selector: selector,
                            direction: styles.flexDirection,
                            justify: styles.justifyContent,
                            align: styles.alignItems,
                            gap: styles.gap
                        });
                    }

                    if (styles.display === 'grid') {
                        layouts.grid.push({
                            selector: selector,
                            columns: styles.gridTemplateColumns,
                            rows: styles.gridTemplateRows,
                            gap: styles.gap
                        });
                    }

                    // Track main container widths
                    if (rect.width > window.innerWidth * 0.8) {
                        layouts.containers.push({
                            selector: selector,
                            maxWidth: styles.maxWidth,
                            width: styles.width,
                            padding: styles.padding
                        });
                    }
                }
            });

            return layouts;
        }
    """)

    return layout_info


def main():
    parser = argparse.ArgumentParser(description='Extract CSS design tokens from a website')
    parser.add_argument('url', help='URL of the website to analyze')
    parser.add_argument('--output', '-o', default='design_tokens.json',
                       help='Output JSON file (default: design_tokens.json)')
    parser.add_argument('--headless', action='store_true', default=True,
                       help='Run browser in headless mode')
    parser.add_argument('--no-headless', action='store_false', dest='headless',
                       help='Show browser window')

    args = parser.parse_args()

    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        print("Error: Playwright not installed. Install with:")
        print("  pip install playwright")
        print("  playwright install chromium")
        return 1

    print(f"Analyzing {args.url}...")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        page = browser.new_page()

        # Visit URL
        print("Loading page...")
        page.goto(args.url, wait_until='networkidle')

        # Extract design tokens
        print("Extracting design tokens...")
        tokens = extract_design_tokens(page)

        # Analyze layout
        print("Analyzing layout patterns...")
        layout = analyze_layout(page)

        # Get page metadata
        metadata = {
            'url': args.url,
            'title': page.title(),
            'viewport': page.viewport_size,
        }

        browser.close()

    # Combine all data
    result = {
        'metadata': metadata,
        'tokens': tokens,
        'layout': layout
    }

    # Save to file
    with open(args.output, 'w') as f:
        json.dump(result, f, indent=2)

    print(f"\n✅ Design tokens extracted to {args.output}")
    print(f"   Colors: {len(tokens['colors'])}")
    print(f"   Fonts: {len(tokens['typography']['fonts'])}")
    print(f"   Font sizes: {len(tokens['typography']['sizes'])}")
    print(f"   Spacing values: {len(tokens['spacing'])}")
    print(f"   CSS variables: {len(tokens['cssVariables'])}")
    print(f"   Flex layouts: {len(layout['flex'])}")
    print(f"   Grid layouts: {len(layout['grid'])}")

    return 0


if __name__ == '__main__':
    exit(main())
