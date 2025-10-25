#!/usr/bin/env python3
"""
Color Palette Extraction Script

Analyzes screenshots to extract color palettes and generate CSS variables.
Uses k-means clustering to identify dominant colors.

Usage:
    python3 analyze_colors.py <image_file> [--output <file.css>] [--num-colors <n>]

Example:
    python3 analyze_colors.py screenshot.png --output colors.css --num-colors 8
"""

import argparse
import json
from collections import Counter


def rgb_to_hex(rgb):
    """Convert RGB tuple to hex color"""
    return '#{:02x}{:02x}{:02x}'.format(int(rgb[0]), int(rgb[1]), int(rgb[2]))


def get_luminance(rgb):
    """Calculate relative luminance for WCAG contrast"""
    r, g, b = [x / 255.0 for x in rgb]
    r = r / 12.92 if r <= 0.03928 else ((r + 0.055) / 1.055) ** 2.4
    g = g / 12.92 if g <= 0.03928 else ((g + 0.055) / 1.055) ** 2.4
    b = b / 12.92 if b <= 0.03928 else ((b + 0.055) / 1.055) ** 2.4
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def is_grayscale(rgb, threshold=10):
    """Check if color is grayscale"""
    r, g, b = rgb
    return abs(r - g) < threshold and abs(g - b) < threshold and abs(r - b) < threshold


def extract_palette(image_path, num_colors=8):
    """Extract color palette from image using k-means clustering"""
    try:
        from PIL import Image
        import numpy as np
        from sklearn.cluster import KMeans
    except ImportError:
        print("Error: Required libraries not installed. Install with:")
        print("  pip install Pillow numpy scikit-learn")
        return None

    # Load and resize image for faster processing
    img = Image.open(image_path)
    img = img.convert('RGB')
    img.thumbnail((400, 400))

    # Convert to numpy array
    pixels = np.array(img)
    pixels = pixels.reshape(-1, 3)

    # Remove pure white and pure black (common background colors)
    pixels = pixels[~np.all(pixels == [255, 255, 255], axis=1)]
    pixels = pixels[~np.all(pixels == [0, 0, 0], axis=1)]

    # Use k-means to find dominant colors
    kmeans = KMeans(n_clusters=num_colors, random_state=42, n_init=10)
    kmeans.fit(pixels)

    # Get cluster centers (dominant colors)
    colors = kmeans.cluster_centers_

    # Get cluster sizes to weight colors by frequency
    labels = kmeans.labels_
    label_counts = Counter(labels)

    # Sort colors by frequency
    color_freq = [(colors[i], label_counts[i]) for i in range(num_colors)]
    color_freq.sort(key=lambda x: x[1], reverse=True)

    return [tuple(map(int, color)) for color, _ in color_freq]


def categorize_colors(colors):
    """Categorize colors into primary, neutral, and accent groups"""
    categorized = {
        'primary': [],
        'neutral': [],
        'accent': []
    }

    for rgb in colors:
        if is_grayscale(rgb):
            categorized['neutral'].append(rgb)
        else:
            # Determine if it's saturated enough to be primary/accent
            r, g, b = rgb
            max_val = max(r, g, b)
            min_val = min(r, g, b)
            saturation = (max_val - min_val) / max_val if max_val > 0 else 0

            if saturation > 0.3:
                if len(categorized['primary']) < 2:
                    categorized['primary'].append(rgb)
                else:
                    categorized['accent'].append(rgb)
            else:
                categorized['neutral'].append(rgb)

    return categorized


