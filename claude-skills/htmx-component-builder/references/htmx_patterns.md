# HTMX Patterns Reference Library

Comprehensive collection of 50+ HTMX patterns for building interactive web components.

## Table of Contents

1. [Basic Patterns](#basic-patterns)
2. [HTTP Methods](#http-methods)
3. [Triggers](#triggers)
4. [Targets & Swaps](#targets--swaps)
5. [Loading States](#loading-states)
6. [Form Patterns](#form-patterns)
7. [Search Patterns](#search-patterns)
8. [Infinite Scroll](#infinite-scroll)
9. [Modal Patterns](#modal-patterns)
10. [Tab Navigation](#tab-navigation)
11. [Delete Confirmation](#delete-confirmation)
12. [Inline Editing](#inline-editing)
13. [Advanced Patterns](#advanced-patterns)
14. [Korean IME Handling](#korean-ime-handling)
15. [Error Handling](#error-handling)

---

## Basic Patterns

### Pattern 1: Basic GET Request
```html
<button hx-get="/api/data" hx-target="#result">
    Load Data
</button>
<div id="result"></div>
```

### Pattern 2: Basic POST Request
```html
<button hx-post="/api/save" hx-target="#status">
    Save
</button>
<div id="status"></div>
```

### Pattern 3: Click to Load Content
```html
<div hx-get="/content/123" hx-trigger="click" hx-target="#content-area">
    Click to load content
</div>
```

### Pattern 4: Auto-load on Page Load
```html
<div hx-get="/api/initial-data" hx-trigger="load" hx-target="this">
    Loading...
</div>
```

### Pattern 5: Replace Element Content
```html
<div hx-get="/api/update" hx-swap="innerHTML">
    Current content
</div>
```

---

## HTTP Methods

### Pattern 6: GET Request
```html
<a hx-get="/users/123" hx-target="#user-detail">View User</a>
```

### Pattern 7: POST Request
```html
<button hx-post="/api/create" hx-vals='{"name": "John"}'>
    Create User
</button>
```

### Pattern 8: PUT Request
```html
<button hx-put="/api/users/123" hx-vals='{"status": "active"}'>
    Activate User
</button>
```

### Pattern 9: PATCH Request
```html
<button hx-patch="/api/users/123" hx-vals='{"email": "new@example.com"}'>
    Update Email
</button>
```

### Pattern 10: DELETE Request
```html
<button hx-delete="/api/users/123"
        hx-confirm="Are you sure?"
        hx-target="#user-list">
    Delete User
</button>
```

---

## Triggers

### Pattern 11: Click Trigger (Default)
```html
<button hx-get="/api/data" hx-trigger="click">Click Me</button>
```

### Pattern 12: Change Trigger (Forms)
```html
<select hx-get="/api/filter" hx-trigger="change">
    <option>Option 1</option>
    <option>Option 2</option>
</select>
```

### Pattern 13: Input with Debounce
```html
<input type="text"
       hx-get="/api/search"
       hx-trigger="keyup changed delay:500ms"
       placeholder="Search...">
```

### Pattern 14: Load Trigger (Page Load)
```html
<div hx-get="/api/initial" hx-trigger="load"></div>
```

### Pattern 15: Custom Event Trigger
```html
<div hx-get="/api/refresh" hx-trigger="customEvent from:body"></div>
```

### Pattern 16: Multiple Triggers
```html
<div hx-get="/api/data"
     hx-trigger="click, customRefresh from:body"></div>
```

### Pattern 17: Revealed Trigger (Infinite Scroll)
```html
<div hx-get="/api/next-page" hx-trigger="revealed"></div>
```

### Pattern 18: Intersect Trigger (Lazy Load)
```html
<img hx-get="/api/image/123"
     hx-trigger="intersect once"
     hx-target="this"
     hx-swap="outerHTML">
```

---

## Targets & Swaps

### Pattern 19: Target by ID
```html
<button hx-get="/api/data" hx-target="#result-area">Load</button>
<div id="result-area"></div>
```

### Pattern 20: Target Closest Parent
```html
<div class="card">
    <button hx-get="/api/update" hx-target="closest .card">Update</button>
</div>
```

### Pattern 21: Target Next Sibling
```html
<button hx-get="/api/data" hx-target="next .result">Load</button>
<div class="result"></div>
```

### Pattern 22: Target Previous Sibling
```html
<div class="result"></div>
<button hx-get="/api/data" hx-target="previous .result">Load</button>
```

### Pattern 23: Swap innerHTML (Default)
```html
<div hx-get="/api/content" hx-swap="innerHTML">Content here</div>
```

### Pattern 24: Swap outerHTML (Replace Element)
```html
<div hx-get="/api/content" hx-swap="outerHTML">Replace me</div>
```

### Pattern 25: Swap beforebegin (Prepend Before)
```html
<div hx-get="/api/new-item" hx-swap="beforebegin">Existing content</div>
```

### Pattern 26: Swap afterbegin (Prepend Inside)
```html
<div hx-get="/api/new-item" hx-swap="afterbegin">Existing content</div>
```

### Pattern 27: Swap beforeend (Append Inside)
```html
<div hx-get="/api/new-item" hx-swap="beforeend">Existing content</div>
```

### Pattern 28: Swap afterend (Append After)
```html
<div hx-get="/api/new-item" hx-swap="afterend">Existing content</div>
```

### Pattern 29: Swap with Transition Timing
```html
<div hx-get="/api/content"
     hx-swap="innerHTML swap:1s settle:1s">
    Content
</div>
```

---

## Loading States

### Pattern 30: Basic Loading Indicator
```html
<button hx-get="/api/data" hx-indicator="#spinner">
    Load Data
</button>
<div id="spinner" class="htmx-indicator">Loading...</div>

<style>
.htmx-indicator { display: none; }
.htmx-request .htmx-indicator { display: inline; }
</style>
```

### Pattern 31: Loading on Element Itself
```html
<button hx-get="/api/data">
    <span class="htmx-indicator">Loading...</span>
    <span>Load Data</span>
</button>
```

### Pattern 32: Disable Button During Request
```html
<button hx-get="/api/save"
        hx-disabled-elt="this"
        hx-indicator="#saving">
    Save
</button>
<span id="saving" class="htmx-indicator">Saving...</span>
```

### Pattern 33: Multiple Loading Indicators
```html
<button hx-get="/api/data"
        hx-indicator="#spinner1, #spinner2">
    Load
</button>
<div id="spinner1" class="htmx-indicator">Loading...</div>
<div id="spinner2" class="htmx-indicator">Processing...</div>
```

### Pattern 34: Loading with CSS Classes
```html
<div hx-get="/api/data" hx-target="this">
    <div class="htmx-swapping">Transitioning out...</div>
    <div class="htmx-settling">Transitioning in...</div>
</div>

<style>
.htmx-swapping { opacity: 0; transition: opacity 200ms; }
.htmx-settling { opacity: 1; transition: opacity 200ms; }
</style>
```

---

## Form Patterns

### Pattern 35: Basic Form Submission
```html
<form hx-post="/api/submit" hx-target="#result">
    <input type="text" name="username">
    <input type="email" name="email">
    <button type="submit">Submit</button>
</form>
<div id="result"></div>
```

### Pattern 36: Form with File Upload
```html
<form hx-post="/api/upload"
      hx-encoding="multipart/form-data"
      hx-target="#upload-result">
    <input type="file" name="file">
    <button type="submit">Upload</button>
</form>
```

### Pattern 37: Form Validation
```html
<form hx-post="/api/validate" hx-target="#errors">
    <input type="text" name="email" required>
    <button type="submit">Validate</button>
</form>
<div id="errors"></div>
```

### Pattern 38: Progressive Form Enhancement
```html
<form action="/submit" method="post"
      hx-post="/api/submit"
      hx-target="#result">
    <!-- Works with and without JavaScript -->
    <input type="text" name="name">
    <button type="submit">Submit</button>
</form>
```

### Pattern 39: Dependent Form Fields
```html
<select name="country"
        hx-get="/api/states"
        hx-target="#state-select"
        hx-trigger="change">
    <option value="us">United States</option>
    <option value="ca">Canada</option>
</select>
<select id="state-select" name="state"></select>
```

---

## Search Patterns

### Pattern 40: Live Search (Basic)
```html
<input type="text"
       name="search"
       hx-get="/api/search"
       hx-trigger="keyup changed delay:500ms"
       hx-target="#search-results"
       placeholder="Search...">
<div id="search-results"></div>
```

### Pattern 41: Live Search with Loading
```html
<form>
    <input type="text"
           name="q"
           hx-get="/api/search"
           hx-trigger="keyup changed delay:500ms"
           hx-target="#results"
           hx-indicator="#search-loading">
    <span id="search-loading" class="htmx-indicator">🔍 Searching...</span>
</form>
<div id="results"></div>
```

### Pattern 42: Search with Enter Key
```html
<input type="text"
       name="search"
       hx-get="/api/search"
       hx-trigger="keyup[key=='Enter']"
       hx-target="#search-results">
```

### Pattern 43: Search with Clear Button
```html
<div class="search-container">
    <input type="text"
           name="q"
           hx-get="/api/search"
           hx-trigger="keyup changed delay:500ms"
           hx-target="#results">
    <button hx-get="/api/search?q="
            hx-target="#results">
        Clear
    </button>
</div>
<div id="results"></div>
```

---

## Infinite Scroll

### Pattern 44: Basic Infinite Scroll
```html
<div id="content-list">
    <!-- Initial content -->
    <div class="content-item">Item 1</div>
    <div class="content-item">Item 2</div>

    <!-- Load more trigger -->
    <div hx-get="/api/content?page=2"
         hx-trigger="revealed"
         hx-swap="afterend">
        Loading more...
    </div>
</div>
```

### Pattern 45: Infinite Scroll with Pagination
```html
<div id="items">
    <!-- Current items -->
</div>
<div hx-get="/api/items?page=2"
     hx-trigger="revealed"
     hx-swap="outerHTML"
     hx-target="this">
    <div class="loading">Loading more...</div>
</div>
```

### Pattern 46: Infinite Scroll with Threshold
```html
<div hx-get="/api/next"
     hx-trigger="revealed threshold:0.5"
     hx-swap="afterend">
    <!-- Triggers when 50% visible -->
</div>
```

---

## Modal Patterns

### Pattern 47: Open Modal with Content
```html
<!-- Trigger -->
<button hx-get="/api/user/123/details"
        hx-target="#modal-container"
        hx-swap="innerHTML">
    View Details
</button>

<!-- Modal container -->
<div id="modal-container"></div>

<!-- Server returns -->
<div class="modal">
    <div class="modal-content">
        <button onclick="closeModal()">Close</button>
        <h2>User Details</h2>
        <!-- content -->
    </div>
</div>
```

### Pattern 48: Modal with Form
```html
<button hx-get="/api/forms/edit/123"
        hx-target="#modal-body">
    Edit
</button>

<div id="modal-body"></div>

<!-- Server returns form that posts back -->
<form hx-post="/api/update/123"
      hx-target="#main-content"
      hx-swap="outerHTML">
    <!-- form fields -->
    <button type="submit">Save</button>
</form>
```

---

## Tab Navigation

### Pattern 49: Dynamic Tab Loading
```html
<div class="tabs">
    <button hx-get="/api/tabs/profile"
            hx-target="#tab-content"
            class="active">Profile</button>
    <button hx-get="/api/tabs/settings"
            hx-target="#tab-content">Settings</button>
    <button hx-get="/api/tabs/activity"
            hx-target="#tab-content">Activity</button>
</div>
<div id="tab-content">
    <!-- Tab content loads here -->
</div>
```

### Pattern 50: Tab with History
```html
<button hx-get="/api/tabs/profile"
        hx-target="#tab-content"
        hx-push-url="true">Profile</button>
```

---

## Delete Confirmation

### Pattern 51: Simple Delete Confirmation
```html
<button hx-delete="/api/items/123"
        hx-confirm="Are you sure you want to delete this item?"
        hx-target="closest .item"
        hx-swap="outerHTML">
    Delete
</button>
```

### Pattern 52: Delete with Success Message
```html
<button hx-delete="/api/items/123"
        hx-confirm="Delete this item?"
        hx-target="closest .item"
        hx-swap="outerHTML swap:1s">
    Delete
</button>

<!-- Server returns empty or success message -->
```

---

## Inline Editing

### Pattern 53: Click to Edit
```html
<div hx-get="/api/edit/field/123"
     hx-target="this"
     hx-swap="outerHTML">
    Current Value (click to edit)
</div>

<!-- Server returns input field -->
<input type="text"
       name="value"
       value="Current Value"
       hx-post="/api/save/field/123"
       hx-target="this"
       hx-swap="outerHTML"
       hx-trigger="blur">
```

### Pattern 54: Inline Edit with Cancel
```html
<!-- Display mode -->
<div class="editable" hx-get="/api/edit/123" hx-target="this">
    <span>Current text</span>
    <button>Edit</button>
</div>

<!-- Edit mode (returned by server) -->
<div class="editing">
    <input type="text" value="Current text"
           hx-post="/api/save/123"
           hx-target="closest .editing"
           hx-swap="outerHTML">
    <button hx-get="/api/cancel/123"
            hx-target="closest .editing">Cancel</button>
</div>
```

---

## Advanced Patterns

### Pattern 55: Out-of-Band Swap (Update Multiple Elements)
```html
<!-- Trigger -->
<button hx-post="/api/action" hx-target="#main">Execute</button>

<!-- Server returns multiple elements -->
<div id="main">Updated main content</div>
<div id="sidebar" hx-swap-oob="true">Updated sidebar</div>
<div id="notifications" hx-swap-oob="true">New notification</div>
```

### Pattern 56: Custom Response Headers
```html
<!-- Client side -->
<button hx-get="/api/data" hx-target="#result">Load</button>

<!-- Server responds with custom headers -->
HX-Trigger: {"showMessage": {"level": "info", "message": "Success"}}
HX-Redirect: /new-page
HX-Refresh: true
```

### Pattern 57: Request Headers
```html
<button hx-get="/api/data"
        hx-headers='{"X-Custom-Header": "value"}'>
    Load
</button>
```

### Pattern 58: Polling (Auto-refresh)
```html
<div hx-get="/api/status"
     hx-trigger="every 2s"
     hx-target="this">
    Current status...
</div>
```

### Pattern 59: Load Polling (Start on Load)
```html
<div hx-get="/api/updates"
     hx-trigger="load, every 5s"
     hx-target="this">
    Checking for updates...
</div>
```

### Pattern 60: History Push (Update URL)
```html
<a hx-get="/page/about"
   hx-target="#content"
   hx-push-url="true">About</a>
```

### Pattern 61: Boosted Links (Progressive Enhancement)
```html
<div hx-boost="true">
    <!-- All links in this container become AJAX -->
    <a href="/page1">Page 1</a>
    <a href="/page2">Page 2</a>
</div>
```

### Pattern 62: Request with Include
```html
<button hx-post="/api/submit"
        hx-include="[name='email'], [name='password']">
    Submit
</button>
```

### Pattern 63: Preserve Element During Swap
```html
<div hx-get="/api/update" hx-target="this">
    <div hx-preserve="true">This won't be replaced</div>
    <div>This will be replaced</div>
</div>
```

### Pattern 64: Synchronize Requests (Wait for Previous)
```html
<button hx-post="/api/action" hx-sync="this:replace">
    Click me (replaces pending request)
</button>
```

---

## Korean IME Handling

### Pattern 65: Search with Korean IME Support
```html
<input type="text"
       name="search"
       id="korean-search"
       hx-get="/api/search"
       hx-trigger="keyup changed delay:500ms"
       hx-target="#results"
       placeholder="검색어를 입력하세요">

<script>
let isComposing = false;
const input = document.getElementById('korean-search');

input.addEventListener('compositionstart', () => {
    isComposing = true;
});

input.addEventListener('compositionend', () => {
    isComposing = false;
    // Manually trigger HTMX after composition
    htmx.trigger(input, 'keyup');
});

input.addEventListener('keyup', (e) => {
    if (isComposing) {
        e.stopPropagation();
        return false;
    }
});
</script>
```

### Pattern 66: Form with Korean Input
```html
<form hx-post="/api/submit" id="korean-form">
    <input type="text" name="title" class="korean-input">
    <textarea name="content" class="korean-input"></textarea>
    <button type="submit">제출</button>
</form>

<script>
document.querySelectorAll('.korean-input').forEach(input => {
    let isComposing = false;

    input.addEventListener('compositionstart', () => {
        isComposing = true;
    });

    input.addEventListener('compositionend', () => {
        isComposing = false;
    });
});
</script>

<style>
.korean-input {
    word-break: keep-all;
    letter-spacing: -0.3px;
    line-height: 1.6;
}
</style>
```

---

## Error Handling

### Pattern 67: Display Error Messages
```html
<button hx-post="/api/save"
        hx-target="#result"
        hx-swap="innerHTML"
        hx-on="htmx:responseError: alert('Request failed')">
    Save
</button>
```

### Pattern 68: Retry on Error
```html
<div hx-get="/api/data"
     hx-trigger="load"
     hx-on="htmx:responseError: this.dispatchEvent(new Event('load'))">
    Loading...
</div>
```

### Pattern 69: Error Target
```html
<form hx-post="/api/submit">
    <input type="text" name="email">
    <button type="submit">Submit</button>
</form>
<div id="errors"></div>

<!-- Server returns 4xx/5xx with error HTML targeting #errors -->
```

### Pattern 70: Validation Error Display
```html
<form hx-post="/api/validate" hx-target="#form-container">
    <input type="email" name="email">
    <span class="error" style="display: none;"></span>
    <button type="submit">Validate</button>
</form>

<!-- Server returns form with errors -->
<form hx-post="/api/validate" hx-target="#form-container">
    <input type="email" name="email" class="invalid">
    <span class="error" style="display: block;">Invalid email</span>
    <button type="submit">Validate</button>
</form>
```

---

## Best Practices

1. **Always provide loading indicators** for better UX
2. **Use debouncing** for search inputs (500ms recommended)
3. **Handle Korean IME** for Korean text inputs
4. **Implement error handling** with user-friendly messages
5. **Use progressive enhancement** (hx-boost) when possible
6. **Include confirmation** for destructive actions
7. **Optimize swap strategies** for smooth transitions
8. **Consider accessibility** in all patterns
9. **Test without JavaScript** for degradation
10. **Use appropriate HTTP methods** (GET for reads, POST for creates, etc.)

---

## HTMX Attributes Quick Reference

| Attribute | Purpose | Example |
|-----------|---------|---------|
| hx-get | GET request | `hx-get="/api/data"` |
| hx-post | POST request | `hx-post="/api/save"` |
| hx-put | PUT request | `hx-put="/api/update"` |
| hx-patch | PATCH request | `hx-patch="/api/modify"` |
| hx-delete | DELETE request | `hx-delete="/api/remove"` |
| hx-trigger | Event trigger | `hx-trigger="click, keyup"` |
| hx-target | Target element | `hx-target="#result"` |
| hx-swap | Swap strategy | `hx-swap="innerHTML"` |
| hx-indicator | Loading indicator | `hx-indicator="#spinner"` |
| hx-confirm | Confirmation dialog | `hx-confirm="Are you sure?"` |
| hx-vals | Additional values | `hx-vals='{"key": "value"}'` |
| hx-headers | Request headers | `hx-headers='{"X-Custom": "val"}'` |
| hx-boost | Progressive enhancement | `hx-boost="true"` |
| hx-push-url | Update browser URL | `hx-push-url="true"` |
| hx-select | Select response subset | `hx-select="#content"` |
| hx-swap-oob | Out-of-band swap | `hx-swap-oob="true"` |
| hx-preserve | Preserve during swap | `hx-preserve="true"` |
| hx-sync | Synchronize requests | `hx-sync="this:replace"` |

---

**Version:** 1.0.0
**Last Updated:** 2025-10-25
**Pattern Count:** 70+
