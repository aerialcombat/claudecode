# Korean Optimization Guide for HTMX Components

Comprehensive guide to building Korean-optimized HTMX components with proper IME handling, typography, and localization.

## Table of Contents

1. [Korean IME Fundamentals](#korean-ime-fundamentals)
2. [IME Event Handling](#ime-event-handling)
3. [Search Component Optimization](#search-component-optimization)
4. [Form Input Optimization](#form-input-optimization)
5. [Typography & CSS](#typography--css)
6. [Localized Messages](#localized-messages)
7. [Date & Number Formatting](#date--number-formatting)
8. [Validation Messages](#validation-messages)
9. [Loading States](#loading-states)
10. [Best Practices](#best-practices)

---

## Korean IME Fundamentals

### Understanding Hangul Composition

Korean text input uses an Input Method Editor (IME) that composes characters:

**Composition Process:**
```
User types: ㄱ → 가 → 간 → 강 (single character being composed)
```

**Problem with HTMX:**
- HTMX triggers on `keyup` events
- IME fires `keyup` during composition
- Triggers premature AJAX requests before user finishes typing character

**Solution:**
- Use `compositionstart` and `compositionend` events
- Block HTMX triggers during composition
- Only send requests after character is complete

---

## IME Event Handling

### Pattern 1: Basic IME-Aware Input
```html
<input type="text"
       id="korean-input"
       name="search"
       placeholder="검색어를 입력하세요">

<script>
let isComposing = false;
const input = document.getElementById('korean-input');

input.addEventListener('compositionstart', () => {
    isComposing = true;
});

input.addEventListener('compositionend', () => {
    isComposing = false;
});

input.addEventListener('keyup', (e) => {
    if (isComposing) {
        e.stopPropagation();
        return false;
    }
    // Normal HTMX processing continues
});
</script>
```

### Pattern 2: IME-Aware HTMX Search
```html
<input type="text"
       id="korean-search"
       name="q"
       hx-get="/api/search"
       hx-trigger="keyup changed delay:500ms"
       hx-target="#results"
       placeholder="검색어 입력">

<script>
(function() {
    let isComposing = false;
    const input = document.getElementById('korean-search');

    input.addEventListener('compositionstart', () => {
        isComposing = true;
        console.log('Composition started');
    });

    input.addEventListener('compositionend', () => {
        isComposing = false;
        console.log('Composition ended');
        // Manually trigger HTMX after composition
        htmx.trigger(input, 'keyup');
    });

    input.addEventListener('keyup', (e) => {
        if (isComposing) {
            console.log('Blocking during composition');
            e.stopPropagation();
            return false;
        }
    });
})();
</script>
```

### Pattern 3: Reusable IME Handler
```javascript
// ime-handler.js
function initIMEHandler(elementId) {
    let isComposing = false;
    const element = document.getElementById(elementId);

    if (!element) return;

    element.addEventListener('compositionstart', () => {
        isComposing = true;
        element.setAttribute('data-composing', 'true');
    });

    element.addEventListener('compositionend', () => {
        isComposing = false;
        element.removeAttribute('data-composing');
        // Trigger HTMX after composition completes
        htmx.trigger(element, 'keyup');
    });

    element.addEventListener('keyup', (e) => {
        if (isComposing) {
            e.stopPropagation();
            return false;
        }
    });

    return {
        isComposing: () => isComposing
    };
}

// Usage
document.addEventListener('DOMContentLoaded', () => {
    initIMEHandler('search-input');
    initIMEHandler('comment-input');
});
```

### Pattern 4: Multiple IME-Aware Inputs
```javascript
// Multi-input IME handler
function initAllKoreanInputs() {
    document.querySelectorAll('.korean-input').forEach(input => {
        let isComposing = false;

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
    });
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', initAllKoreanInputs);

// Re-initialize after HTMX content swap
document.body.addEventListener('htmx:afterSwap', initAllKoreanInputs);
```

---

## Search Component Optimization

### Pattern 5: Complete Korean Search Component
```html
<div class="search-container">
    <form class="search-form">
        <input type="text"
               id="korean-search"
               name="q"
               class="korean-input search-input"
               hx-get="/api/search"
               hx-trigger="keyup changed delay:500ms"
               hx-target="#search-results"
               hx-indicator="#search-loading"
               placeholder="검색어를 입력하세요"
               autocomplete="off">

        <span id="search-loading" class="htmx-indicator">
            🔍 검색 중...
        </span>
    </form>

    <div id="search-results" class="search-results"></div>
</div>

<style>
.korean-input {
    font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", sans-serif;
    word-break: keep-all;
    letter-spacing: -0.3px;
    line-height: 1.6;
}

.search-input {
    padding: 12px 16px;
    font-size: 16px;
    border: 2px solid #e0e0e0;
    border-radius: 8px;
    width: 100%;
}

.search-input:focus {
    outline: none;
    border-color: #0066cc;
}

.search-input[data-composing="true"] {
    border-color: #ff9900; /* Visual indicator during composition */
}

.htmx-indicator {
    display: none;
    color: #666;
    font-size: 14px;
    margin-left: 8px;
}

.htmx-request .htmx-indicator {
    display: inline;
}
</style>

<script>
(function() {
    let isComposing = false;
    const input = document.getElementById('korean-search');

    input.addEventListener('compositionstart', () => {
        isComposing = true;
        input.setAttribute('data-composing', 'true');
    });

    input.addEventListener('compositionend', () => {
        isComposing = false;
        input.removeAttribute('data-composing');
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
```

### Pattern 6: Search with Minimum Length (Korean-aware)
```javascript
function initKoreanSearch() {
    const input = document.getElementById('korean-search');
    let isComposing = false;

    input.addEventListener('compositionstart', () => {
        isComposing = true;
    });

    input.addEventListener('compositionend', () => {
        isComposing = false;
        checkAndSearch();
    });

    input.addEventListener('keyup', (e) => {
        if (isComposing) {
            e.stopPropagation();
            return false;
        }
        checkAndSearch();
    });

    function checkAndSearch() {
        const value = input.value.trim();

        // Korean characters count differently
        // 1 Korean character = valuable, unlike English
        if (value.length < 1) {
            document.getElementById('search-results').innerHTML =
                '<div class="hint">검색어를 입력하세요</div>';
            return;
        }

        // Trigger HTMX search
        htmx.trigger(input, 'htmx:trigger');
    }
}
```

---

## Form Input Optimization

### Pattern 7: Korean-Optimized Form
```html
<form hx-post="/api/submit"
      hx-target="#form-result"
      id="korean-form">
    <div class="form-group">
        <label for="name">이름</label>
        <input type="text"
               id="name"
               name="name"
               class="korean-input"
               required>
    </div>

    <div class="form-group">
        <label for="comment">댓글</label>
        <textarea id="comment"
                  name="comment"
                  class="korean-input"
                  rows="4"
                  required></textarea>
    </div>

    <button type="submit" class="btn-submit">제출</button>
</form>

<div id="form-result"></div>

<style>
.korean-input {
    font-family: "Malgun Gothic", "맑은 고딕", "Apple SD Gothic Neo", sans-serif;
    font-size: 16px;
    padding: 10px;
    border: 1px solid #ddd;
    border-radius: 4px;
    width: 100%;

    /* Korean text optimization */
    word-break: keep-all;
    word-wrap: break-word;
    letter-spacing: -0.3px;
    line-height: 1.6;
}

textarea.korean-input {
    resize: vertical;
    min-height: 100px;
}
</style>

<script>
// Initialize IME handling for all Korean inputs
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
```

### Pattern 8: Validation with Korean Messages
```html
<form hx-post="/api/validate"
      hx-target="#validation-result">
    <input type="email"
           name="email"
           class="korean-input"
           placeholder="이메일을 입력하세요">
    <button type="submit">확인</button>
</form>

<div id="validation-result"></div>

<!-- Server response for invalid email -->
<div class="error-message">
    올바른 이메일 형식이 아닙니다
</div>

<!-- Server response for valid email -->
<div class="success-message">
    ✓ 사용 가능한 이메일입니다
</div>
```

---

## Typography & CSS

### Pattern 9: Korean Typography System
```css
/* Korean font stack */
:root {
    --font-korean: -apple-system, BlinkMacSystemFont,
                   "Malgun Gothic", "맑은 고딕",
                   "Apple SD Gothic Neo", "Noto Sans KR",
                   sans-serif;
}

/* Base Korean text styling */
.korean-text {
    font-family: var(--font-korean);
    word-break: keep-all;       /* Prevent breaking within words */
    word-wrap: break-word;      /* Allow breaking between words */
    letter-spacing: -0.3px;     /* Tighten spacing for Korean */
    line-height: 1.6;           /* Better readability */
}

/* Headings */
.korean-heading {
    font-family: var(--font-korean);
    font-weight: 700;
    word-break: keep-all;
    letter-spacing: -0.5px;
    line-height: 1.4;
}

/* Paragraph text */
.korean-paragraph {
    font-family: var(--font-korean);
    word-break: keep-all;
    letter-spacing: -0.3px;
    line-height: 1.8;
}

/* Long-form content */
.korean-article {
    font-family: var(--font-korean);
    font-size: 16px;
    word-break: keep-all;
    letter-spacing: -0.3px;
    line-height: 1.8;
    text-align: justify;
}

/* Buttons and UI */
.korean-button {
    font-family: var(--font-korean);
    font-weight: 500;
    letter-spacing: -0.2px;
}
```

### Pattern 10: Responsive Korean Text
```css
/* Mobile-first Korean typography */
.korean-responsive {
    font-family: var(--font-korean);
    word-break: keep-all;
    letter-spacing: -0.3px;

    /* Mobile */
    font-size: 14px;
    line-height: 1.6;
}

/* Tablet and up */
@media (min-width: 768px) {
    .korean-responsive {
        font-size: 16px;
        line-height: 1.7;
    }
}

/* Desktop */
@media (min-width: 1024px) {
    .korean-responsive {
        font-size: 18px;
        line-height: 1.8;
    }
}
```

---

## Localized Messages

### Pattern 11: Loading States (Korean)
```html
<!-- Search loading -->
<div class="htmx-indicator">🔍 검색 중...</div>

<!-- Saving -->
<div class="htmx-indicator">💾 저장 중...</div>

<!-- Loading content -->
<div class="htmx-indicator">⏳ 불러오는 중...</div>

<!-- Processing -->
<div class="htmx-indicator">⚙️ 처리 중...</div>

<!-- Uploading -->
<div class="htmx-indicator">📤 업로드 중...</div>
```

### Pattern 12: Error Messages (Korean)
```html
<!-- Generic error -->
<div class="error-message">
    ❌ 오류가 발생했습니다
</div>

<!-- Network error -->
<div class="error-message">
    🌐 네트워크 오류가 발생했습니다. 다시 시도해주세요.
</div>

<!-- Validation error -->
<div class="error-message">
    ⚠️ 입력하신 정보를 확인해주세요
</div>

<!-- Not found -->
<div class="error-message">
    🔍 요청하신 내용을 찾을 수 없습니다
</div>

<!-- Permission denied -->
<div class="error-message">
    🔒 접근 권한이 없습니다
</div>
```

### Pattern 13: Success Messages (Korean)
```html
<!-- Save success -->
<div class="success-message">
    ✅ 저장되었습니다
</div>

<!-- Update success -->
<div class="success-message">
    ✅ 수정되었습니다
</div>

<!-- Delete success -->
<div class="success-message">
    ✅ 삭제되었습니다
</div>

<!-- Complete -->
<div class="success-message">
    ✅ 완료되었습니다
</div>

<!-- Sent -->
<div class="success-message">
    ✅ 전송되었습니다
</div>
```

### Pattern 14: Confirmation Messages (Korean)
```html
<!-- Delete confirmation -->
<button hx-delete="/api/items/123"
        hx-confirm="정말 삭제하시겠습니까?">
    삭제
</button>

<!-- Discard confirmation -->
<button hx-confirm="작성 중인 내용이 사라집니다. 계속하시겠습니까?">
    취소
</button>

<!-- Irreversible action -->
<button hx-confirm="이 작업은 되돌릴 수 없습니다. 계속하시겠습니까?">
    실행
</button>
```

---

## Date & Number Formatting

### Pattern 15: Go Date Formatting (Korean)
```go
package handlers

import (
    "time"
    "fmt"
)

// Format date in Korean style
func FormatKoreanDate(t time.Time) string {
    return t.Format("2006년 1월 2일")
}

// Format datetime in Korean style
func FormatKoreanDateTime(t time.Time) string {
    return t.Format("2006년 1월 2일 15시 04분")
}

// Format relative time in Korean
func FormatKoreanRelativeTime(t time.Time) string {
    now := time.Now()
    diff := now.Sub(t)

    switch {
    case diff < time.Minute:
        return "방금 전"
    case diff < time.Hour:
        mins := int(diff.Minutes())
        return fmt.Sprintf("%d분 전", mins)
    case diff < 24*time.Hour:
        hours := int(diff.Hours())
        return fmt.Sprintf("%d시간 전", hours)
    case diff < 30*24*time.Hour:
        days := int(diff.Hours() / 24)
        return fmt.Sprintf("%d일 전", days)
    default:
        return FormatKoreanDate(t)
    }
}

// Weekday in Korean
func FormatKoreanWeekday(t time.Time) string {
    weekdays := map[time.Weekday]string{
        time.Sunday:    "일요일",
        time.Monday:    "월요일",
        time.Tuesday:   "화요일",
        time.Wednesday: "수요일",
        time.Thursday:  "목요일",
        time.Friday:    "금요일",
        time.Saturday:  "토요일",
    }
    return weekdays[t.Weekday()]
}
```

### Pattern 16: Go Number Formatting (Korean)
```go
import (
    "fmt"
    "github.com/dustin/go-humanize"
)

// Format number with Korean counter
func FormatKoreanCount(n int) string {
    return fmt.Sprintf("%s개", humanize.Comma(int64(n)))
}

// Format file size in Korean
func FormatKoreanFileSize(bytes int64) string {
    size := humanize.Bytes(uint64(bytes))
    // Convert "1.5 MB" to "1.5MB"
    return size
}

// Format currency (KRW)
func FormatKoreanCurrency(amount int) string {
    return fmt.Sprintf("₩%s", humanize.Comma(int64(amount)))
}

// Format percentage
func FormatKoreanPercentage(value float64) string {
    return fmt.Sprintf("%.1f%%", value)
}
```

### Pattern 17: JavaScript Number Formatting (Korean)
```javascript
// Format number with commas
function formatKoreanNumber(num) {
    return num.toLocaleString('ko-KR') + '개';
}

// Format currency
function formatKoreanCurrency(amount) {
    return '₩' + amount.toLocaleString('ko-KR');
}

// Format file size
function formatKoreanFileSize(bytes) {
    const units = ['바이트', 'KB', 'MB', 'GB', 'TB'];
    let size = bytes;
    let unitIndex = 0;

    while (size >= 1024 && unitIndex < units.length - 1) {
        size /= 1024;
        unitIndex++;
    }

    return size.toFixed(1) + units[unitIndex];
}

// Usage in HTMX component
document.body.addEventListener('htmx:afterSwap', (e) => {
    e.detail.elt.querySelectorAll('.korean-number').forEach(el => {
        const num = parseInt(el.textContent);
        el.textContent = formatKoreanNumber(num);
    });
});
```

---

## Validation Messages

### Pattern 18: Form Validation (Korean)
```html
<form hx-post="/api/submit" hx-target="#result">
    <div class="form-group">
        <input type="email"
               name="email"
               required
               class="korean-input">
        <span class="validation-error">
            올바른 이메일 주소를 입력해주세요
        </span>
    </div>

    <div class="form-group">
        <input type="password"
               name="password"
               required
               minlength="8"
               class="korean-input">
        <span class="validation-error">
            비밀번호는 최소 8자 이상이어야 합니다
        </span>
    </div>

    <button type="submit">제출</button>
</form>
```

### Pattern 19: Common Validation Messages
```javascript
const KOREAN_VALIDATION_MESSAGES = {
    required: '필수 입력 항목입니다',
    email: '올바른 이메일 형식이 아닙니다',
    minLength: (min) => `최소 ${min}자 이상 입력해주세요`,
    maxLength: (max) => `최대 ${max}자까지 입력 가능합니다`,
    pattern: '형식이 올바르지 않습니다',
    min: (min) => `${min} 이상의 값을 입력해주세요`,
    max: (max) => `${max} 이하의 값을 입력해주세요`,
    url: '올바른 URL 형식이 아닙니다',
    number: '숫자만 입력 가능합니다',
    tel: '올바른 전화번호 형식이 아닙니다',
    date: '올바른 날짜 형식이 아닙니다',
};
```

---

## Loading States

### Pattern 20: Korean Loading Indicators
```html
<!-- Spinner with Korean text -->
<div class="loading-spinner htmx-indicator">
    <div class="spinner"></div>
    <span>로딩 중...</span>
</div>

<!-- Progress bar with Korean text -->
<div class="loading-progress htmx-indicator">
    <div class="progress-bar">
        <div class="progress-fill"></div>
    </div>
    <span>처리 중... <span class="progress-percent">0%</span></span>
</div>

<!-- Dots animation -->
<div class="loading-dots htmx-indicator">
    <span>로딩 중</span>
    <span class="dot">.</span>
    <span class="dot">.</span>
    <span class="dot">.</span>
</div>

<style>
.loading-spinner {
    display: flex;
    align-items: center;
    gap: 8px;
    font-family: var(--font-korean);
    color: #666;
}

.spinner {
    width: 20px;
    height: 20px;
    border: 2px solid #f3f3f3;
    border-top: 2px solid #0066cc;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    0% { transform: rotate(0deg); }
    100% { transform: rotate(360deg); }
}

.loading-dots .dot {
    animation: blink 1.4s infinite;
}

.loading-dots .dot:nth-child(2) { animation-delay: 0.2s; }
.loading-dots .dot:nth-child(3) { animation-delay: 0.4s; }

@keyframes blink {
    0%, 20% { opacity: 0; }
    50% { opacity: 1; }
    100% { opacity: 0; }
}
</style>
```

---

## Best Practices

### 1. Always Handle IME Events
```javascript
// ✅ Good: Handle IME events
input.addEventListener('compositionstart', () => { isComposing = true; });
input.addEventListener('compositionend', () => { isComposing = false; });

// ❌ Bad: Ignore IME events
input.addEventListener('keyup', () => { /* trigger immediately */ });
```

### 2. Use Proper Korean Fonts
```css
/* ✅ Good: Korean-optimized font stack */
font-family: -apple-system, BlinkMacSystemFont, "Malgun Gothic", "맑은 고딕", sans-serif;

/* ❌ Bad: Generic sans-serif only */
font-family: Arial, sans-serif;
```

### 3. Prevent Word Breaking
```css
/* ✅ Good: Keep Korean words together */
word-break: keep-all;

/* ❌ Bad: Break anywhere */
word-break: break-all;
```

### 4. Appropriate Debounce Timing
```html
<!-- ✅ Good: 500ms minimum for Korean -->
hx-trigger="keyup changed delay:500ms"

<!-- ❌ Bad: Too fast for IME -->
hx-trigger="keyup changed delay:100ms"
```

### 5. Use Native Korean Messages
```html
<!-- ✅ Good: Natural Korean -->
<div>저장되었습니다</div>

<!-- ❌ Bad: Awkward translation -->
<div>당신의 작업이 저장 완료 되었습니다</div>
```

### 6. Context-Aware Formatting
```javascript
// ✅ Good: Context-aware counters
'게시물 3개'  // articles
'댓글 5개'    // comments
'좋아요 10개' // likes

// ❌ Bad: Generic counter
'items: 3'
```

### 7. Proper Line Height
```css
/* ✅ Good: Readable line height for Korean */
line-height: 1.6;

/* ❌ Bad: Too tight for Korean */
line-height: 1.2;
```

### 8. Test with Real Korean Content
```
✅ Good: Test with: 한글, 혼합된 English text, 숫자 123, 특수문자!
❌ Bad: Test with: Lorem ipsum dolor sit amet
```

---

## Complete Example: Korean-Optimized Search

```html
<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>한글 검색</title>
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>
    <style>
        :root {
            --font-korean: -apple-system, BlinkMacSystemFont,
                           "Malgun Gothic", "맑은 고딕", sans-serif;
        }

        body {
            font-family: var(--font-korean);
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
        }

        .search-container {
            margin: 20px 0;
        }

        .korean-input {
            font-family: var(--font-korean);
            font-size: 16px;
            padding: 12px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            width: 100%;
            word-break: keep-all;
            letter-spacing: -0.3px;
        }

        .korean-input:focus {
            outline: none;
            border-color: #0066cc;
        }

        .htmx-indicator {
            display: none;
            margin-top: 10px;
            color: #666;
        }

        .htmx-request .htmx-indicator {
            display: block;
        }

        .search-results {
            margin-top: 20px;
        }

        .result-item {
            padding: 15px;
            border: 1px solid #e0e0e0;
            border-radius: 4px;
            margin-bottom: 10px;
            word-break: keep-all;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="search-container">
        <h1>한글 검색</h1>
        <input type="text"
               id="korean-search"
               name="q"
               class="korean-input"
               hx-get="/api/search"
               hx-trigger="keyup changed delay:500ms"
               hx-target="#search-results"
               hx-indicator="#search-loading"
               placeholder="검색어를 입력하세요"
               autocomplete="off">

        <div id="search-loading" class="htmx-indicator">
            🔍 검색 중...
        </div>

        <div id="search-results" class="search-results"></div>
    </div>

    <script>
    (function() {
        let isComposing = false;
        const input = document.getElementById('korean-search');

        input.addEventListener('compositionstart', () => {
            isComposing = true;
            console.log('한글 조합 시작');
        });

        input.addEventListener('compositionend', () => {
            isComposing = false;
            console.log('한글 조합 완료');
            htmx.trigger(input, 'keyup');
        });

        input.addEventListener('keyup', (e) => {
            if (isComposing) {
                console.log('조합 중 - HTMX 트리거 차단');
                e.stopPropagation();
                return false;
            }
        });
    })();
    </script>
</body>
</html>
```

---

**Version:** 1.0.0
**Last Updated:** 2025-10-25
**Focus:** Korean IME handling, typography, localization
