# Dark Project HTML Structure Reference

Documentation of the Dark topic portal platform's HTML structure for CSS generation alignment.

## Overview

The Dark project uses Go templates with a component-based architecture:
- **Layouts:** Base template with blocks
- **Pages:** Topic portals, content views, search, home
- **Partials:** Reusable components (header, footer, content previews)
- **CSS Framework:** `life.css` (Modum Design System)
- **JavaScript:** HTMX for dynamic loading, theme toggle

## Base Template Structure

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <!-- Meta -->
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">

    <!-- Title & Description -->
    <title>{{.Title}}</title>
    <meta name="description" content="...">

    <!-- Favicon -->
    <link rel="icon" type="image/svg+xml" href="/static/images/favicon.svg">

    <!-- Theme Script (inline to prevent flash) -->
    <script>
        (function(){
            const savedTheme = localStorage.getItem('theme') || 'system';
            const root = document.documentElement;
            if (savedTheme === 'system') {
                const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
                root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
            } else {
                root.setAttribute('data-theme', savedTheme);
            }
        })();
    </script>

    <!-- CSS -->
    <link rel="stylesheet" href="/static/css/life.css">

    <!-- JavaScript -->
    <script defer src="/static/js/vendor/htmx.min.js"></script>
    <script defer src="/static/js/theme-lite.js"></script>
</head>
<body>
    <header class="sticky-header">
        <div class="container flex items-center justify-between" style="height: var(--header-height);">
            <div class="flex items-center gap-4">
                <h1 class="text-xl font-bold m-0">
                    <a href="/" style="color: var(--primary-foreground); text-decoration: none;">Dark</a>
                </h1>
                <p class="text-sm m-0" style="color: var(--primary-foreground); opacity: 0.9;">토픽 포털!</p>
            </div>
        </div>
    </header>

    <main class="container" style="margin-top: 1.5rem;">
        <!-- Page content here -->
    </main>

    <footer>
        <p>Dark Web Service v1.0.0</p>
    </footer>
</body>
</html>
```

## CSS Classes Used

### Layout Classes

| Class | Purpose | CSS Properties |
|-------|---------|----------------|
| `.container` | Page width constraint | `max-width`, `margin-inline: auto`, `padding-inline` |
| `.sticky-header` | Fixed header | `position: sticky`, `top: 0`, `z-index` |
| `.flex` | Flexbox container | `display: flex` |
| `.items-center` | Vertical center align | `align-items: center` |
| `.justify-between` | Space between | `justify-content: space-between` |
| `.gap-4` | Flex/grid gap | `gap: 1rem` (or `var(--space-4)`) |

### Typography Classes

| Class | Purpose | CSS Properties |
|-------|---------|----------------|
| `.text-xl` | Extra large text | `font-size: 1.25rem` |
| `.text-lg` | Large text | `font-size: 1.125rem` |
| `.text-base` | Base text size | `font-size: 1rem` |
| `.text-sm` | Small text | `font-size: 0.875rem` |
| `.text-xs` | Extra small text | `font-size: 0.75rem` |
| `.font-bold` | Bold weight | `font-weight: 700` |
| `.font-semibold` | Semibold weight | `font-weight: 600` |
| `.text-muted` | Muted text color | `color: var(--muted-foreground)` |
| `.korean-text` | Korean typography | Korean font settings |

### Spacing Classes

| Class | Purpose | CSS Properties |
|-------|---------|----------------|
| `.m-0` | No margin | `margin: 0` |
| `.mb-2` | Margin bottom (small) | `margin-bottom: 0.5rem` |
| `.mb-3` | Margin bottom (medium) | `margin-bottom: 0.75rem` |
| `.mb-4` | Margin bottom (large) | `margin-bottom: 1rem` |
| `.mb-6` | Margin bottom (xl) | `margin-bottom: 1.5rem` |
| `.mt-2` | Margin top | `margin-top: 0.5rem` |

### Component Classes

| Class | Purpose | Context |
|-------|---------|---------|
| `.content-preview` | Content card/preview | Article preview styling |
| `.post-preview-group` | Content list container | Group of content previews |
| `.meta-bar` | Metadata display | Content metadata (type, date, stats) |
| `.keywords` | Keyword tags container | Topic keywords |
| `.keyword` | Individual keyword tag | Inline tag styling |
| `.description` | Content description | Excerpt or summary text |
| `.content-type` | Content type badge | Badge/tag for content type |

## Topic Portal Page Structure

```html
<main class="container" style="margin-top: 1.5rem;">
    <section>
        <!-- Topic Header -->
        <div class="mb-6">
            <h1 class="text-2xl font-bold mb-2 korean-text">{{.Topic.Name}}</h1>
            <p class="text-base text-muted mb-3 korean-text">{{.Topic.Description}}</p>

            <!-- Keywords -->
            <div class="keywords">
                <span class="keyword">키워드1</span>
                <span class="keyword">키워드2</span>
            </div>
        </div>

        <!-- Content Section -->
        <h2 class="text-lg font-semibold mb-4">콘텐츠 (10개)</h2>

        <div class="post-preview-group">
            <!-- Content Preview (repeated) -->
            <article class="content-preview korean-text">
                <h3>
                    <a href="/content/123">Content Title Here</a>
                </h3>
                <p class="description">Content description or excerpt goes here...</p>

                <!-- Metadata bar -->
                <div class="meta-bar">
                    <span class="content-type">article</span>
                    <span class="text-xs">ko</span>
                    <time class="text-xs">2025-10-20</time>
                    <span class="text-xs">품질: 85%</span>
                    <span class="text-xs">조회 1,234</span>
                </div>

                <p class="text-xs text-muted mt-2">Author Name</p>
            </article>
        </div>
    </section>
