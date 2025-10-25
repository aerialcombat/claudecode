# Design Tokens Guide

Design tokens are the visual design atoms of a design system — the named entities that store visual design attributes. This guide explains how to identify, organize, and implement design tokens in CSS.

## What are Design Tokens?

Design tokens are abstract, reusable values that maintain visual consistency across a design system. They represent:

- **Colors** - Brand colors, semantic colors, state colors
- **Typography** - Font families, sizes, weights, line heights
- **Spacing** - Margins, padding, gaps (often following a scale)
- **Sizing** - Widths, heights, max/min dimensions
- **Border** - Radii, widths, styles
- **Shadows** - Box shadows, text shadows
- **Animation** - Durations, timing functions

## Identifying Design Tokens from a Website

### Step 1: Extract Colors

**Look for:**
- Primary brand colors (usually in headers, buttons, links)
- Secondary/accent colors
- Neutral colors (grays for text, backgrounds, borders)
- Semantic colors (success green, error red, warning yellow)
- State colors (hover, active, disabled)

**Tools:**
- Browser DevTools Inspector
- `extract_css.py` script
- `analyze_colors.py` script for screenshots

**Example extraction:**
```css
:root {
  /* Primary */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;

  /* Neutral */
  --color-gray-100: #f3f4f6;
  --color-gray-200: #e5e7eb;
  --color-gray-900: #111827;

  /* Semantic */
  --color-success: #10b981;
  --color-error: #ef4444;
  --color-warning: #f59e0b;
}
```

### Step 2: Extract Typography

**Font Families:**
```css
:root {
  --font-sans: 'Inter', system-ui, sans-serif;
  --font-serif: 'Merriweather', Georgia, serif;
  --font-mono: 'JetBrains Mono', 'Courier New', monospace;
}
```

**Font Sizes (Type Scale):**

Look for a consistent scale. Common approaches:
- **Modular scale** (ratio-based: 1.25, 1.5, 1.618)
- **Fixed increments** (14px, 16px, 18px, 20px, 24px)
- **Responsive** (clamp functions)

```css
:root {
  /* Type scale (1.25 ratio) */
  --font-xs: 0.8rem;    /* 12.8px */
  --font-sm: 0.875rem;  /* 14px */
  --font-base: 1rem;    /* 16px */
  --font-lg: 1.25rem;   /* 20px */
  --font-xl: 1.563rem;  /* 25px */
  --font-2xl: 1.953rem; /* 31.25px */
  --font-3xl: 2.441rem; /* 39px */
}
```

**Font Weights:**
```css
:root {
  --font-light: 300;
  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;
}
```

**Line Heights:**
```css
:root {
  --leading-tight: 1.25;
  --leading-normal: 1.5;
  --leading-relaxed: 1.75;
  --leading-loose: 2;
}
```

### Step 3: Extract Spacing

**Common spacing scales:**

**Tailwind-style (4px base):**
```css
:root {
  --space-0: 0;
  --space-1: 0.25rem;  /* 4px */
  --space-2: 0.5rem;   /* 8px */
  --space-3: 0.75rem;  /* 12px */
  --space-4: 1rem;     /* 16px */
  --space-5: 1.25rem;  /* 20px */
  --space-6: 1.5rem;   /* 24px */
  --space-8: 2rem;     /* 32px */
  --space-10: 2.5rem;  /* 40px */
  --space-12: 3rem;    /* 48px */
  --space-16: 4rem;    /* 64px */
  --space-20: 5rem;    /* 80px */
}
```

**Golden ratio spacing:**
```css
:root {
  --space-xs: 0.5rem;
  --space-sm: 0.75rem;
  --space-md: 1rem;
  --space-lg: 1.5rem;
  --space-xl: 2.5rem;
  --space-2xl: 4rem;
}
```

### Step 4: Extract Border Radii

```css
:root {
  --radius-none: 0;
  --radius-sm: 0.125rem;  /* 2px */
  --radius-md: 0.375rem;  /* 6px */
  --radius-lg: 0.5rem;    /* 8px */
  --radius-xl: 0.75rem;   /* 12px */
  --radius-2xl: 1rem;     /* 16px */
  --radius-full: 9999px;  /* Pill shape */
}
```

### Step 5: Extract Shadows

```css
:root {
  --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1),
               0 2px 4px -1px rgba(0, 0, 0, 0.06);
  --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1),
               0 4px 6px -2px rgba(0, 0, 0, 0.05);
  --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1),
               0 10px 10px -5px rgba(0, 0, 0, 0.04);
}
```

## Organizing Design Tokens

### Naming Conventions

**Tier 1: Global/Brand Tokens**
```css
:root {
  --brand-primary: #3b82f6;
  --brand-secondary: #8b5cf6;
  --brand-accent: #ec4899;
}
```

**Tier 2: Semantic Tokens**
```css
:root {
  --color-text-primary: var(--brand-gray-900);
  --color-text-secondary: var(--brand-gray-600);
  --color-bg-primary: white;
  --color-bg-secondary: var(--brand-gray-50);
  --color-border: var(--brand-gray-300);
}
```

**Tier 3: Component Tokens**
```css
:root {
  --button-bg: var(--color-primary);
  --button-text: white;
  --button-hover-bg: var(--color-primary-hover);

  --card-bg: white;
  --card-border: var(--color-border);
  --card-shadow: var(--shadow-md);
}
```

