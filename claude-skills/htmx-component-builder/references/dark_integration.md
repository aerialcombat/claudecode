# Dark Project Integration Guide

Complete guide to integrating HTMX components with the Dark topic portal platform.

## Table of Contents

1. [Dark Project Overview](#dark-project-overview)
2. [Project Structure](#project-structure)
3. [Template Integration](#template-integration)
4. [Handler Integration](#handler-integration)
5. [Router Configuration](#router-configuration)
6. [CSS Integration](#css-integration)
7. [Common Patterns](#common-patterns)
8. [Testing](#testing)
9. [Deployment](#deployment)

---

## Dark Project Overview

### Architecture
Dark is a Go-based topic portal platform with:
- **Frontend**: Go templates + HTMX + dark-v2.css
- **Backend**: Go 1.25.1 with chi router
- **Database**: PostgreSQL with JSONB
- **Message Queue**: NATS
- **Style**: Korean-optimized, Naver News inspired

### Tech Stack
- **Language**: Go 1.25.1 (module: ananti/life/dark)
- **Router**: chi (v5)
- **Templates**: Go html/template with HTMX attributes
- **CSS**: dark-v2.css (custom, responsive, Korean-optimized)
- **Observability**: mojilog + Prometheus + Tempo

---

## Project Structure

### Directory Layout
```
dark/
├── cmd/
│   ├── web/                    # Web server (main entry point)
│   │   ├── main.go            # Server setup + routes
│   │   └── handlers/          # HTMX handler functions
│   ├── content-api/           # REST API server
│   └── consumer/              # NATS consumer
├── internal/
│   ├── content/               # Content domain logic
│   ├── domain/                # Business entities
│   └── shared/                # Shared utilities
├── web/
│   ├── templates/             # Go HTML templates
│   │   ├── layouts/           # Page layouts
│   │   ├── partials/          # Reusable components
│   │   ├── components/        # HTMX components (ADD HERE)
│   │   └── pages/             # Full page templates
│   └── static/
│       ├── css/
│       │   └── dark-v2.css    # Main stylesheet
│       ├── js/
│       │   └── vendor/
│       │       └── htmx.min.js
│       └── images/
└── docs/
    └── CLAUDE.md              # AI assistant guide
```

### File Locations for HTMX Components

**Templates**: `web/templates/components/`
- Component HTML with HTMX attributes
- Partial templates for reuse
- Example: `search-live.html`, `topic-scroll.html`

**Handlers**: `cmd/web/handlers/`
- Go handler functions for HTMX endpoints
- Example: `search.go`, `content.go`

**Routes**: `cmd/web/main.go`
- API route definitions
- Middleware configuration

**CSS**: `web/static/css/dark-v2.css`
- Existing styles to use
- Add HTMX-specific styles here

**JavaScript**: `web/static/js/`
- HTMX library (already included)
- Custom scripts (Korean IME handlers, etc.)

---

## Template Integration

### Pattern 1: Create HTMX Component Template

**Location**: `web/templates/components/search-live.html`

```html
{{define "search-live"}}
<div class="search-container">
    <form class="search-form">
        <input type="text"
               id="search-input"
               name="q"
               class="search-input korean-text"
               hx-get="/api/search"
               hx-trigger="keyup changed delay:500ms"
               hx-target="#search-results"
               hx-indicator="#search-loading"
               placeholder="검색어를 입력하세요"
               value="{{.Query}}"
               autocomplete="off">

        <span id="search-loading" class="loading-indicator htmx-indicator">
            검색 중...
        </span>
    </form>

    <div id="search-results" class="search-results">
        {{if .Results}}
            {{template "search-results" .}}
        {{end}}
    </div>
</div>

<script>
// Korean IME handling
(function() {
    let isComposing = false;
    const input = document.getElementById('search-input');

    input.addEventListener('compositionstart', () => {
        isComposing = true;
    });

    input.addEventListener('compositionend', () => {
        isComposing = false;
        htmx.trigger(input, 'keyup');
    });

    input.addEventListener('keyup', (e) => {
        if (isComposing) {
            e.stopPropagation();
            return false;
        }
    });
})();
</script>
{{end}}

{{define "search-results"}}
{{range .Results}}
<div class="search-result-item">
    <a href="/topics/{{.TopicSlug}}/content/{{.ID}}" class="content-link">
        <h3 class="content-title-single-line">{{.Title}}</h3>
        <p class="content-excerpt">{{.Excerpt}}</p>
        <div class="content-meta korean-text">
            <span class="meta-source">{{.Source}}</span>
            <span class="meta-separator">·</span>
            <span class="meta-date">{{.FormattedDate}}</span>
        </div>
    </a>
</div>
{{end}}
{{end}}
```

### Pattern 2: Include Component in Page

**Location**: `web/templates/pages/home.html`

```html
{{define "home"}}
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dark - {{.Title}}</title>
    <link rel="stylesheet" href="/static/css/dark-v2.css">
    <script src="/static/js/vendor/htmx.min.js"></script>
</head>
<body>
    {{template "header" .}}

    <main class="main-content">
        <!-- Include HTMX search component -->
        {{template "search-live" .Search}}

        <div class="topic-groups">
            {{range .TopicGroups}}
                {{template "topic-group" .}}
            {{end}}
        </div>
    </main>

    {{template "footer" .}}
</body>
</html>
{{end}}
```

### Pattern 3: Reuse Existing Partials

**Location**: Dark already has useful partials in `web/templates/partials/`

```html
{{define "content-preview-regular"}}
<!-- Use existing content preview partial -->
<a href="/topics/{{.TopicSlug}}/content/{{.ID}}" class="content-link">
    {{if .ImageURL}}
    <div class="content-thumbnail">
        <img src="{{.ImageURL}}" alt="{{.Title}}">
    </div>
    {{end}}
    <div class="content-text">
        <h3 class="content-title-single-line">{{.Title}}</h3>
        <p class="content-excerpt">{{.Excerpt}}</p>
        {{template "content-meta" .}}
    </div>
</a>
{{end}}
```

**In HTMX component**: Reuse these partials in HTMX responses

```html
{{define "content-list-partial"}}
{{range .Items}}
    {{template "content-preview-regular" .}}
{{end}}
{{end}}
```

---

## Handler Integration

### Pattern 4: Create HTMX Handler

**Location**: `cmd/web/handlers/search.go`

```go
package handlers

import (
    "net/http"
    "html/template"
    "strings"

    "ananti/life/dark/internal/content"
)

type SearchHandler struct {
    contentRepo content.Repository
    templates   *template.Template
}

func NewSearchHandler(repo content.Repository, templates *template.Template) *SearchHandler {
    return &SearchHandler{
        contentRepo: repo,
        templates:   templates,
    }
}

// LiveSearch handles HTMX live search requests
func (h *SearchHandler) LiveSearch(w http.ResponseWriter, r *http.Request) {
    query := strings.TrimSpace(r.URL.Query().Get("q"))

    // Empty query returns empty results
    if query == "" {
        w.Header().Set("Content-Type", "text/html; charset=utf-8")
        w.Write([]byte(""))
        return
    }

    // Minimum 1 character for Korean (1 character = meaningful)
    if len([]rune(query)) < 1 {
        w.Header().Set("Content-Type", "text/html; charset=utf-8")
        w.Write([]byte(`<div class="hint korean-text">검색어를 입력하세요</div>`))
        return
    }

    // Search database
    results, err := h.contentRepo.Search(r.Context(), query, 20)
    if err != nil {
        http.Error(w, "검색 중 오류가 발생했습니다", http.StatusInternalServerError)
        return
    }

    // Format dates for display
    for i := range results {
        results[i].FormattedDate = formatKoreanRelativeTime(results[i].PublishedAt)
    }

    data := map[string]interface{}{
        "Query":   query,
        "Results": results,
        "Count":   len(results),
    }

    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    h.templates.ExecuteTemplate(w, "search-results", data)
}

// Helper function for Korean date formatting
func formatKoreanRelativeTime(t time.Time) string {
    now := time.Now()
    diff := now.Sub(t)

    switch {
    case diff < time.Minute:
        return "방금 전"
    case diff < time.Hour:
        return fmt.Sprintf("%d분 전", int(diff.Minutes()))
    case diff < 24*time.Hour:
        return fmt.Sprintf("%d시간 전", int(diff.Hours()))
    case diff < 30*24*time.Hour:
        return fmt.Sprintf("%d일 전", int(diff.Hours()/24))
    default:
        return t.Format("2006년 1월 2일")
    }
}
```

### Pattern 5: Infinite Scroll Handler

**Location**: `cmd/web/handlers/content.go`

```go
package handlers

import (
    "net/http"
    "strconv"
    "html/template"

    "github.com/go-chi/chi/v5"
    "ananti/life/dark/internal/content"
)

type ContentHandler struct {
    contentRepo content.Repository
    templates   *template.Template
}

func NewContentHandler(repo content.Repository, templates *template.Template) *ContentHandler {
    return &ContentHandler{
        contentRepo: repo,
        templates:   templates,
    }
}

// LoadMore handles infinite scroll requests
func (h *ContentHandler) LoadMore(w http.ResponseWriter, r *http.Request) {
    topicSlug := chi.URLParam(r, "slug")
    pageStr := r.URL.Query().Get("page")

    page, err := strconv.Atoi(pageStr)
    if err != nil || page < 1 {
        page = 1
    }

    perPage := 20
    offset := (page - 1) * perPage

    // Fetch content for topic
    items, total, err := h.contentRepo.GetByTopic(r.Context(), topicSlug, offset, perPage)
    if err != nil {
        http.Error(w, "콘텐츠를 불러올 수 없습니다", http.StatusInternalServerError)
        return
    }

    hasMore := offset+perPage < total
    nextPage := page + 1

    data := map[string]interface{}{
        "Items":     items,
        "HasMore":   hasMore,
        "NextPage":  nextPage,
        "TopicSlug": topicSlug,
    }

    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    h.templates.ExecuteTemplate(w, "content-infinite-scroll", data)
}
```

---

## Router Configuration

### Pattern 6: Register HTMX Routes

**Location**: `cmd/web/main.go`

```go
package main

import (
    "html/template"
    "log"
    "net/http"

    "github.com/go-chi/chi/v5"
    "github.com/go-chi/chi/v5/middleware"

    "ananti/life/dark/cmd/web/handlers"
    "ananti/life/dark/internal/content"
)

func main() {
    // Initialize dependencies
    db := setupDatabase()
    contentRepo := content.NewPostgresRepository(db)

    // Parse templates
    templates := template.Must(template.ParseGlob("web/templates/**/*.html"))

    // Initialize handlers
    searchHandler := handlers.NewSearchHandler(contentRepo, templates)
    contentHandler := handlers.NewContentHandler(contentRepo, templates)

    // Setup router
    r := chi.NewRouter()

    // Middleware
    r.Use(middleware.Logger)
    r.Use(middleware.Recoverer)
    r.Use(middleware.Compress(5))

    // Static files
    r.Handle("/static/*", http.StripPrefix("/static/",
        http.FileServer(http.Dir("web/static"))))

    // HTMX API routes
    r.Route("/api", func(r chi.Router) {
        // Search
        r.Get("/search", searchHandler.LiveSearch)

        // Content
        r.Get("/topics/{slug}/content/more", contentHandler.LoadMore)
        r.Get("/content/{id}", contentHandler.GetContent)
        r.Delete("/content/{id}", contentHandler.DeleteContent)

        // Other HTMX endpoints
        r.Get("/topics/{slug}/related", contentHandler.GetRelated)
    })

    // Regular page routes
    r.Get("/", pageHandler.Home)
    r.Get("/topics/{slug}", pageHandler.TopicPage)
    r.Get("/topics/{slug}/content/{id}", pageHandler.ContentDetail)

    // Start server
    log.Printf("Server starting on :8085")
    http.ListenAndServe(":8085", r)
}
```

---

## CSS Integration

### Pattern 7: Using dark-v2.css Classes

Dark already has comprehensive CSS. Use existing classes:

```html
<!-- Content previews -->
<div class="content-preview">
    <h3 class="content-title-single-line">Title</h3>
    <p class="content-excerpt">Excerpt text...</p>
</div>

<!-- Korean text -->
<div class="korean-text">한글 텍스트</div>

<!-- Metadata -->
<div class="content-meta">
    <span class="meta-source">Source</span>
    <span class="meta-separator">·</span>
    <span class="meta-date">1시간 전</span>
</div>

<!-- Buttons -->
<button class="btn-primary">주요 버튼</button>
<button class="btn-secondary">보조 버튼</button>

<!-- Forms -->
<input type="text" class="form-input">
<textarea class="form-textarea"></textarea>
```

### Pattern 8: Add HTMX-Specific Styles

**Location**: Add to `web/static/css/dark-v2.css`

```css
/* HTMX Loading Indicators */
.htmx-indicator {
    display: none;
    opacity: 0;
    transition: opacity var(--transition-base);
}

.htmx-request .htmx-indicator {
    display: block;
    opacity: 1;
}

.htmx-request.htmx-indicator {
    display: inline-block;
    opacity: 1;
}

/* HTMX Swapping Transitions */
.htmx-swapping {
    opacity: 0;
    transition: opacity var(--transition-fast);
}

.htmx-settling {
    opacity: 1;
    transition: opacity var(--transition-fast);
}

/* HTMX Added Elements (fade in) */
.htmx-added {
    animation: fadeIn var(--transition-base);
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

/* Search Results */
.search-results {
    margin-top: var(--spacing-4);
}

.search-result-item {
    padding: var(--spacing-3);
    border-bottom: 1px solid var(--color-border);
    transition: background-color var(--transition-fast);
}

.search-result-item:hover {
    background-color: var(--color-hover);
}

/* Loading Spinner */
.loading-indicator {
    display: inline-flex;
    align-items: center;
    gap: var(--spacing-2);
    color: var(--color-text-secondary);
    font-size: var(--font-size-sm);
}

.loading-indicator::before {
    content: "";
    width: 16px;
    height: 16px;
    border: 2px solid var(--color-border);
    border-top-color: var(--color-primary);
    border-radius: 50%;
    animation: spin 0.8s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

/* Infinite Scroll Trigger */
.load-more-trigger {
    padding: var(--spacing-4);
    text-align: center;
    color: var(--color-text-secondary);
}
```

---

## Common Patterns

### Pattern 9: Topic Content List with Infinite Scroll

**Template**: `web/templates/components/topic-content-scroll.html`

```html
{{define "topic-content-scroll"}}
<div class="topic-content-list" id="content-list-{{.TopicSlug}}">
    {{range .Items}}
        {{template "content-preview-regular" .}}
    {{end}}

    {{if .HasMore}}
    <div class="load-more-trigger"
         hx-get="/api/topics/{{.TopicSlug}}/content/more?page={{.NextPage}}"
         hx-trigger="revealed"
         hx-swap="outerHTML">
        <div class="loading-indicator htmx-indicator">
            더 불러오는 중...
        </div>
    </div>
    {{end}}
</div>
{{end}}
```

**Handler**: Already shown in Pattern 5

**Usage in page**:
```html
{{template "topic-content-scroll" .TopicContent}}
```

### Pattern 10: Modal Content Detail

**Template**: `web/templates/components/content-modal.html`

```html
{{define "content-modal"}}
<div class="modal-overlay" id="content-modal" onclick="closeModal()">
    <div class="modal-container" onclick="event.stopPropagation()">
        <div class="modal-header">
            <button class="modal-close" onclick="closeModal()">✕</button>
        </div>
        <div class="modal-body">
            <article class="content-detail korean-text">
                <h1>{{.Title}}</h1>

                <div class="content-meta">
                    <span class="meta-source">{{.Source}}</span>
                    <span class="meta-separator">·</span>
                    <span class="meta-date">{{.FormattedDate}}</span>
                </div>

                <div class="content-body">
                    {{.Content}}
                </div>

                {{if .RelatedContent}}
                <div class="related-content">
                    <h3>관련 콘텐츠</h3>
                    {{range .RelatedContent}}
                        {{template "content-preview-regular" .}}
                    {{end}}
                </div>
                {{end}}
            </article>
        </div>
    </div>
</div>

<script>
function closeModal() {
    document.getElementById('content-modal').remove();
}
</script>
{{end}}
```

**Trigger from list**:
```html
<a href="/topics/{{.TopicSlug}}/content/{{.ID}}"
   hx-get="/api/content/{{.ID}}"
   hx-target="body"
   hx-swap="beforeend">
    {{.Title}}
</a>
```

### Pattern 11: Delete with Confirmation

```html
<button class="btn-danger"
        hx-delete="/api/content/{{.ID}}"
        hx-confirm="이 콘텐츠를 삭제하시겠습니까?"
        hx-target="closest .content-item"
        hx-swap="outerHTML swap:300ms">
    삭제
</button>
```

**Handler**:
```go
func (h *ContentHandler) DeleteContent(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    err := h.contentRepo.Delete(r.Context(), id)
    if err != nil {
        http.Error(w, "삭제 실패", http.StatusInternalServerError)
        return
    }

    // Return empty response - HTMX will remove element
    w.Header().Set("HX-Trigger", `{"contentDeleted": {"id": "`+id+`"}}`)
    w.WriteHeader(http.StatusOK)
}
```

---

## Testing

### Pattern 12: Local Testing Setup

**1. Start Dark web server:**
```bash
cd dark
go run cmd/web/main.go
```

**2. Access at:** `http://localhost:8085`

**3. Test HTMX component:**
- Use browser DevTools Network tab
- Filter by "XHR" to see HTMX requests
- Check request/response headers
- Verify `HX-Request: true` header

**4. Test Korean IME:**
- Open browser console
- Type Korean in search input
- Watch for "Composition started/ended" logs
- Verify no premature requests during typing

### Pattern 13: Component Test Page

Create standalone test page: `web/templates/test/search-test.html`

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <title>Search Component Test</title>
    <link rel="stylesheet" href="/static/css/dark-v2.css">
    <script src="/static/js/vendor/htmx.min.js"></script>
</head>
<body>
    <div class="container">
        <h1>Search Component Test</h1>
        {{template "search-live" .}}
    </div>
</body>
</html>
```

Add test route:
```go
r.Get("/test/search", func(w http.ResponseWriter, r *http.Request) {
    templates.ExecuteTemplate(w, "search-test", nil)
})
```

---

## Deployment

### Pattern 14: Production Checklist

**Before deployment:**

1. **Minify HTMX**: Use minified version
2. **Test all HTMX endpoints**: Ensure proper error handling
3. **Verify Korean IME**: Test with real Korean input
4. **Check loading states**: All indicators working
5. **Test mobile**: Responsive behavior
6. **Validate HTML**: Use W3C validator
7. **Performance**: Check network waterfall
8. **Security**: Validate all user inputs

**Environment variables:**
```bash
export DARK_ENV=production
export DARK_WEB_PORT=8085
export DARK_DB_HOST=localhost
export DARK_DB_NAME=life
```

**Build and run:**
```bash
cd dark
go build -o bin/web cmd/web/main.go
./bin/web
```

---

## Quick Reference

### HTMX Component Checklist

- [ ] Template created in `web/templates/components/`
- [ ] Handler created in `cmd/web/handlers/`
- [ ] Route registered in `cmd/web/main.go`
- [ ] Korean IME handling added if text input
- [ ] Uses existing dark-v2.css classes
- [ ] Loading indicators implemented
- [ ] Error handling included
- [ ] Mobile responsive
- [ ] Tested locally

### Common Dark CSS Classes

| Class | Purpose |
|-------|---------|
| `.korean-text` | Korean-optimized text |
| `.content-preview` | Content card |
| `.content-title-single-line` | Title (ellipsis) |
| `.content-excerpt` | Excerpt text |
| `.content-meta` | Metadata row |
| `.btn-primary` | Primary button |
| `.btn-secondary` | Secondary button |
| `.form-input` | Text input |
| `.loading-indicator` | Loading state |

### HTMX Headers (Dark Handlers)

| Header | Usage |
|--------|-------|
| `Content-Type: text/html; charset=utf-8` | Always for HTML |
| `HX-Trigger: {"event": {}}` | Trigger client events |
| `HX-Redirect: /path` | Client-side redirect |
| `Vary: HX-Request` | Cache control |

---

**Version:** 1.0.0
**Last Updated:** 2025-10-25
**Dark Project Compatibility:** 0.2.0-mvp