</main>
```

## CSS Variable System (life.css)

The Dark project uses CSS custom properties for theming:

### Color Variables
```css
:root {
  --primary: /* Primary brand color */
  --primary-foreground: /* Text on primary */
  --muted-foreground: /* Muted text color */
  --background: /* Page background */
  --foreground: /* Main text color */
  --border: /* Border color */
}

[data-theme="dark"] {
  /* Dark mode overrides */
}
```

### Spacing Variables
```css
:root {
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;
}
```

### Layout Variables
```css
:root {
  --header-height: 60px;
  --container-max-width: 1200px;
  --border-radius: 0.5rem;
}
```

## Common HTML Patterns

### Header Navigation
```html
<header class="sticky-header">
    <div class="container flex items-center justify-between">
        <div class="flex items-center gap-4">
            <h1 class="text-xl font-bold m-0">
                <a href="/">Site Name</a>
            </h1>
            <p class="text-sm m-0">Tagline</p>
        </div>
        <!-- Optional: Navigation links, theme toggle -->
    </div>
</header>
```

### Content Card/Preview
```html
<article class="content-preview">
    <h3>
        <a href="/content/id">Title</a>
    </h3>
    <p class="description">Excerpt text...</p>
    <div class="meta-bar">
        <span class="content-type">type</span>
        <time>Date</time>
        <span>Additional metadata</span>
    </div>
</article>
```

### Keyword Tags
```html
<div class="keywords">
    <span class="keyword">Tag 1</span>
    <span class="keyword">Tag 2</span>
    <span class="keyword">Tag 3</span>
</div>
```

### Main Container
```html
<main class="container" style="margin-top: 1.5rem;">
    <section>
        <!-- Page content -->
    </section>
</main>
```

## Responsive Considerations

- **Container padding:** Responsive via CSS variables
- **Font sizes:** Use utility classes (`.text-sm`, `.text-lg`)
- **Layout:** Flexbox with gap for easy responsive stacking
- **Header:** Sticky positioning with `--header-height` variable

## Korean Typography

Classes like `.korean-text` apply specific font settings for Korean content:
- Font family optimized for Hangul
- Line height adjustments
- Letter spacing considerations

## Theme System

The Dark project supports light/dark themes via `data-theme` attribute:

```javascript
// Theme detection (inline in <head>)
const savedTheme = localStorage.getItem('theme') || 'system';
const root = document.documentElement;

if (savedTheme === 'system') {
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    root.setAttribute('data-theme', prefersDark ? 'dark' : 'light');
} else {
    root.setAttribute('data-theme', savedTheme);
}
```

CSS responds to the attribute:
```css
:root {
  --background: white;
  --foreground: #1a1a1a;
}

[data-theme="dark"] {
  --background: #1a1a1a;
  --foreground: #f5f5f5;
}
```

## HTMX Integration

The Dark project uses HTMX for dynamic content loading:

```html
<!-- Loaded deferred -->
<script defer src="/static/js/vendor/htmx.min.js"></script>

<!-- Example usage -->
<div hx-get="/api/content" hx-trigger="intersect once">
    Loading...
</div>
```

## CSS File Organization

```
static/css/
└── life.css        # Main stylesheet (Modum Design System)
```

Single-file CSS approach with:
1. CSS Reset/Normalize
2. CSS Custom Properties
3. Base styles
4. Utility classes
5. Component styles
6. Dark theme overrides

## Key Differences from Standard Web Design

1. **Korean-first:** Typography and layout optimized for Korean content
2. **Server-side rendering:** Go templates, not SPA
3. **HTMX over React:** Progressive enhancement approach
4. **Single CSS file:** No build step, direct browser support
5. **Theme attribute:** `data-theme` not class-based theme switching
6. **Minimal JavaScript:** Theme toggle + HTMX only

## CSS Generation Strategy

When generating CSS for Dark project HTML:

1. **Match utility class patterns** (`.text-*`, `.m-*`, `.flex`, etc.)
2. **Use CSS variables** for colors, spacing, typography
3. **Support `data-theme`** attribute for dark mode
4. **Maintain semantic class names** (`.content-preview`, `.meta-bar`)
5. **Keep Korean text support** (font families, line heights)
6. **Preserve layout structure** (`.container`, `.sticky-header`)
7. **Use modern CSS** (flexbox, grid, logical properties)

## Example: Generating CSS for Topic Portal

Given the HTML structure above, generate CSS that:

```css
/* Container */
.container {
  max-width: var(--container-max-width, 1200px);
  margin-inline: auto;
  padding-inline: var(--space-4, 1rem);
}

/* Content Preview */
.content-preview {
  padding: var(--space-4);
  border: 1px solid var(--border);
  border-radius: var(--border-radius);
  margin-bottom: var(--space-4);
}

.content-preview h3 {
  margin: 0 0 var(--space-2) 0;
  font-size: var(--font-lg);
}

.content-preview h3 a {
  color: var(--foreground);
  text-decoration: none;
}

.content-preview h3 a:hover {
  color: var(--primary);
  text-decoration: underline;
}

/* Meta bar */
.meta-bar {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  align-items: center;
  margin-top: var(--space-3);
  font-size: var(--font-xs);
  color: var(--muted-foreground);
}

/* Keywords */
.keywords {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
}

.keyword {
  display: inline-block;
  padding: var(--space-1) var(--space-2);
  background: var(--primary);
  color: var(--primary-foreground);
  border-radius: calc(var(--border-radius) / 2);
  font-size: var(--font-sm);
}
```

This ensures generated CSS aligns with Dark project's HTML structure and design system.
