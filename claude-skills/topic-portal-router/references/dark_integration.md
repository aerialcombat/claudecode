# Dark Project Integration Guide

## Architecture Overview

Dark is a Go-based topic portal platform with the following structure:

```
cmd/web/          - Web server binary
  main.go         - Server initialization and routing

internal/
  content/        - Content domain logic
    repository.go - Content data access

web/
  templates/      - Go html/templates
  static/         - CSS, JS, images
```

## Current Routing Structure

Dark uses Chi router (v5) for HTTP routing. Current structure in `cmd/web/main.go`:

```go
router := chi.NewRouter()

// Middleware
router.Use(middleware.Logger)
router.Use(middleware.Recoverer)

// Static files
router.Handle("/static/*", http.StripPrefix("/static/", http.FileServer(http.Dir("web/static"))))

// Pages
router.Get("/", ws.handleHome)
router.Get("/topics/{slug}", ws.handleTopicPage)

// HTMX API routes
router.Get("/api/topics/{slug}/tree", ws.handleTopicTree)
router.Get("/api/topics/{slug}/switch", ws.handleTopicSwitch)
```

## WebServer Structure

```go
type WebServer struct {
    repo        content.Repository  // Database access
    templates   *template.Template  // Go templates
    hotReload   bool               // Dev mode template reload
}
```

## Template Loading

Templates are loaded from `web/templates/`:

```go
templates := template.New("").Funcs(funcMap)
templates, err = templates.ParseGlob("web/templates/*.html")
templates, err = templates.ParseGlob("web/templates/partials/*.html")
templates, err = templates.ParseGlob("web/templates/components/*.html")
```

## Database Access

Content repository interface (in `internal/content/repository.go`):

```go
type Repository interface {
    GetTopicBySlug(ctx context.Context, slug string) (domain.Topic, error)
    ListTopics(ctx context.Context, limit, offset int) ([]domain.Topic, int, error)
    GetTopicContent(ctx context.Context, topicID int64, limit, offset int) ([]domain.Content, error)
    // ... other methods
}
```

## Topic Model

```go
type Topic struct {
    ID          int64
    Name        string
    Slug        string
    Description string
    CreatedAt   time.Time
    UpdatedAt   time.Time
}
```

## Integration Points for Subdomain Routing

### 1. Add Middleware

In `cmd/web/main.go`, add subdomain middleware before routes:

```go
router.Use(middleware.SubdomainExtractor)
```

### 2. Add Portal Route

```go
router.Get("/", ws.handlePortal)
```

### 3. Handler Implementation

```go
func (ws *WebServer) handlePortal(w http.ResponseWriter, r *http.Request) {
    subdomain, ok := middleware.GetSubdomain(r)
    if !ok || subdomain == "" {
        // No subdomain - show main landing page
        ws.handleHome(w, r)
        return
    }

    // Subdomain present - load topic portal
    // This will integrate with cache layer
    ws.handleTopicPortal(w, r, subdomain)
}
```

## Caching Integration Points

When cache layer is added, the flow will be:

```
Request → SubdomainExtractor → CacheCheck → BuildPortal → CacheStore → Response
```

Cache middleware will:
1. Extract subdomain
2. Generate cache key: `portal:{slug}`
3. Check cache (Redis)
4. If miss, call next handler
5. Cache response before returning

## Environment Variables

Dark uses environment variables for configuration (parsed in `shared/env/`):

- `PORT` - Server port (default: 8085)
- `DB_*` - Database connection settings
- `LOG_LEVEL` - Logging level
- `HOT_RELOAD` - Template hot reload for dev

For cache integration, will add:
- `REDIS_ADDR` - Redis address
- `CACHE_TTL` - Cache expiration time
- `CACHE_ENABLED` - Enable/disable caching

## Observability

Dark implements structured logging with mojilog:

```go
mojilog.Info("Portal request",
    "subdomain", subdomain,
    "request_id", requestID,
)
```

All portal handlers should log:
- Subdomain/slug
- Cache hit/miss
- Topic found/not found
- Build time
- Request ID for tracing

## Error Handling

Standard error responses:

```go
// Topic not found
http.Error(w, "Topic not found", http.StatusNotFound)

// Invalid subdomain
http.Error(w, "Invalid subdomain", http.StatusBadRequest)

// Internal error
http.Error(w, "Internal server error", http.StatusInternalServerError)
mojilog.Error("Error building portal", "error", err, "subdomain", subdomain)
```

## Testing Approach

Dark uses table-driven tests with testcontainers for integration tests:

```go
func TestSubdomainExtraction(t *testing.T) {
    tests := []struct {
        name       string
        host       string
        wantSubdomain string
    }{
        {"with subdomain", "golf.example.com", "golf"},
        {"with port", "golf.example.com:8080", "golf"},
        {"localhost", "localhost:8080", ""},
        {"www", "www.example.com", ""},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            // Test implementation
        })
    }
}
```
