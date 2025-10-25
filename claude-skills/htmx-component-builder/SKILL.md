---
name: htmx-component-builder
description: Generate production-ready HTMX components with matching Go handlers for interactive web UIs. Creates complete frontend-backend integrations with Korean text optimization, perfect for the Dark project's topic portals. Triggers include requests for "HTMX component", "interactive UI", "live search", "infinite scroll", or "dynamic content loading".
---

# HTMX Component Builder

Generate production-ready, interactive web components using HTMX with matching Go backend handlers. Optimized for server-side rendering, Korean text handling, and the Dark project architecture.

## Overview

This skill creates complete HTMX-powered interactive components including:
- **Frontend**: HTML with HTMX attributes for dynamic behavior
- **Backend**: Go handler functions for API endpoints
- **Korean Optimization**: IME handling, proper text display, localized messages
- **Dark Integration**: Works seamlessly with Dark project structure and CSS

## When to Use This Skill

Activate this skill when you need to:
- "Add live search to my website"
- "Create infinite scroll for content lists"
- "Build an HTMX component for [feature]"
- "Make this form submit without page reload"
- "Add dynamic content loading"
- "Convert static page to interactive HTMX"

## Component Catalog

### 🟢 Simple Components (Quick Wins)
**Use when:** Need basic interactivity with minimal complexity

- **HX-Boosted Links** - Progressive enhancement for navigation
- **Inline Edit** - Click-to-edit text fields
- **Delete Confirmation** - Confirm before delete action
- **Toggle Visibility** - Show/hide content sections
- **Live Badges** - Auto-updating status indicators

### 🟡 Medium Components (High Value)
**Use when:** Building core interactive features

- **Live Search** - Real-time search as user types
- **Pagination** - Server-rendered pagination controls
- **Tab Navigation** - Dynamic tab content loading
- **Dropdown Menu** - Ajax-loaded dropdown options
- **Sort/Filter** - Interactive content sorting/filtering

### 🔴 Complex Components (Advanced)
**Use when:** Need sophisticated interactions

- **Infinite Scroll** - Load more content on scroll
- **Multi-Step Form** - Wizard with server validation
- **Real-Time Updates** - Server-sent events or polling
- **Drag-Drop Sort** - Reorderable lists with persistence
- **Autocomplete** - Smart search with suggestions

## Workflow

### Step 1: Choose Component Type

**Question:** What kind of interaction do you need?

```
Search functionality? → Live Search component
Long content lists? → Infinite Scroll component
Form submission? → Form Validation component
Modal dialogs? → Modal component
Custom interaction? → Analyze requirements → Generate custom component
```

### Step 2: Generate Component

Use `generate_component.py`:

```bash
python scripts/generate_component.py \
  --type [component-type] \
  --name [component-name] \
  --korean \           # Include Korean optimizations
  --go-handler \       # Generate Go handler code
  --output [path]      # Output directory
```

**Component Types:**
- `search` - Live search with debouncing
- `infinite-scroll` - Infinite scroll loading
- `modal` - Modal dialog system
- `form` - Server-validated form
- `pagination` - Pagination controls
- `tabs` - Tab navigation
- `inline-edit` - Inline editing
- `delete-confirm` - Delete confirmation
- `toggle` - Toggle visibility
- `dropdown` - Ajax dropdown
- `sort-filter` - Sort/filter controls
- `autocomplete` - Autocomplete search
- `drag-drop` - Drag-drop sorting
- `realtime` - Real-time updates

### Step 3: Integrate with Project

**For Dark Project:**

1. **Add component template**
   - Place in `web/templates/components/`
   - Include in parent template: `{{template "component-name" .}}`

2. **Add Go handler**
   - Place in `cmd/web/handlers/`
   - Add route to `main.go`:
     ```go
     mux.Get("/api/[endpoint]", handlers.[HandlerName])
     ```

3. **Test component**
   - Use generated `test-[component].html` for visual testing
   - Test with real Dark data

### Step 4: Customize & Refine

**Common Customizations:**
- Adjust debounce timing for search
- Change loading indicators
- Modify error messages
- Update CSS classes
- Add custom HTMX headers

## Korean Optimization Features

### Input Method Editor (IME) Handling

**Problem:** Korean Hangul composition causes premature AJAX requests

**Solution:** Proper event handling for `compositionstart`/`compositionend`

```javascript
// Generated code includes IME-aware debouncing
let isComposing = false;
input.addEventListener('compositionstart', () => isComposing = true);
input.addEventListener('compositionend', () => isComposing = false);
input.addEventListener('input', (e) => {
  if (!isComposing) {
    // Trigger HTMX request
  }
});
```