### File Organization

```
styles/
├── tokens/
│   ├── colors.css
│   ├── typography.css
│   ├── spacing.css
│   ├── shadows.css
│   └── index.css (imports all)
├── base/
│   ├── reset.css
│   └── global.css
├── components/
│   ├── buttons.css
│   ├── cards.css
│   └── navigation.css
└── main.css
```

## Design Token Extraction Workflow

### Using Browser DevTools

1. **Open DevTools** (F12)
2. **Inspect element** (right-click → Inspect)
3. **Check Computed styles** for actual rendered values
4. **Look for CSS variables** in the Styles panel
5. **Note patterns** in spacing, colors, fonts

### Using Scripts

**Extract from live URL:**
```bash
python3 scripts/extract_css.py https://example.com --output tokens.json
```

**Extract colors from screenshot:**
```bash
python3 scripts/analyze_colors.py screenshot.png --output colors.css --json
```

**Generate CSS from tokens:**
```bash
python3 scripts/generate_css_template.py tokens.json --output styles.css
```

## Best Practices

### 1. Use Semantic Names

❌ **Bad:**
```css
--blue: #3b82f6;
--dark-blue: #2563eb;
```

✅ **Good:**
```css
--color-primary: #3b82f6;
--color-primary-hover: #2563eb;
```

### 2. Layer Your Tokens

```css
/* Layer 1: Raw values */
--blue-500: #3b82f6;
--gray-900: #111827;

/* Layer 2: Semantic */
--color-primary: var(--blue-500);
--color-text: var(--gray-900);

/* Layer 3: Component */
--button-bg: var(--color-primary);
```

### 3. Use a Scale System

**Spacing:**
```css
/* Consistent 8px scale */
--space-1: 0.5rem;  /* 8px */
--space-2: 1rem;    /* 16px */
--space-3: 1.5rem;  /* 24px */
--space-4: 2rem;    /* 32px */
--space-5: 2.5rem;  /* 40px */
--space-6: 3rem;    /* 48px */
```

**Typography:**
```css
/* 1.25 modular scale */
--font-sm: 0.8rem;
--font-base: 1rem;
--font-lg: 1.25rem;
--font-xl: 1.563rem;
--font-2xl: 1.953rem;
```

### 4. Support Dark Mode

```css
:root {
  --color-bg: white;
  --color-text: #111827;
}

@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #111827;
    --color-text: #f3f4f6;
  }
}

/* Or use data attribute */
[data-theme="dark"] {
  --color-bg: #111827;
  --color-text: #f3f4f6;
}
```

### 5. Document Your Tokens

```css
:root {
  /* Primary colors - Used for main CTAs and brand elements */
  --color-primary: #3b82f6;
  --color-primary-hover: #2563eb;

  /* Spacing scale - 8px base unit */
  --space-1: 0.5rem;   /* 8px - Tight spacing */
  --space-2: 1rem;     /* 16px - Standard spacing */
  --space-3: 1.5rem;   /* 24px - Comfortable spacing */
}
```

## Common Mistakes to Avoid

### 1. Too Many Tokens
Don't create a token for every possible value. Limit yourself to:
- **Colors:** 8-12 main colors + shades
- **Font sizes:** 6-8 sizes
- **Spacing:** 8-10 values
- **Shadows:** 4-5 variations

### 2. Hardcoded Values in Components
❌ **Bad:**
```css
.button {
  background: #3b82f6;
  padding: 12px 24px;
}
```

✅ **Good:**
```css
.button {
  background: var(--color-primary);
  padding: var(--space-3) var(--space-6);
}
```

### 3. Inconsistent Naming
Pick a naming convention and stick to it:
- `--color-primary` OR `--primary-color` (not both)
- `--space-4` OR `--spacing-md` (not both)

### 4. Not Considering Contrast
Always check color contrast ratios:
- **Normal text:** 4.5:1 minimum
- **Large text:** 3:1 minimum
- **UI components:** 3:1 minimum

Use tools like:
- WebAIM Contrast Checker
- Chrome DevTools Contrast Ratio

## Example: Complete Token System

```css
:root {
  /* ========== Colors ========== */

  /* Primary */
  --color-primary-50: #eff6ff;
  --color-primary-500: #3b82f6;
  --color-primary-900: #1e3a8a;

  /* Gray */
  --color-gray-50: #f9fafb;
  --color-gray-100: #f3f4f6;
  --color-gray-900: #111827;

  /* Semantic */
  --color-success: #10b981;
  --color-error: #ef4444;
  --color-warning: #f59e0b;

  /* ========== Typography ========== */

  --font-sans: 'Inter', system-ui, sans-serif;

  --font-xs: 0.75rem;
  --font-sm: 0.875rem;
  --font-base: 1rem;
  --font-lg: 1.125rem;
  --font-xl: 1.25rem;
  --font-2xl: 1.5rem;

  --font-normal: 400;
  --font-medium: 500;
  --font-semibold: 600;
  --font-bold: 700;

  /* ========== Spacing ========== */

  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* ========== Other ========== */

  --radius-sm: 0.25rem;
  --radius-md: 0.375rem;
  --radius-lg: 0.5rem;

  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);

  --transition-fast: 150ms;
  --transition-base: 200ms;
  --transition-slow: 300ms;
}
```
