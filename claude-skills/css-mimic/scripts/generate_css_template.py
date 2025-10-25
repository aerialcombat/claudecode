#!/usr/bin/env python3
"""
CSS Template Generator

Generates a complete CSS file from design tokens (extracted from websites or screenshots).
Creates organized CSS with custom properties, responsive design, and modern best practices.

Usage:
    python3 generate_css_template.py <tokens.json> [--output <file.css>] [--html <file.html>]

Example:
    python3 generate_css_template.py design_tokens.json --output styles.css --html index.html
"""

import argparse
import json
from pathlib import Path


def load_tokens(token_file):
    """Load design tokens from JSON file"""
    with open(token_file, 'r') as f:
        return json.load(f)


def generate_css_reset():
    """Generate modern CSS reset"""
    return """/* ==========================================
   CSS Reset - Modern Baseline
   ========================================== */

*, *::before, *::after {
  box-sizing: border-box;
}

* {
  margin: 0;
  padding: 0;
}

html {
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
}

body {
  min-height: 100vh;
  line-height: 1.5;
}

img, picture, video, canvas, svg {
  display: block;
  max-width: 100%;
}

input, button, textarea, select {
  font: inherit;
}

p, h1, h2, h3, h4, h5, h6 {
  overflow-wrap: break-word;
}
"""


def generate_custom_properties(tokens):
    """Generate CSS custom properties from tokens"""
    css = ["\n/* =========================================="]
    css.append("   Design Tokens - CSS Custom Properties")
    css.append("   ========================================== */\n")
    css.append(":root {")

    # Colors
    if 'colors' in tokens.get('tokens', {}):
        css.append("  /* Colors */")
        colors = tokens['tokens']['colors'][:10]  # Limit to 10 most common
        for i, color in enumerate(colors, 1):
            css.append(f"  --color-{i}: {color};")
        css.append("")

    # Typography
    if 'typography' in tokens.get('tokens', {}):
        typo = tokens['tokens']['typography']

        # Fonts
        if 'fonts' in typo and typo['fonts']:
            css.append("  /* Typography - Fonts */")
            primary_font = typo['fonts'][0]
            css.append(f"  --font-primary: {primary_font}, sans-serif;")
            if len(typo['fonts']) > 1:
                css.append(f"  --font-secondary: {typo['fonts'][1]}, serif;")
            css.append("")

        # Font sizes
        if 'sizes' in typo and typo['sizes']:
            css.append("  /* Typography - Sizes */")
            sizes = typo['sizes']
            if len(sizes) >= 5:
                css.append(f"  --font-xs: {sizes[0]};")
                css.append(f"  --font-sm: {sizes[1]};")
                css.append(f"  --font-base: {sizes[2]};")
                css.append(f"  --font-lg: {sizes[3]};")
                css.append(f"  --font-xl: {sizes[4]};")
            css.append("")

        # Font weights
        if 'weights' in typo and typo['weights']:
            css.append("  /* Typography - Weights */")
            weights = sorted(set(typo['weights']))
            for i, weight in enumerate(weights):
                name = {
                    '300': 'light',
                    '400': 'normal',
                    '500': 'medium',
                    '600': 'semibold',
                    '700': 'bold',
                    '800': 'extrabold'
                }.get(weight, f'weight-{i}')
                css.append(f"  --font-{name}: {weight};")
            css.append("")

    # Spacing
    if 'spacing' in tokens.get('tokens', {}):
        css.append("  /* Spacing Scale */")
        spacing = tokens['tokens']['spacing'][:8]  # Limit to 8 values
        for i, space in enumerate(spacing, 1):
            css.append(f"  --space-{i}: {space};")
        css.append("")

    # Border radius
    if 'borderRadius' in tokens.get('tokens', {}):
        css.append("  /* Border Radius */")
        radii = tokens['tokens']['borderRadius'][:4]
        for i, radius in enumerate(radii, 1):
            css.append(f"  --radius-{i}: {radius};")
        css.append("")

    # Shadows
    if 'shadows' in tokens.get('tokens', {}):
        css.append("  /* Shadows */")
        shadows = tokens['tokens']['shadows'][:3]
        for i, shadow in enumerate(shadows, 1):
            css.append(f"  --shadow-{i}: {shadow};")
        css.append("")

    # CSS Variables from the site
    if 'cssVariables' in tokens.get('tokens', {}) and tokens['tokens']['cssVariables']:
        css.append("  /* Extracted CSS Variables */")
        for var_name, var_value in list(tokens['tokens']['cssVariables'].items())[:10]:
            css.append(f"  {var_name}: {var_value};")
        css.append("")

    css.append("}\n")
    return "\n".join(css)