### Text Display Optimization

**Korean-specific CSS:**
```css
.korean-text {
  word-break: keep-all;        /* Prevent breaking within words */
  letter-spacing: -0.3px;      /* Tighten letter spacing */
  line-height: 1.6;            /* Increase line height for readability */
}
```

### Localized Messages

**Loading States:**
- "로딩 중..." (Loading...)
- "저장 중..." (Saving...)
- "검색 중..." (Searching...)

**Error Messages:**
- "오류가 발생했습니다" (An error occurred)
- "다시 시도해주세요" (Please try again)

**Success Messages:**
- "저장되었습니다" (Saved)
- "완료되었습니다" (Completed)

### Date/Number Formatting

```go
// Generated handlers include Korean formatting
func formatKoreanDate(t time.Time) string {
    return t.Format("2006년 1월 2일")
}

func formatKoreanNumber(n int) string {
    return fmt.Sprintf("%s개", humanize.Comma(int64(n)))
}
```

## Dark Project Integration

### File Structure

**Templates:**
```
web/templates/
├── components/              # Generated HTMX components here
│   ├── search-live.html
│   ├── topic-scroll.html
│   └── content-modal.html
└── partials/                # Existing partials (reuse these!)
    ├── content-preview-regular.html
    ├── content-preview-featured.html
    └── content-meta.html
```

**Handlers:**
```
cmd/web/
├── main.go                  # Add routes here
└── handlers/                # Generated handlers here
    ├── search.go
    ├── content.go
    └── htmx_helpers.go      # Shared HTMX utilities
```

### Router Integration

```go
// cmd/web/main.go
func setupRoutes(mux *chi.Mux, handlers *Handlers) {
    // HTMX API endpoints
    mux.Get("/api/search", handlers.LiveSearch)
    mux.Get("/api/topics/{slug}/content", handlers.LoadMoreContent)
    mux.Post("/api/content/{id}/delete", handlers.DeleteContent)

    // ... other routes
}
```

### CSS Integration

Generated components use `dark-v2.css` classes:

```html
<!-- HTMX component with Dark CSS -->
<div class="content-preview korean-text"
     hx-get="/api/content/123"
     hx-trigger="click"
     hx-target="#content-detail">
    <h3 class="content-title-single-line">{{.Title}}</h3>
</div>

<!-- Loading indicator -->
<div class="htmx-indicator korean-text" id="loading">
    로딩 중...
</div>
```

**HTMX-specific CSS (auto-generated):**
```css
.htmx-indicator {
    display: none;
    opacity: 0;
    transition: opacity var(--transition-base);
}

.htmx-request .htmx-indicator {
    display: block;
    opacity: 1;
}

.htmx-swapping {
    opacity: 0;
    transition: opacity var(--transition-fast);
}

.htmx-settling {
    opacity: 1;
}
```

## Common Patterns

### Pattern 1: Live Search (Dark Header)

**Use Case:** Add live search to Dark's header search bar

**Generate:**
```bash
python scripts/generate_component.py \
  --type search \
  --name header-search \
  --korean \
  --go-handler \
  --output /path/to/dark/web/templates/components/
```

**Result:**
- `components/header-search.html` - HTMX search component
- `handlers/search.go` - Go handler with search logic
- `test-header-search.html` - Test page

**Integration:**
```html
<!-- web/templates/layouts/header.html -->
{{template "header-search" .}}
```

### Pattern 2: Infinite Scroll (Topic Lists)

**Use Case:** Load more content as user scrolls topic groups

**Generate:**
```bash
python scripts/generate_component.py \
  --type infinite-scroll \
  --name topic-content \
  --korean \
  --go-handler \
  --output /path/to/dark/web/templates/components/
```

**Result:**
- `components/topic-content-scroll.html` - Scroll container
- `handlers/content.go` - Pagination handler
- `test-topic-content-scroll.html` - Test page

**Integration:**
```html
<!-- web/templates/home.html -->
<div class="topic-groups-masonry">
    {{template "topic-content-scroll" .}}
</div>
```

### Pattern 3: Modal Content Detail

**Use Case:** Show content details in modal without page reload

**Generate:**
```bash
python scripts/generate_component.py \
  --type modal \
  --name content-detail \
  --korean \
  --go-handler \
  --output /path/to/dark/web/templates/components/
```

**Result:**
- `components/content-detail-modal.html` - Modal structure
- `handlers/content_detail.go` - Content loading handler
- `test-content-detail-modal.html` - Test page

