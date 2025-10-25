---
name: topic-portal-router
description: Generate Go Chi router infrastructure for subdomain-based topic portals. Use when implementing wildcard subdomain routing (e.g., golf.mydomain.com → golf topic portal) with subdomain extraction, topic validation, 404 handling, and cache integration points. Designed for Dark's Go web server architecture.
---

# Topic Portal Router

## Overview

Generate complete subdomain routing infrastructure for topic-based portals using Go and Chi router. Enable dynamic subdomain-to-topic mapping where visiting `{topic}.domain.com` loads a portal for that topic (e.g., `golf.mydomain.com` → golf topic portal, `tigerwoods.mydomain.com` → tigerwoods topic portal).

## When to Use This Skill

Use when:
- Implementing wildcard subdomain routing for topic portals
- Need to extract topic slug from subdomain
- Building infrastructure that validates topics before rendering
- Preparing for Redis cache integration (creates integration points)
- Working with Go Chi router in Dark web server

Do not use when:
- Building path-based routing (`/topics/{slug}`) - use standard Chi patterns
- Implementing non-topic subdomain routing (tenants, locales)
- Working with non-Go frameworks

## Quick Start

Generate subdomain routing infrastructure with three components:

1. **Middleware** - Extract subdomain from host, add to context
2. **Routes** - Wire portal handler into Chi router
3. **Handler** - Validate topic, handle 404s, prepare for caching

See detailed implementation steps below.

## Adding Subdomain Middleware

### Step 1: Create Middleware Package

Generate middleware code from the template in `assets/subdomain_middleware.go.template`:

```go
package middleware

import (
    "context"
    "net/http"
    "strings"
)

type ContextKey string

const (
    SubdomainKey ContextKey = "subdomain"
    CacheKeyKey ContextKey = "cache_key"
)

func SubdomainExtractor(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        host := r.Host
        if strings.Contains(host, ":") {
            host = strings.Split(host, ":")[0]
        }

        // Handle localhost (development)
        if host == "localhost" || strings.HasPrefix(host, "127.0.0.1") {
            next.ServeHTTP(w, r)
            return
        }

        // Extract subdomain
        parts := strings.Split(host, ".")
        var subdomain string
        if len(parts) > 2 {
            subdomain = parts[0]
        }

        if subdomain == "" || subdomain == "www" {
            next.ServeHTTP(w, r)
            return
        }

        ctx := context.WithValue(r.Context(), SubdomainKey, subdomain)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}

func GetSubdomain(r *http.Request) (string, bool) {
    subdomain, ok := r.Context().Value(SubdomainKey).(string)
    return subdomain, ok
}
```

### Step 2: Wire Middleware into Router

In Dark's `cmd/web/main.go`, add middleware before routes:

```go
router := chi.NewRouter()

// Existing middleware
router.Use(middleware.Logger)
router.Use(middleware.Recoverer)

// Add subdomain extractor
router.Use(middleware.SubdomainExtractor)

// Routes follow...
```

**See `references/chi_subdomain_patterns.md` for additional middleware patterns and variations.**

## Adding Portal Routes

### Modify Root Route

Update the root route handler to dispatch based on subdomain presence:

```go
// In cmd/web/main.go
router.Get("/", ws.handlePortalOrHome)
```

### Implement Dispatcher

```go
func (ws *WebServer) handlePortalOrHome(w http.ResponseWriter, r *http.Request) {
    subdomain, ok := middleware.GetSubdomain(r)
    if !ok || subdomain == "" {
        // No subdomain - show main landing page
        ws.handleHome(w, r)
        return
    }

    // Subdomain present - load topic portal
    ws.handleTopicPortal(w, r, subdomain)
}
```

## Implementing Portal Handler

### Basic Handler Structure

```go
func (ws *WebServer) handleTopicPortal(w http.ResponseWriter, r *http.Request, slug string) {
    ctx := r.Context()

    // 1. Validate topic exists
    topic, err := ws.repo.GetTopicBySlug(ctx, slug)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            http.Error(w, "Topic not found", http.StatusNotFound)
            return
        }
        mojilog.Error("Error fetching topic", "error", err, "slug", slug)
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    // 2. Build portal data (placeholder for cache integration)
    portalData := ws.buildPortalData(ctx, topic)

    // 3. Render template
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    if err := ws.getTemplates().ExecuteTemplate(w, "topic-portal", portalData); err != nil {
        mojilog.Error("Error rendering portal", "error", err, "slug", slug)
        http.Error(w, "Internal server error", http.StatusInternalServerError)
        return
    }

    mojilog.Info("Portal served", "slug", slug, "topic_id", topic.ID)
}
```

### Build Portal Data Method

Create placeholder for portal data assembly:

```go
func (ws *WebServer) buildPortalData(ctx context.Context, topic domain.Topic) map[string]interface{} {
    // TODO: This is where graph traversal and content selection will happen
    // For now, return basic topic data

    return map[string]interface{}{
        "Title":       topic.Name,
        "Topic":       topic,
        "Contents":    []domain.Content{},
        "Subtopics":   []domain.Topic{},
    }
}
```

