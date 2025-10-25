# Go Handler Patterns for HTMX

Complete guide to implementing Go backend handlers for HTMX applications with 20+ production-ready patterns.

## Table of Contents

1. [Handler Basics](#handler-basics)
2. [HTMX Detection](#htmx-detection)
3. [Response Patterns](#response-patterns)
4. [Search Handlers](#search-handlers)
5. [Pagination Handlers](#pagination-handlers)
6. [Form Handlers](#form-handlers)
7. [CRUD Operations](#crud-operations)
8. [Error Handling](#error-handling)
9. [Custom Headers](#custom-headers)
10. [Template Rendering](#template-rendering)

---

## Handler Basics

### Pattern 1: Basic HTMX Handler Structure
```go
package handlers

import (
    "net/http"
    "html/template"
)

type Handler struct {
    templates *template.Template
    // dependencies (db, cache, etc.)
}

func NewHandler(templates *template.Template) *Handler {
    return &Handler{
        templates: templates,
    }
}

func (h *Handler) ServeHTTP(w http.ResponseWriter, r *http.Request) {
    // Handler logic
    w.Header().Set("Content-Type", "text/html; charset=utf-8")

    data := map[string]interface{}{
        "Title": "Example",
    }

    h.templates.ExecuteTemplate(w, "component.html", data)
}
```

### Pattern 2: Handler with Dependency Injection
```go
type Dependencies struct {
    DB     *sql.DB
    Cache  *redis.Client
    Logger *slog.Logger
}

type Handler struct {
    deps      *Dependencies
    templates *template.Template
}

func NewHandler(deps *Dependencies, templates *template.Template) *Handler {
    return &Handler{
        deps:      deps,
        templates: templates,
    }
}
```

---

## HTMX Detection

### Pattern 3: Detect HTMX Request
```go
func (h *Handler) HandleRequest(w http.ResponseWriter, r *http.Request) {
    isHTMX := r.Header.Get("HX-Request") == "true"

    if isHTMX {
        // Return partial HTML for HTMX
        h.templates.ExecuteTemplate(w, "partial.html", data)
    } else {
        // Return full page for direct access
        h.templates.ExecuteTemplate(w, "full-page.html", data)
    }
}
```

### Pattern 4: HTMX Request Helper
```go
func IsHTMXRequest(r *http.Request) bool {
    return r.Header.Get("HX-Request") == "true"
}

func GetHTMXTrigger(r *http.Request) string {
    return r.Header.Get("HX-Trigger")
}

func GetHTMXTriggerName(r *http.Request) string {
    return r.Header.Get("HX-Trigger-Name")
}

func GetHTMXTarget(r *http.Request) string {
    return r.Header.Get("HX-Target")
}

func GetHTMXCurrentURL(r *http.Request) string {
    return r.Header.Get("HX-Current-URL")
}
```

---

## Response Patterns

### Pattern 5: HTML Fragment Response
```go
func (h *Handler) GetContent(w http.ResponseWriter, r *http.Request) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")

    content := struct {
        ID    int
        Title string
        Body  string
    }{
        ID:    123,
        Title: "Example Content",
        Body:  "This is the content body",
    }

    h.templates.ExecuteTemplate(w, "content-item.html", content)
}
```

### Pattern 6: JSON Response (for Client-Side Processing)
```go
func (h *Handler) GetData(w http.ResponseWriter, r *http.Request) {
    data := map[string]interface{}{
        "status": "success",
        "items":  []string{"item1", "item2"},
    }

    w.Header().Set("Content-Type", "application/json")
    json.NewEncoder(w).Encode(data)
}
```

### Pattern 7: Empty Response (204 No Content)
```go
func (h *Handler) DeleteItem(w http.ResponseWriter, r *http.Request) {
    id := chi.URLParam(r, "id")

    err := h.deps.DB.DeleteItem(id)
    if err != nil {
        http.Error(w, "Failed to delete", http.StatusInternalServerError)
        return
    }

    // Return 204 - HTMX will remove the element
    w.WriteHeader(http.StatusNoContent)
}
```

---

## Search Handlers

### Pattern 8: Live Search Handler
```go
func (h *Handler) LiveSearch(w http.ResponseWriter, r *http.Request) {
    query := r.URL.Query().Get("q")

    // Empty query returns empty results
    if query == "" {
        w.Header().Set("Content-Type", "text/html; charset=utf-8")
        w.Write([]byte(""))
        return
    }

    // Search database
    results, err := h.deps.DB.Search(query)
    if err != nil {
        h.renderError(w, "검색 중 오류가 발생했습니다")
        return
    }

    data := map[string]interface{}{
        "Query":   query,
        "Results": results,
        "Count":   len(results),
    }

    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    h.templates.ExecuteTemplate(w, "search-results.html", data)
}
```

### Pattern 9: Search with Debounce and Loading State
```go
func (h *Handler) SearchWithLoading(w http.ResponseWriter, r *http.Request) {
    query := strings.TrimSpace(r.URL.Query().Get("q"))

    if len(query) < 2 {
        // Minimum 2 characters
        w.Write([]byte(`<div class="hint">최소 2자 이상 입력하세요</div>`))
        return
    }

    // Simulate processing time for demonstration
    time.Sleep(100 * time.Millisecond)

    results, err := h.searchDatabase(query)
    if err != nil {
        h.renderError(w, "검색 실패")
        return
    }

    h.templates.ExecuteTemplate(w, "search-results.html", map[string]interface{}{
        "Query":   query,
        "Results": results,
    })
}
```

### Pattern 10: Search with Filters
```go
func (h *Handler) SearchWithFilters(w http.ResponseWriter, r *http.Request) {
    query := r.URL.Query().Get("q")
    category := r.URL.Query().Get("category")
    sortBy := r.URL.Query().Get("sort")

    // Validate sort parameter (prevent SQL injection)
    validSorts := map[string]bool{
        "created_at": true,
        "title":      true,
        "relevance":  true,
    }

    if !validSorts[sortBy] {
        sortBy = "relevance"
    }

    results, err := h.deps.DB.SearchWithFilters(query, category, sortBy)
    if err != nil {
        h.renderError(w, "검색 오류")
        return
    }

    h.templates.ExecuteTemplate(w, "search-results.html", map[string]interface{}{
        "Query":    query,
        "Category": category,
        "SortBy":   sortBy,
        "Results":  results,
    })
}
```

---

## Pagination Handlers

### Pattern 11: Basic Pagination
```go
func (h *Handler) GetPage(w http.ResponseWriter, r *http.Request) {
    pageStr := r.URL.Query().Get("page")
    page, err := strconv.Atoi(pageStr)
    if err != nil || page < 1 {
        page = 1
    }

    perPage := 20
    offset := (page - 1) * perPage

    items, total, err := h.deps.DB.GetItems(offset, perPage)
    if err != nil {
        h.renderError(w, "Failed to load items")
        return
    }

    data := map[string]interface{}{
        "Items":       items,
        "CurrentPage": page,
        "TotalPages":  (total + perPage - 1) / perPage,
        "HasNext":     page*perPage < total,
        "HasPrev":     page > 1,
    }

    h.templates.ExecuteTemplate(w, "items-page.html", data)
}
```

### Pattern 12: Infinite Scroll Handler
```go
func (h *Handler) LoadMore(w http.ResponseWriter, r *http.Request) {
    pageStr := r.URL.Query().Get("page")
    page, err := strconv.Atoi(pageStr)
    if err != nil || page < 1 {
        page = 1
    }

    perPage := 20
    offset := (page - 1) * perPage

    items, total, err := h.deps.DB.GetItems(offset, perPage)
    if err != nil {
        h.renderError(w, "Failed to load more")
        return
    }

    hasMore := offset+perPage < total
    nextPage := page + 1

    data := map[string]interface{}{
        "Items":    items,
        "HasMore":  hasMore,
        "NextPage": nextPage,
    }

    // Render items + optional load-more trigger
    h.templates.ExecuteTemplate(w, "items-infinite.html", data)
}
```

### Pattern 13: Cursor-Based Pagination
```go
func (h *Handler) GetItemsCursor(w http.ResponseWriter, r *http.Request) {
    cursor := r.URL.Query().Get("cursor")
    limit := 20

    items, nextCursor, err := h.deps.DB.GetItemsAfterCursor(cursor, limit)
    if err != nil {
        h.renderError(w, "Failed to load items")
        return
    }

    data := map[string]interface{}{
        "Items":      items,
        "NextCursor": nextCursor,
        "HasMore":    nextCursor != "",
    }

    h.templates.ExecuteTemplate(w, "items-cursor.html", data)
}
```

---

## Form Handlers

### Pattern 14: Form Submission with Validation
```go
type FormData struct {
    Email    string `validate:"required,email"`
    Username string `validate:"required,min=3,max=20"`
    Password string `validate:"required,min=8"`
}

func (h *Handler) SubmitForm(w http.ResponseWriter, r *http.Request) {
    if err := r.ParseForm(); err != nil {
        h.renderError(w, "잘못된 요청입니다")
        return
    }

    form := FormData{
        Email:    r.FormValue("email"),
        Username: r.FormValue("username"),
        Password: r.FormValue("password"),
    }

    // Validate
    if err := h.validator.Struct(form); err != nil {
        h.renderValidationErrors(w, err)
        return
    }

    // Process form
    err := h.deps.DB.CreateUser(form)
    if err != nil {
        h.renderError(w, "저장 실패")
        return
    }

    // Success response
    w.Header().Set("HX-Trigger", "userCreated")
    h.templates.ExecuteTemplate(w, "success-message.html", map[string]string{
        "Message": "성공적으로 저장되었습니다",
    })
}
```

### Pattern 15: Inline Validation
```go
func (h *Handler) ValidateField(w http.ResponseWriter, r *http.Request) {
    field := chi.URLParam(r, "field")
    value := r.FormValue(field)

    var errorMsg string

    switch field {
    case "email":
        if !isValidEmail(value) {
            errorMsg = "유효한 이메일 주소를 입력하세요"
        }
    case "username":
        if len(value) < 3 {
            errorMsg = "사용자명은 3자 이상이어야 합니다"
        }
        exists, _ := h.deps.DB.UsernameExists(value)
        if exists {
            errorMsg = "이미 사용 중인 사용자명입니다"
        }
    }

    w.Header().Set("Content-Type", "text/html; charset=utf-8")

    if errorMsg != "" {
        w.Write([]byte(fmt.Sprintf(`<span class="error">%s</span>`, errorMsg)))
    } else {
        w.Write([]byte(`<span class="success">✓</span>`))
    }
}
```

### Pattern 16: Multi-Step Form
```go
func (h *Handler) FormStep(w http.ResponseWriter, r *http.Request) {
    stepStr := r.URL.Query().Get("step")
    step, _ := strconv.Atoi(stepStr)
    if step < 1 {
        step = 1
    }

    // Get form data from session or hidden fields
    sessionData := h.getSessionData(r)

    // Validate previous step if moving forward
    if r.Method == "POST" && step > 1 {
        if err := h.validateStep(step-1, r); err != nil {
            h.renderValidationErrors(w, err)
            return
        }

        // Save step data to session
        h.saveStepData(w, r, step-1)
        step++ // Move to next step
    }

    data := map[string]interface{}{
        "Step":        step,
        "TotalSteps":  3,
        "SessionData": sessionData,
    }

    h.templates.ExecuteTemplate(w, fmt.Sprintf("form-step-%d.html", step), data)
}
```

---

## CRUD Operations

### Pattern 17: Create Handler
```go
func (h *Handler) CreateItem(w http.ResponseWriter, r *http.Request) {
    if err := r.ParseForm(); err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }

    item := &Item{
        Title:   r.FormValue("title"),
        Content: r.FormValue("content"),
    }

    // Validate
    if item.Title == "" {
        h.renderError(w, "제목은 필수입니다")
        return
    }

    // Create in database
    id, err := h.deps.DB.CreateItem(item)
    if err != nil {
        h.renderError(w, "저장 실패")
        return
    }

    item.ID = id

    // Return new item HTML
    w.Header().Set("HX-Trigger", "itemCreated")
    h.templates.ExecuteTemplate(w, "item.html", item)
}
```

### Pattern 18: Update Handler
```go
func (h *Handler) UpdateItem(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.Atoi(idStr)
    if err != nil {
        http.Error(w, "Invalid ID", http.StatusBadRequest)
        return
    }

    if err := r.ParseForm(); err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }

    updates := map[string]interface{}{
        "title":   r.FormValue("title"),
        "content": r.FormValue("content"),
    }

    err = h.deps.DB.UpdateItem(id, updates)
    if err != nil {
        h.renderError(w, "수정 실패")
        return
    }

    // Fetch updated item
    item, err := h.deps.DB.GetItem(id)
    if err != nil {
        h.renderError(w, "조회 실패")
        return
    }

    w.Header().Set("HX-Trigger", "itemUpdated")
    h.templates.ExecuteTemplate(w, "item.html", item)
}
```

### Pattern 19: Delete Handler
```go
func (h *Handler) DeleteItem(w http.ResponseWriter, r *http.Request) {
    idStr := chi.URLParam(r, "id")
    id, err := strconv.Atoi(idStr)
    if err != nil {
        http.Error(w, "Invalid ID", http.StatusBadRequest)
        return
    }

    err = h.deps.DB.DeleteItem(id)
    if err != nil {
        h.renderError(w, "삭제 실패")
        return
    }

    // Return 200 with empty body or success message
    w.Header().Set("HX-Trigger", `{"itemDeleted": {"id": `+idStr+`}}`)
    w.WriteHeader(http.StatusOK)

    // HTMX will swap with empty content (removes element)
}
```

### Pattern 20: Bulk Operations
```go
func (h *Handler) BulkDelete(w http.ResponseWriter, r *http.Request) {
    if err := r.ParseForm(); err != nil {
        http.Error(w, "Bad request", http.StatusBadRequest)
        return
    }

    ids := r.Form["ids[]"]
    if len(ids) == 0 {
        h.renderError(w, "선택된 항목이 없습니다")
        return
    }

    // Convert to integers
    intIDs := make([]int, 0, len(ids))
    for _, idStr := range ids {
        id, err := strconv.Atoi(idStr)
        if err == nil {
            intIDs = append(intIDs, id)
        }
    }

    count, err := h.deps.DB.BulkDelete(intIDs)
    if err != nil {
        h.renderError(w, "삭제 실패")
        return
    }

    w.Header().Set("HX-Trigger", `{"bulkDeleted": {"count": `+strconv.Itoa(count)+`}}`)
    w.Write([]byte(fmt.Sprintf(`<div class="success">%d개 항목이 삭제되었습니다</div>`, count)))
}
```

---

## Error Handling

### Pattern 21: Error Response Helper
```go
func (h *Handler) renderError(w http.ResponseWriter, message string) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.WriteHeader(http.StatusBadRequest)

    data := map[string]string{
        "Message": message,
    }

    h.templates.ExecuteTemplate(w, "error.html", data)
}

func (h *Handler) renderValidationErrors(w http.ResponseWriter, err error) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.WriteHeader(http.StatusUnprocessableEntity)

    // Parse validation errors
    errors := parseValidationErrors(err)

    data := map[string]interface{}{
        "Errors": errors,
    }

    h.templates.ExecuteTemplate(w, "validation-errors.html", data)
}
```

### Pattern 22: Structured Error Response
```go
type ErrorResponse struct {
    Message string            `json:"message"`
    Fields  map[string]string `json:"fields,omitempty"`
}

func (h *Handler) HandleError(w http.ResponseWriter, err error, status int) {
    w.Header().Set("Content-Type", "text/html; charset=utf-8")
    w.WriteHeader(status)

    errResp := ErrorResponse{
        Message: err.Error(),
    }

    // Check if it's a validation error
    if validationErr, ok := err.(validator.ValidationErrors); ok {
        errResp.Fields = make(map[string]string)
        for _, fieldErr := range validationErr {
            errResp.Fields[fieldErr.Field()] = fieldErr.Tag()
        }
    }

    h.templates.ExecuteTemplate(w, "error-detail.html", errResp)
}
```

---

## Custom Headers

### Pattern 23: Trigger Client-Side Events
```go
func (h *Handler) SaveItem(w http.ResponseWriter, r *http.Request) {
    // ... save logic ...

    // Trigger custom event on client
    w.Header().Set("HX-Trigger", `{"itemSaved": {"id": 123, "message": "저장됨"}}`)

    h.templates.ExecuteTemplate(w, "item.html", item)
}
```

### Pattern 24: Redirect After Action
```go
func (h *Handler) CompleteAction(w http.ResponseWriter, r *http.Request) {
    // ... complete action ...

    // Redirect to another page
    w.Header().Set("HX-Redirect", "/success-page")
    w.WriteHeader(http.StatusOK)
}
```

### Pattern 25: Refresh Page
```go
func (h *Handler) SystemUpdate(w http.ResponseWriter, r *http.Request) {
    // ... update system ...

    // Tell HTMX to refresh the entire page
    w.Header().Set("HX-Refresh", "true")
    w.WriteHeader(http.StatusOK)
}
```

### Pattern 26: Multiple Triggers
```go
func (h *Handler) ComplexAction(w http.ResponseWriter, r *http.Request) {
    // ... perform action ...

    // Trigger multiple events
    triggers := map[string]interface{}{
        "itemSaved": map[string]interface{}{
            "id": 123,
        },
        "showNotification": map[string]interface{}{
            "message": "저장 완료",
            "level":   "success",
        },
        "updateSidebar": true,
    }

    triggersJSON, _ := json.Marshal(triggers)
    w.Header().Set("HX-Trigger", string(triggersJSON))

    h.templates.ExecuteTemplate(w, "result.html", data)
}
```

---

## Template Rendering

### Pattern 27: Render with Layout
```go
func (h *Handler) RenderPage(w http.ResponseWriter, r *http.Request) {
    isHTMX := IsHTMXRequest(r)

    data := map[string]interface{}{
        "Title":   "Page Title",
        "Content": "Page content",
    }

    if isHTMX {
        // Render just the content partial
        h.templates.ExecuteTemplate(w, "content.html", data)
    } else {
        // Render full page with layout
        h.templates.ExecuteTemplate(w, "layout.html", data)
    }
}
```

### Pattern 28: Out-of-Band Swap Response
```go
func (h *Handler) UpdateMultiple(w http.ResponseWriter, r *http.Request) {
    // Main content
    mainContent := map[string]interface{}{
        "Items": []string{"item1", "item2"},
    }

    // Sidebar content (out-of-band)
    sidebarContent := map[string]interface{}{
        "Count": 42,
    }

    w.Header().Set("Content-Type", "text/html; charset=utf-8")

    // Render main content
    h.templates.ExecuteTemplate(w, "main-content.html", mainContent)

    // Render sidebar with hx-swap-oob
    w.Write([]byte(`<div id="sidebar" hx-swap-oob="true">`))
    h.templates.ExecuteTemplate(w, "sidebar.html", sidebarContent)
    w.Write([]byte(`</div>`))
}
```

---

## Router Setup (chi example)

### Pattern 29: HTMX Route Group
```go
func SetupRoutes(r chi.Router, h *Handler) {
    // API routes for HTMX
    r.Route("/api", func(r chi.Router) {
        // Search
        r.Get("/search", h.LiveSearch)

        // CRUD
        r.Get("/items", h.GetItems)
        r.Post("/items", h.CreateItem)
        r.Get("/items/{id}", h.GetItem)
        r.Put("/items/{id}", h.UpdateItem)
        r.Delete("/items/{id}", h.DeleteItem)

        // Pagination
        r.Get("/items/page/{page}", h.GetPage)
        r.Get("/items/more", h.LoadMore)

        // Forms
        r.Post("/forms/submit", h.SubmitForm)
        r.Post("/forms/validate/{field}", h.ValidateField)
    })

    // Regular pages
    r.Get("/", h.HomePage)
    r.Get("/items/{id}", h.ItemPage)
}
```

### Pattern 30: Middleware for HTMX
```go
func HTMXMiddleware(next http.Handler) http.Handler {
    return http.HandlerFunc(func(w http.ResponseWriter, r *http.Request) {
        // Add HTMX detection to context
        ctx := context.WithValue(r.Context(), "isHTMX", IsHTMXRequest(r))

        // Add common HTMX headers
        if IsHTMXRequest(r) {
            w.Header().Set("Vary", "HX-Request")
        }

        next.ServeHTTP(w, r.WithContext(ctx))
    })
}
```

---

## Best Practices

1. **Always set Content-Type**: `text/html; charset=utf-8` for HTML responses
2. **Detect HTMX requests**: Use `HX-Request` header to return partial vs full pages
3. **Use appropriate status codes**: 200 (success), 204 (no content), 422 (validation error)
4. **Implement proper error handling**: Return user-friendly error messages
5. **Validate input**: Always validate and sanitize user input
6. **Use templates efficiently**: Cache parsed templates, reuse partials
7. **Return Korean messages**: Use proper UTF-8 encoding for Korean text
8. **Set custom headers**: Use HX-Trigger, HX-Redirect for client-side actions
9. **Handle edge cases**: Empty queries, invalid IDs, missing data
10. **Test without HTMX**: Ensure endpoints work as standalone APIs

---

## Common Response Headers

| Header | Purpose | Example |
|--------|---------|---------|
| Content-Type | Response content type | `text/html; charset=utf-8` |
| HX-Trigger | Trigger client events | `{"eventName": {"data": "value"}}` |
| HX-Redirect | Client-side redirect | `/new-page` |
| HX-Refresh | Refresh entire page | `true` |
| HX-Push-Url | Update browser URL | `/new-url` |
| HX-Retarget | Change target element | `#new-target` |
| HX-Reswap | Change swap strategy | `outerHTML` |
| Vary | Cache control | `HX-Request` |

---

**Version:** 1.0.0
**Last Updated:** 2025-10-25
**Pattern Count:** 30+