**Integration:**
```html
<!-- Trigger modal from content list -->
<a href="/content/{{.ID}}"
   hx-get="/api/content/{{.ID}}"
   hx-target="#modal-container"
   hx-swap="innerHTML">
    {{.Title}}
</a>
```

## Advanced Techniques

### Out-of-Band Swaps

Update multiple page sections with single request:

```html
<!-- Component that updates sidebar too -->
<div id="content" hx-swap-oob="true">
    <article>{{.Content}}</article>
</div>
<div id="sidebar" hx-swap-oob="true">
    <div>{{.RelatedContent}}</div>
</div>
```

### Request Headers & Custom Events

```go
// Go handler with custom HTMX headers
func (h *Handler) DeleteContent(w http.ResponseWriter, r *http.Request) {
    // ... delete logic ...

    // Trigger client-side event
    w.Header().Set("HX-Trigger", `{"contentDeleted": {"id": "123"}}`)

    // Redirect after delete
    w.Header().Set("HX-Redirect", "/topics/topic-a")
}
```

### Loading States & Indicators

```html
<!-- Multiple loading indicators -->
<div hx-get="/api/search"
     hx-indicator="#search-loading, #global-loading">
    <input type="text" name="q">
</div>

<div id="search-loading" class="htmx-indicator korean-text">
    검색 중...
</div>
```

### Optimistic UI Updates

```html
<!-- Show success state immediately -->
<button hx-post="/api/like"
        hx-swap="outerHTML settle:100ms"
        class="btn-primary">
    좋아요
</button>
```

## Troubleshooting

### Component Not Loading

**Check:**
1. HTMX library loaded: `<script src="/static/js/vendor/htmx.min.js"></script>`
2. Handler route registered in `main.go`
3. Handler returns correct content-type: `text/html`
4. Browser console for errors

### Korean Input Issues

**Check:**
1. IME handling script included
2. Debounce timing appropriate (500ms+ for Korean)
3. `compositionstart`/`compositionend` events working

### Infinite Scroll Not Triggering

**Check:**
1. `hx-trigger="revealed"` attribute present
2. Viewport detection working (test with `threshold` attribute)
3. Next page URL correct
4. Loading indicator showing

### HTMX Headers Not Working

**Check:**
1. Request has `HX-Request: true` header
2. Response headers set correctly (`HX-Trigger`, etc.)
3. Handler detects HTMX request properly

## Resources

### Scripts
- **`scripts/generate_component.py`** - Main component generator
- **`scripts/analyze_templates.py`** - Find HTMX conversion opportunities
- **`scripts/test_component.py`** - Generate test pages

### References
- **`references/htmx_patterns.md`** - Complete HTMX pattern library (50+ examples)
- **`references/go_handlers.md`** - Go backend patterns (20+ examples)
- **`references/korean_optimization.md`** - Korean-specific optimizations
- **`references/dark_integration.md`** - Dark project integration guide

### Assets
- **`assets/components/`** - 15 ready-to-use HTML components
- **`assets/handlers/`** - 3 Go handler templates
- **`assets/examples/`** - Test pages for visual testing

## Tips for Success

1. **Start Simple** - Begin with basic components (inline edit, delete confirm) before complex ones
2. **Test Incrementally** - Use generated test pages to verify before integrating
3. **Reuse Partials** - Leverage existing Dark templates (content-preview, etc.)
4. **Korean Testing** - Test with real Korean text, not just Lorem Ipsum
5. **Progressive Enhancement** - Ensure components work without JavaScript
6. **Monitor Network** - Use browser devtools to debug HTMX requests
7. **Use Indicators** - Always show loading states for better UX
8. **Handle Errors** - Return proper error HTML with Korean messages

## Quick Reference

### Component Generation
```bash
# Simple component
python scripts/generate_component.py --type inline-edit --name post-title

# Medium component with Korean + Go
python scripts/generate_component.py --type search --name topic-search --korean --go-handler

# Complex component with everything
python scripts/generate_component.py --type infinite-scroll --name content-list --korean --go-handler --output /path/to/project/
```

### Template Analysis
```bash
# Find HTMX opportunities
python scripts/analyze_templates.py --path /path/to/templates/

# Get priority recommendations
python scripts/analyze_templates.py --path /path/to/templates/ --priority
```

### Test Page Generation
```bash
# Visual test page
python scripts/test_component.py --component search --output test-search.html
```

---

**Version:** 1.0.0
**Created:** 2025-10-25
**Optimized For:** Dark Project, Korean Text, Go + HTMX Stack