**Note:** The `buildPortalData` method is the integration point for:
- Graph traversal (next skill: Graph Scoring Builder)
- Content ranking (later skill: Content Ranker)
- Cache storage (next skill: Portal Cache Manager)

## Cache Integration Points

Prepare for cache integration by adding cache key context:

```go
func (ws *WebServer) handleTopicPortal(w http.ResponseWriter, r *http.Request, slug string) {
    ctx := r.Context()

    // Add cache key to context for future cache integration
    cacheKey := fmt.Sprintf("portal:%s", slug)
    ctx = context.WithValue(ctx, middleware.CacheKeyKey, cacheKey)

    // ... rest of handler
}
```

When cache skill is added, it will:
1. Check Redis using cache key
2. Return cached data if available
3. Call `buildPortalData` on cache miss
4. Store result in Redis with TTL

## Error Handling

Implement consistent error responses:

### Topic Not Found (404)

```go
if errors.Is(err, sql.ErrNoRows) {
    http.Error(w, "Topic not found", http.StatusNotFound)
    mojilog.Info("Topic not found", "slug", slug)
    return
}
```

### Invalid Subdomain (400)

```go
if !isValidSlug(subdomain) {
    http.Error(w, "Invalid subdomain format", http.StatusBadRequest)
    mojilog.Warn("Invalid subdomain", "subdomain", subdomain)
    return
}
```

### Internal Errors (500)

```go
mojilog.Error("Error building portal", "error", err, "slug", slug)
http.Error(w, "Internal server error", http.StatusInternalServerError)
```

## Testing

### Table-Driven Tests

Generate tests for subdomain extraction:

```go
func TestSubdomainExtraction(t *testing.T) {
    tests := []struct {
        name          string
        host          string
        wantSubdomain string
        wantOK        bool
    }{
        {"valid subdomain", "golf.example.com", "golf", true},
        {"with port", "golf.example.com:8080", "golf", true},
        {"localhost", "localhost:8080", "", false},
        {"www", "www.example.com", "", false},
        {"no subdomain", "example.com", "", false},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", "http://"+tt.host+"/", nil)

            var gotSubdomain string
            var gotOK bool

            handler := middleware.SubdomainExtractor(http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
                gotSubdomain, gotOK = middleware.GetSubdomain(r)
            }))

            handler.ServeHTTP(httptest.NewRecorder(), req)

            if gotSubdomain != tt.wantSubdomain {
                t.Errorf("got subdomain %q, want %q", gotSubdomain, tt.wantSubdomain)
            }
            if gotOK != tt.wantOK {
                t.Errorf("got ok %v, want %v", gotOK, tt.wantOK)
            }
        })
    }
}
```

### Integration Tests

Generate integration tests for portal handler:

```go
func TestPortalHandler(t *testing.T) {
    // Setup test database with topics
    repo := setupTestRepo(t)
    ws := &WebServer{repo: repo}

    tests := []struct {
        name       string
        subdomain  string
        wantStatus int
    }{
        {"existing topic", "golf", http.StatusOK},
        {"non-existent topic", "notfound", http.StatusNotFound},
        {"empty subdomain", "", http.StatusOK}, // Falls back to home
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            req := httptest.NewRequest("GET", "/", nil)
            if tt.subdomain != "" {
                ctx := context.WithValue(req.Context(), middleware.SubdomainKey, tt.subdomain)
                req = req.WithContext(ctx)
            }

            rr := httptest.NewRecorder()
            ws.handlePortalOrHome(rr, req)

            if rr.Code != tt.wantStatus {
                t.Errorf("got status %d, want %d", rr.Code, tt.wantStatus)
            }
        })
    }
}
```

## Resources

### references/

- **chi_subdomain_patterns.md** - Comprehensive Chi router patterns for subdomain extraction, validation, and error handling
- **dark_integration.md** - Dark project architecture, current routing structure, database access patterns, and integration points

### assets/

- **subdomain_middleware.go.template** - Complete Go middleware template for subdomain extraction and context management

## Development vs Production

### Development (localhost)

Middleware automatically skips subdomain extraction for localhost:

```bash
# No subdomain routing
http://localhost:8085/

# For local testing with subdomains, use /etc/hosts:
127.0.0.1  golf.localhost
127.0.0.1  tigerwoods.localhost
```

### Production

Configure DNS with wildcard A record:

```
*.yourdomain.com  →  Your server IP
```

Then deploy with proper domain environment variable if needed.

## Next Steps

After implementing subdomain routing:

1. **Graph Scoring Builder** - Implement weighted topic collection
2. **Portal Cache Manager** - Add Redis caching layer
3. **Content Ranker** - Multi-factor content selection
4. Create topic portal template (`topic-portal.html`)
5. Add observability (Prometheus metrics, OpenTelemetry traces)

The subdomain router creates the foundation; subsequent skills build the portal data pipeline.