def generate_layout_css(tokens):
    """Generate layout CSS based on extracted patterns"""
    css = ["\n/* =========================================="]
    css.append("   Layout Patterns")
    css.append("   ========================================== */\n")

    # Container
    css.append("/* Container */")
    css.append(".container {")
    css.append("  width: 100%;")
    css.append("  max-width: 1200px;")
    css.append("  margin-inline: auto;")
    css.append("  padding-inline: var(--space-4, 1rem);")
    css.append("}\n")

    # Flex layouts from tokens
    if 'layout' in tokens and 'flex' in tokens['layout'] and tokens['layout']['flex']:
        css.append("/* Flex Layouts (extracted from target site) */")
        for i, flex in enumerate(tokens['layout']['flex'][:3], 1):  # Limit to 3 examples
            css.append(f".flex-pattern-{i} {{")
            css.append(f"  display: flex;")
            css.append(f"  flex-direction: {flex.get('direction', 'row')};")
            css.append(f"  justify-content: {flex.get('justify', 'flex-start')};")
            css.append(f"  align-items: {flex.get('align', 'flex-start')};")
            if flex.get('gap') and flex['gap'] != 'normal':
                css.append(f"  gap: {flex['gap']};")
            css.append("}\n")

    # Grid layouts from tokens
    if 'layout' in tokens and 'grid' in tokens['layout'] and tokens['layout']['grid']:
        css.append("/* Grid Layouts (extracted from target site) */")
        for i, grid in enumerate(tokens['layout']['grid'][:2], 1):  # Limit to 2 examples
            css.append(f".grid-pattern-{i} {{")
            css.append(f"  display: grid;")
            if grid.get('columns'):
                css.append(f"  grid-template-columns: {grid['columns']};")
            if grid.get('gap') and grid['gap'] != 'normal':
                css.append(f"  gap: {grid['gap']};")
            css.append("}\n")

    return "\n".join(css)


def generate_typography_css():
    """Generate typography CSS"""
    return """
/* ==========================================
   Typography
   ========================================== */

body {
  font-family: var(--font-primary, system-ui, sans-serif);
  font-size: var(--font-base, 1rem);
  font-weight: var(--font-normal, 400);
  line-height: 1.5;
  color: var(--color-1, #333);
}

h1, h2, h3, h4, h5, h6 {
  font-weight: var(--font-bold, 700);
  line-height: 1.2;
}

h1 { font-size: var(--font-xl, 2.5rem); }
h2 { font-size: var(--font-lg, 2rem); }
h3 { font-size: var(--font-base, 1.5rem); }

a {
  color: var(--color-2, #0066cc);
  text-decoration: none;
}

a:hover {
  text-decoration: underline;
}
"""


def generate_responsive_css():
    """Generate responsive design patterns"""
    return """
/* ==========================================
   Responsive Design
   ========================================== */

/* Mobile first approach */
@media (min-width: 640px) {
  :root {
    --font-base: 1.125rem;
  }
}

@media (min-width: 768px) {
  .container {
    padding-inline: var(--space-6, 2rem);
  }
}

@media (min-width: 1024px) {
  :root {
    --font-base: 1.25rem;
  }
}
"""


def generate_utility_classes():
    """Generate utility classes"""
    return """
/* ==========================================
   Utility Classes
   ========================================== */

/* Spacing */
.mt-1 { margin-top: var(--space-1, 0.25rem); }
.mt-2 { margin-top: var(--space-2, 0.5rem); }
.mt-3 { margin-top: var(--space-3, 1rem); }
.mt-4 { margin-top: var(--space-4, 1.5rem); }

.mb-1 { margin-bottom: var(--space-1, 0.25rem); }
.mb-2 { margin-bottom: var(--space-2, 0.5rem); }
.mb-3 { margin-bottom: var(--space-3, 1rem); }
.mb-4 { margin-bottom: var(--space-4, 1.5rem); }

/* Display */
.flex { display: flex; }
.grid { display: grid; }
.block { display: block; }
.inline-block { display: inline-block; }
.hidden { display: none; }

/* Text alignment */
.text-center { text-align: center; }
.text-left { text-align: left; }
.text-right { text-align: right; }
"""


def main():
    parser = argparse.ArgumentParser(description='Generate CSS from design tokens')
    parser.add_argument('tokens', help='Path to design tokens JSON file')
    parser.add_argument('--output', '-o', default='generated_styles.css',
                       help='Output CSS file (default: generated_styles.css)')
    parser.add_argument('--html', help='Optional: HTML file to analyze for additional context')
    parser.add_argument('--no-reset', action='store_true',
                       help='Skip CSS reset')
    parser.add_argument('--no-utilities', action='store_true',
                       help='Skip utility classes')

    args = parser.parse_args()

    # Load tokens
    print(f"Loading design tokens from {args.tokens}...")
    tokens = load_tokens(args.tokens)

    # Generate CSS sections
    css_parts = []

    if not args.no_reset:
        css_parts.append(generate_css_reset())

    css_parts.append(generate_custom_properties(tokens))
    css_parts.append(generate_layout_css(tokens))
    css_parts.append(generate_typography_css())
    css_parts.append(generate_responsive_css())

    if not args.no_utilities:
        css_parts.append(generate_utility_classes())

    # Combine all CSS
    final_css = "\n".join(css_parts)

    # Save to file
    with open(args.output, 'w') as f:
        f.write(final_css)

    print(f"\n✅ CSS generated and saved to {args.output}")
    print(f"   Total length: {len(final_css)} characters")

    # Print summary
    print("\nGenerated sections:")
    if not args.no_reset:
        print("  ✓ CSS Reset")
    print("  ✓ Custom Properties (Design Tokens)")
    print("  ✓ Layout Patterns")
    print("  ✓ Typography")
    print("  ✓ Responsive Design")
    if not args.no_utilities:
        print("  ✓ Utility Classes")

    return 0


if __name__ == '__main__':
    exit(main())