def generate_css_variables(categorized_colors):
    """Generate CSS custom properties from categorized colors"""
    css_vars = []
    css_vars.append("/* Color Palette - Generated from screenshot */")
    css_vars.append(":root {")

    # Primary colors
    for i, rgb in enumerate(categorized_colors['primary'], 1):
        hex_color = rgb_to_hex(rgb)
        css_vars.append(f"  --color-primary-{i}: {hex_color};")

    # Neutral colors (sorted by luminance)
    neutrals = sorted(categorized_colors['neutral'], key=get_luminance)
    for i, rgb in enumerate(neutrals, 1):
        hex_color = rgb_to_hex(rgb)
        luminance = get_luminance(rgb)
        # Name based on lightness
        if luminance > 0.7:
            name = f"light-{i}"
        elif luminance < 0.3:
            name = f"dark-{i}"
        else:
            name = f"neutral-{i}"
        css_vars.append(f"  --color-{name}: {hex_color};")

    # Accent colors
    for i, rgb in enumerate(categorized_colors['accent'], 1):
        hex_color = rgb_to_hex(rgb)
        css_vars.append(f"  --color-accent-{i}: {hex_color};")

    css_vars.append("}\n")

    return "\n".join(css_vars)


def generate_usage_example(categorized_colors):
    """Generate example CSS showing how to use the variables"""
    examples = []
    examples.append("/* Usage Examples */")
    examples.append("body {")
    if categorized_colors['neutral']:
        bg_color = rgb_to_hex(max(categorized_colors['neutral'], key=get_luminance))
        examples.append(f"  background-color: var(--color-light-1, {bg_color});")
    if categorized_colors['neutral']:
        text_color = rgb_to_hex(min(categorized_colors['neutral'], key=get_luminance))
        examples.append(f"  color: var(--color-dark-1, {text_color});")
    examples.append("}\n")

    if categorized_colors['primary']:
        examples.append("button, a {")
        examples.append(f"  background-color: var(--color-primary-1);")
        examples.append(f"  color: white;")
        examples.append("}\n")

    if categorized_colors['accent']:
        examples.append(".highlight {")
        examples.append(f"  border-left: 3px solid var(--color-accent-1);")
        examples.append("}\n")

    return "\n".join(examples)


def main():
    parser = argparse.ArgumentParser(description='Extract color palette from screenshot')
    parser.add_argument('image', help='Path to screenshot image')
    parser.add_argument('--output', '-o', default='color_palette.css',
                       help='Output CSS file (default: color_palette.css)')
    parser.add_argument('--num-colors', '-n', type=int, default=8,
                       help='Number of colors to extract (default: 8)')
    parser.add_argument('--json', action='store_true',
                       help='Also output JSON file with RGB values')

    args = parser.parse_args()

    print(f"Analyzing {args.image}...")

    # Extract palette
    colors = extract_palette(args.image, args.num_colors)
    if colors is None:
        return 1

    print(f"Extracted {len(colors)} colors")

    # Categorize colors
    categorized = categorize_colors(colors)
    print(f"  Primary: {len(categorized['primary'])}")
    print(f"  Neutral: {len(categorized['neutral'])}")
    print(f"  Accent: {len(categorized['accent'])}")

    # Generate CSS
    css_output = generate_css_variables(categorized)
    css_output += "\n" + generate_usage_example(categorized)

    # Save CSS file
    with open(args.output, 'w') as f:
        f.write(css_output)

    print(f"\n✅ CSS variables saved to {args.output}")

    # Optionally save JSON
    if args.json:
        json_output = {
            'primary': [rgb_to_hex(c) for c in categorized['primary']],
            'neutral': [rgb_to_hex(c) for c in categorized['neutral']],
            'accent': [rgb_to_hex(c) for c in categorized['accent']],
            'all_colors': [rgb_to_hex(c) for c in colors]
        }
        json_file = args.output.replace('.css', '.json')
        with open(json_file, 'w') as f:
            json.dump(json_output, f, indent=2)
        print(f"✅ Color data saved to {json_file}")

    # Print color preview
    print("\nColor Palette:")
    for category, color_list in categorized.items():
        if color_list:
            print(f"\n{category.upper()}:")
            for rgb in color_list:
                hex_color = rgb_to_hex(rgb)
                print(f"  {hex_color} - RGB{rgb}")

    return 0


if __name__ == '__main__':
    exit(main())
