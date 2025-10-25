# Chi Router Subdomain Patterns

## Subdomain Extraction

### Using Middleware

The most common pattern is to extract the subdomain in middleware and add it to the request context:

```go
func SubdomainMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        host := r.Host
        // Remove port if present
        if strings.Contains(host, ":") {
            host = strings.Split(host, ":")[0]
        }

        // Extract subdomain
        parts := strings.Split(host, ".")
        var subdomain string
        if len(parts) > 2 {
            subdomain = parts[0]
        }

        // Add to context
        ctx := context.WithValue(r.Context(), "subdomain", subdomain)
        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

### Using Route Groups

Chi supports route groups with conditions:

```go
router.Group(func(r chi.Router) {
    r.Use(SubdomainMiddleware)
    r.Get("/", handlePortalHome)
    r.Get("/content", handlePortalContent)
})
```

## Context Access Pattern

Retrieve subdomain in handlers:

```go
func handlePortalHome(w http.ResponseWriter, r *http.Request) {
    subdomain, ok := r.Context().Value("subdomain").(string)
    if !ok || subdomain == "" {
        http.Error(w, "No subdomain", http.StatusBadRequest)
        return
    }

    // Use subdomain (e.g., as topic slug)
    // ...
}
```

## Subdomain Validation

Pattern for validating subdomains before processing:

```go
func ValidateSubdomain(allowedPattern *regexp.Regexp) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            subdomain := r.Context().Value("subdomain").(string)

            if subdomain == "" {
                // No subdomain - could be main domain
                next.ServeHTTP(w, r)
                return
            }

            if !allowedPattern.MatchString(subdomain) {
                http.Error(w, "Invalid subdomain", http.StatusBadRequest)
                return
            }

            next.ServeHTTP(w, r)
        })
    }
}
```

## Development vs Production

Handle different domain structures:

```go
func extractSubdomain(host string) string {
    // Remove port
    if strings.Contains(host, ":") {
        host = strings.Split(host, ":")[0]
    }

    // Handle localhost (development)
    if host == "localhost" || strings.HasPrefix(host, "127.0.0.1") {
        return ""
    }

    // Extract subdomain
    parts := strings.Split(host, ".")
    if len(parts) > 2 {
        return parts[0]
    }
    return ""
}
```

## Combining with Cache Layer

Pattern for cache integration:

```go
func SubdomainWithCache(cache Cache) func(http.Handler) http.Handler {
    return func(next http.Handler) http.Handler {
        return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
            subdomain := extractSubdomain(r.Host)

            if subdomain == "" {
                next.ServeHTTP(w, r)
                return
            }

            // Check cache
            cacheKey := fmt.Sprintf("portal:%s", subdomain)
            if cached, err := cache.Get(cacheKey); err == nil {
                w.Write(cached)
                return
            }

            // Add subdomain to context for handler
            ctx := context.WithValue(r.Context(), "subdomain", subdomain)
            ctx = context.WithValue(ctx, "cache_key", cacheKey)
            next.ServeHTTP(w, r.WithContext(ctx))
        })
    }
}
```

## Error Handling

Pattern for 404 handling when topic doesn't exist:

```go
func handlePortal(w http.ResponseWriter, r *http.Request) {
    subdomain := r.Context().Value("subdomain").(string)

    // Validate topic exists
    topic, err := repo.GetTopicBySlug(r.Context(), subdomain)
    if err != nil {
        if errors.Is(err, sql.ErrNoRows) {
            http.Error(w, "Topic not found", http.StatusNotFound)
            return
        }
        http.Error(w, "Internal error", http.StatusInternalServerError)
        return
    }

    // Build and serve portal
    // ...
}
```
