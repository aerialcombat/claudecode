# CSS Layout Patterns Reference

Common CSS layout patterns and techniques for building modern, responsive web layouts.

## Table of Contents
- [Flexbox Patterns](#flexbox-patterns)
- [Grid Patterns](#grid-patterns)
- [Responsive Patterns](#responsive-patterns)
- [Common Components](#common-components)
- [Modern CSS Features](#modern-css-features)

---

## Flexbox Patterns

### Horizontal Navigation
```css
.nav {
  display: flex;
  align-items: center;
  gap: 2rem;
}

.nav-links {
  display: flex;
  gap: 1rem;
  margin-left: auto; /* Push to right */
}
```

### Card Layout (Flex Wrap)
```css
.card-container {
  display: flex;
  flex-wrap: wrap;
  gap: 1.5rem;
}

.card {
  flex: 1 1 300px; /* Grow, shrink, base 300px */
  min-width: 0; /* Allow shrinking below content size */
}
```

### Center Content (Flex)
```css
.center-flex {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
}
```

### Split Layout (Sidebar + Main)
```css
.layout {
  display: flex;
  gap: 2rem;
}

.sidebar {
  flex: 0 0 250px; /* Fixed width sidebar */
}

.main {
  flex: 1; /* Fill remaining space */
  min-width: 0; /* Prevent overflow */
}

/* Responsive: stack on mobile */
@media (max-width: 768px) {
  .layout {
    flex-direction: column;
  }

  .sidebar {
    flex: 1;
  }
}
```

### Flex Direction Utilities
```css
.flex-row { flex-direction: row; }
.flex-col { flex-direction: column; }
.flex-row-reverse { flex-direction: row-reverse; }
.flex-col-reverse { flex-direction: column-reverse; }

.items-start { align-items: flex-start; }
.items-center { align-items: center; }
.items-end { align-items: flex-end; }
.items-stretch { align-items: stretch; }

.justify-start { justify-content: flex-start; }
.justify-center { justify-content: center; }
.justify-end { justify-content: flex-end; }
.justify-between { justify-content: space-between; }
.justify-around { justify-content: space-around; }
```

---

## Grid Patterns

### 12-Column Grid System
```css
.grid-12 {
  display: grid;
  grid-template-columns: repeat(12, 1fr);
  gap: 1rem;
}

.col-span-1 { grid-column: span 1; }
.col-span-2 { grid-column: span 2; }
.col-span-3 { grid-column: span 3; }
.col-span-4 { grid-column: span 4; }
.col-span-6 { grid-column: span 6; }
.col-span-8 { grid-column: span 8; }
.col-span-12 { grid-column: span 12; }
```

### Auto-Fit Grid (Responsive Cards)
```css
.auto-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
  gap: 2rem;
}
```

### Holy Grail Layout (Grid)
```css
.holy-grail {
  display: grid;
  grid-template-areas:
    "header header header"
    "sidebar main aside"
    "footer footer footer";
  grid-template-columns: 200px 1fr 200px;
  grid-template-rows: auto 1fr auto;
  min-height: 100vh;
  gap: 1rem;
}

.header { grid-area: header; }
.sidebar { grid-area: sidebar; }
.main { grid-area: main; }
.aside { grid-area: aside; }
.footer { grid-area: footer; }

@media (max-width: 768px) {
  .holy-grail {
    grid-template-areas:
      "header"
      "main"
      "sidebar"
      "aside"
      "footer";
    grid-template-columns: 1fr;
  }
}
```

### Dashboard Grid
```css
.dashboard {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-auto-rows: 200px;
  gap: 1.5rem;
}

.widget-large {
  grid-column: span 2;
  grid-row: span 2;
}

.widget-wide {
  grid-column: span 2;
}

.widget-tall {
  grid-row: span 2;
}

@media (max-width: 1024px) {
  .dashboard {
    grid-template-columns: repeat(2, 1fr);
  }
}

@media (max-width: 640px) {
  .dashboard {
    grid-template-columns: 1fr;
  }
}
```

---

## Responsive Patterns

### Mobile-First Breakpoints
```css
/* Base: Mobile (< 640px) */
.container {
  padding-inline: 1rem;
}

/* Small (≥ 640px) */
@media (min-width: 640px) {
  .container {
    padding-inline: 1.5rem;
  }
}

/* Medium (≥ 768px) */
@media (min-width: 768px) {
  .container {
    max-width: 768px;
    margin-inline: auto;
  }
}

/* Large (≥ 1024px) */
@media (min-width: 1024px) {
  .container {
    max-width: 1024px;
  }
}

/* Extra Large (≥ 1280px) */
@media (min-width: 1280px) {
  .container {
    max-width: 1280px;
  }
}
```

### Container Queries (Modern)
```css
.card-container {
  container-type: inline-size;
  container-name: card;
}

.card-content {
  display: flex;
  flex-direction: column;
}

@container card (min-width: 400px) {
  .card-content {
    flex-direction: row;
  }
}
```

### Responsive Typography
```css
:root {
  --fluid-min-width: 320;
  --fluid-max-width: 1140;
  --fluid-min-size: 16;
  --fluid-max-size: 20;
}

body {
  font-size: clamp(
    calc(var(--fluid-min-size) * 1px),
    calc((var(--fluid-min-size) * 1px) + (var(--fluid-max-size) - var(--fluid-min-size)) * ((100vw - (var(--fluid-min-width) * 1px)) / (var(--fluid-max-width) - var(--fluid-min-width)))),
    calc(var(--fluid-max-size) * 1px)
  );
}

/* Simplified fluid typography */
h1 { font-size: clamp(2rem, 5vw, 4rem); }
h2 { font-size: clamp(1.5rem, 4vw, 3rem); }
h3 { font-size: clamp(1.25rem, 3vw, 2rem); }
```

---

## Common Components

### Hero Section
```css
.hero {
  min-height: 60vh;
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  text-align: center;
  padding: 4rem 2rem;
  background: linear-gradient(135deg, var(--color-primary), var(--color-secondary));
}

.hero h1 {
  font-size: clamp(2.5rem, 5vw, 4rem);
  margin-bottom: 1rem;
}

.hero p {
  font-size: clamp(1.125rem, 2vw, 1.5rem);
  max-width: 60ch;
}
```

### Card Component
```css
.card {
  background: white;
  border-radius: var(--radius-lg, 0.5rem);
  box-shadow: var(--shadow-md, 0 4px 6px rgba(0, 0, 0, 0.1));
  padding: 1.5rem;
  transition: transform 0.2s, box-shadow 0.2s;
}

.card:hover {
  transform: translateY(-4px);
  box-shadow: var(--shadow-lg, 0 10px 20px rgba(0, 0, 0, 0.15));
}

.card-image {
  width: 100%;
  aspect-ratio: 16 / 9;
  object-fit: cover;
  border-radius: var(--radius-md, 0.25rem);
  margin-bottom: 1rem;
}
```

### Button Styles
```css
.btn {
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  font-weight: 600;
  border: none;
  border-radius: var(--radius-md, 0.25rem);
  cursor: pointer;
  transition: all 0.2s;
}

.btn-primary {
  background: var(--color-primary);
  color: white;
}

.btn-primary:hover {
  background: var(--color-primary-dark);
  transform: translateY(-1px);
}

.btn-outline {
  background: transparent;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
}

.btn-outline:hover {
  background: var(--color-primary);
  color: white;
}
```

### Navigation Header
```css
.header {
  position: sticky;
  top: 0;
  z-index: 100;
  background: white;
  box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.nav-container {
  display: flex;
  align-items: center;
  justify-content: space-between;
  max-width: 1280px;
  margin-inline: auto;
  padding: 1rem 2rem;
}

.nav-links {
  display: flex;
  gap: 2rem;
  list-style: none;
}

.nav-link {
  color: var(--color-text);
  text-decoration: none;
  font-weight: 500;
  transition: color 0.2s;
}

.nav-link:hover,
.nav-link.active {
  color: var(--color-primary);
}

/* Mobile menu */
@media (max-width: 768px) {
  .nav-links {
    position: fixed;
    top: 60px;
    left: 0;
    right: 0;
    flex-direction: column;
    background: white;
    padding: 2rem;
    transform: translateX(-100%);
    transition: transform 0.3s;
  }

  .nav-links.open {
    transform: translateX(0);
  }
}
```

---

## Modern CSS Features

### CSS Custom Properties (Variables)
```css
:root {
  /* Colors */
  --color-primary: #3b82f6;
  --color-primary-dark: #2563eb;
  --color-secondary: #8b5cf6;

  /* Spacing scale */
  --space-1: 0.25rem;
  --space-2: 0.5rem;
  --space-3: 0.75rem;
  --space-4: 1rem;
  --space-6: 1.5rem;
  --space-8: 2rem;

  /* Typography */
  --font-sans: system-ui, sans-serif;
  --font-mono: 'Courier New', monospace;

  /* Shadows */
  --shadow-sm: 0 1px 2px rgba(0, 0, 0, 0.05);
  --shadow-md: 0 4px 6px rgba(0, 0, 0, 0.1);
  --shadow-lg: 0 10px 20px rgba(0, 0, 0, 0.15);
}

/* Dark mode */
@media (prefers-color-scheme: dark) {
  :root {
    --color-bg: #1a1a1a;
    --color-text: #f5f5f5;
  }
}
```

### Aspect Ratio
```css
.video-container {
  aspect-ratio: 16 / 9;
}

.square {
  aspect-ratio: 1;
}
```

### Logical Properties
```css
/* Instead of margin-left/right */
.element {
  margin-inline: auto;
  padding-inline: 2rem;
  padding-block: 1rem;
}

/* Border */
.box {
  border-inline-start: 3px solid var(--color-primary);
}
```

### Gap (Flexbox & Grid)
```css
.flex-container {
  display: flex;
  gap: 1rem; /* Better than margin */
}

.grid-container {
  display: grid;
  gap: 2rem 1rem; /* row gap, column gap */
}
```

### Clamp for Responsive Sizing
```css
.responsive-text {
  font-size: clamp(1rem, 2.5vw, 2rem);
  /* min, preferred, max */
}

.responsive-spacing {
  padding: clamp(1rem, 5vw, 4rem);
}
```
