#!/usr/bin/env python3
"""
HTMX Component Generator

Generates production-ready HTMX components with optional Go handlers,
Korean optimization, and Dark project integration.

Usage:
    python generate_component.py --type search --name topic-search --korean --go-handler

Component Types:
    - search: Live search with debouncing
    - infinite-scroll: Infinite scroll loading
    - modal: Modal dialog system
    - form: Server-validated form
    - pagination: Pagination controls
    - tabs: Tab navigation
    - inline-edit: Inline editing
    - delete-confirm: Delete confirmation
    - toggle: Toggle visibility
    - dropdown: Ajax dropdown
    - sort-filter: Sort/filter controls
    - autocomplete: Autocomplete search
    - drag-drop: Drag-drop sorting
    - realtime: Real-time updates
"""

import argparse
import os
import sys
from pathlib import Path
from datetime import datetime

# Component templates
COMPONENTS = {
    'search': {
        'html': '''<!-- Live Search Component -->
<!-- Generated: {timestamp} -->
<form class="search-form korean-text"
      role="search"
      hx-get="{api_endpoint}"
      hx-trigger="keyup changed delay:{debounce}ms, search"
      hx-target="#{target_id}"
      hx-indicator="#{indicator_id}">

    <label for="{input_id}" class="sr-only">{label_text}</label>
    <input type="search"
           id="{input_id}"
           name="q"
           class="search-input"
           placeholder="{placeholder_text}"
           autocomplete="off"
           aria-label="{aria_label}">

    <button type="submit" class="search-btn" aria-label="{button_label}">
        🔍
    </button>
</form>

<!-- Search Results Container -->
<div id="{target_id}" class="search-results">
    <!-- Results will be loaded here -->
</div>

<!-- Loading Indicator -->
<div id="{indicator_id}" class="htmx-indicator korean-text">
    {loading_text}
</div>

{ime_script}
''',
        'go_handler': '''package handlers

import (
\t"net/http"
\t"strings"

\t"github.com/go-chi/chi/v5"
)

// {HandlerName} handles live search requests
// HTMX endpoint: GET {api_endpoint}
func (h *Handler) {HandlerName}(w http.ResponseWriter, r *http.Request) {{
\t// Extract search query
\tquery := r.URL.Query().Get("q")
\tif query == "" {{
\t\tw.WriteHeader(http.StatusOK)
\t\tw.Write([]byte("<p class='text-muted korean-text'>{empty_message}</p>"))
\t\treturn
\t}}

\t// Perform search (implement your search logic)
\tresults, err := h.searchService.Search(r.Context(), query)
\tif err != nil {{
\t\tw.WriteHeader(http.StatusInternalServerError)
\t\tw.Write([]byte("<p class='text-muted korean-text'>{error_message}</p>"))
\t\treturn
\t}}

\t// Check if HTMX request
\tif r.Header.Get("HX-Request") != "true" {{
\t\t// Handle non-HTMX request (return full page)
\t\th.renderFullSearchPage(w, r, query, results)
\t\treturn
\t}}

\t// Render search results partial
\terr = h.tmpl.ExecuteTemplate(w, "search-results", map[string]interface{{}}{{
\t\t"Query":   query,
\t\t"Results": results,
\t\t"Total":   len(results),
\t}})
\tif err != nil {{
\t\thttp.Error(w, err.Error(), http.StatusInternalServerError)
\t}}
}}
''',
        'params': {
            'api_endpoint': '/api/search',
            'target_id': 'search-results',
            'indicator_id': 'search-loading',
            'input_id': 'search-input',
            'debounce': '500',  # Higher for Korean IME
            'label_text': '콘텐츠 검색',
            'placeholder_text': '검색어를 입력하세요...',
            'aria_label': '검색어 입력',
            'button_label': '검색',
            'loading_text': '검색 중...',
            'empty_message': '검색어를 입력하세요',
            'error_message': '검색 중 오류가 발생했습니다',
        }
    },

    'infinite-scroll': {
        'html': '''<!-- Infinite Scroll Component -->
<!-- Generated: {timestamp} -->
<div id="{container_id}" class="{container_class}">
    {{{{range .{ContentVar}}}}}
        {{{{template "{item_template}" .}}}}
    {{{{end}}}}
</div>

<!-- Scroll Trigger (loads next page when visible) -->
<div hx-get="{api_endpoint}?page={{{{.NextPage}}}}"
     hx-trigger="revealed"
     hx-swap="afterend"
     hx-target="#{container_id}"
     hx-indicator="#{indicator_id}">
</div>

<!-- Loading Indicator -->
<div id="{indicator_id}" class="htmx-indicator korean-text" style="text-align: center; padding: var(--space-4);">
    {loading_text}
</div>

<!-- End of Content Message -->
{{{{if not .HasMore}}}}
<div class="text-center text-muted korean-text" style="padding: var(--space-6);">
    {end_message}
</div>
{{{{end}}}}
''',
        'go_handler': '''package handlers

import (
\t"net/http"
\t"strconv"

\t"github.com/go-chi/chi/v5"
)

// {HandlerName} handles infinite scroll pagination
// HTMX endpoint: GET {api_endpoint}
func (h *Handler) {HandlerName}(w http.ResponseWriter, r *http.Request) {{
\t// Parse page number
\tpageStr := r.URL.Query().Get("page")
\tpage, err := strconv.Atoi(pageStr)
\tif err != nil || page < 1 {{
\t\tpage = 1
\t}}

\t// Load content with pagination (implement your logic)
\tcontent, hasMore, err := h.contentService.LoadPage(r.Context(), page, {PageSize})
\tif err != nil {{
\t\tw.WriteHeader(http.StatusInternalServerError)
\t\tw.Write([]byte("<p class='text-muted korean-text'>{error_message}</p>"))
\t\treturn
\t}}

\t// Check if HTMX request
\tif r.Header.Get("HX-Request") != "true" {{
\t\t// Handle non-HTMX request (return full page)
\t\th.renderFullContentPage(w, r, content, page, hasMore)
\t\treturn
\t}}

\t// Send trigger if no more content
\tif !hasMore {{
\t\tw.Header().Set("HX-Trigger", "noMoreContent")
\t}}

\t// Render content items partial
\terr = h.tmpl.ExecuteTemplate(w, "{item_template}", map[string]interface{{}}{{
\t\t"{ContentVar}": content,
\t\t"NextPage":     page + 1,
\t\t"HasMore":      hasMore,
\t}})
\tif err != nil {{
\t\thttp.Error(w, err.Error(), http.StatusInternalServerError)
\t}}
}}
''',
        'params': {
            'container_id': 'content-list',
            'container_class': 'content-previews',
            'ContentVar': 'Contents',
            'item_template': 'content-preview-regular',
            'api_endpoint': '/api/content',
            'indicator_id': 'scroll-loading',
            'loading_text': '로딩 중...',
            'end_message': '모든 콘텐츠를 불러왔습니다',
            'error_message': '콘텐츠를 불러오는 중 오류가 발생했습니다',
            'PageSize': '20',
        }
    },

    'modal': {
        'html': '''<!-- Modal Component -->
<!-- Generated: {timestamp} -->

<!-- Modal Trigger -->
<a href="{content_url}"
   hx-get="{api_endpoint}"
   hx-target="#{modal_id}"
   hx-swap="innerHTML"
   class="{trigger_class}">
    {trigger_text}
</a>

<!-- Modal Container -->
<div id="{modal_id}" class="modal" style="display: none;">
    <!-- Modal content loaded here -->
</div>

<!-- Modal Template -->
<template id="modal-template">
    <div class="modal-backdrop" onclick="this.parentElement.style.display='none'"></div>
    <div class="modal-dialog" role="dialog" aria-modal="true">
        <div class="modal-header">
            <h2 class="modal-title korean-text">{{{{.Title}}}}</h2>
            <button class="modal-close"
                    onclick="document.getElementById('{modal_id}').style.display='none'"
                    aria-label="{close_label}">
                ✕
            </button>
        </div>
        <div class="modal-body korean-text">
            {{{{.Content}}}}
        </div>
        <div class="modal-footer">
            <button class="btn-primary"
                    onclick="document.getElementById('{modal_id}').style.display='none'">
                {confirm_text}
            </button>
        </div>
    </div>
</template>

<style>
.modal {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    z-index: 1000;
    display: flex;
    align-items: center;
    justify-content: center;
}}

.modal-backdrop {{
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0, 0, 0, 0.5);
    backdrop-filter: blur(4px);
}}

.modal-dialog {{
    position: relative;
    background: var(--color-bg);
    border-radius: var(--radius-lg);
    box-shadow: var(--shadow-xl);
    max-width: 600px;
    width: 90%;
    max-height: 80vh;
    overflow-y: auto;
}}

.modal-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    padding: var(--space-6);
    border-bottom: 1px solid var(--border);
}}

.modal-body {{
    padding: var(--space-6);
}}

.modal-footer {{
    padding: var(--space-6);
    border-top: 1px solid var(--border);
    display: flex;
    justify-content: flex-end;
    gap: var(--space-3);
}}

.modal-close {{
    background: none;
    border: none;
    font-size: var(--font-xl);
    cursor: pointer;
    color: var(--foreground-muted);
}}
</style>

<script>
// Show modal when content loaded
document.body.addEventListener('htmx:afterSwap', function(evt) {{
    if (evt.detail.target.id === '{modal_id}') {{
        evt.detail.target.style.display = 'flex';
    }}
}});

// Close on ESC key
document.addEventListener('keydown', function(evt) {{
    if (evt.key === 'Escape') {{
        document.getElementById('{modal_id}').style.display = 'none';
    }}
}});
</script>
''',
        'go_handler': '''package handlers

import (
\t"net/http"

\t"github.com/go-chi/chi/v5"
)

// {HandlerName} loads content for modal
// HTMX endpoint: GET {api_endpoint}
func (h *Handler) {HandlerName}(w http.ResponseWriter, r *http.Request) {{
\t// Extract content ID from URL
\tcontentID := chi.URLParam(r, "id")
\tif contentID == "" {{
\t\tw.WriteHeader(http.StatusBadRequest)
\t\tw.Write([]byte("<p class='text-muted korean-text'>{error_message}</p>"))
\t\treturn
\t}}

\t// Load content (implement your logic)
\tcontent, err := h.contentService.GetByID(r.Context(), contentID)
\tif err != nil {{
\t\tw.WriteHeader(http.StatusNotFound)
\t\tw.Write([]byte("<p class='text-muted korean-text'>{not_found_message}</p>"))
\t\treturn
\t}}

\t// Render modal content
\terr = h.tmpl.ExecuteTemplate(w, "modal-content", map[string]interface{{}}{{
\t\t"Title":   content.Title,
\t\t"Content": content.BodyHTML,
\t}})
\tif err != nil {{
\t\thttp.Error(w, err.Error(), http.StatusInternalServerError)
\t}}
}}
''',
        'params': {
            'modal_id': 'content-modal',
            'api_endpoint': '/api/content/{id}/modal',
            'content_url': '/content/{id}',
            'trigger_class': 'content-link',
            'trigger_text': '{{.Title}}',
            'close_label': '닫기',
            'confirm_text': '확인',
            'error_message': '콘텐츠를 불러올 수 없습니다',
            'not_found_message': '콘텐츠를 찾을 수 없습니다',
        }
    },

    'form': {
        'html': '''<!-- Server-Validated Form Component -->
<!-- Generated: {timestamp} -->
<form hx-post="{api_endpoint}"
      hx-target="#{form_id}"
      hx-swap="outerHTML"
      hx-indicator="#{indicator_id}"
      id="{form_id}"
      class="korean-text">

    <!-- Form Fields -->
    <div class="form-group">
        <label for="{field_id}">{field_label}</label>
        <input type="text"
               id="{field_id}"
               name="{field_name}"
               class="form-input"
               required
               aria-describedby="{field_id}-error">
        <div id="{field_id}-error" class="form-error"></div>
    </div>

    <!-- Submit Button -->
    <div class="form-actions">
        <button type="submit" class="btn-primary">
            {submit_text}
        </button>
        <button type="reset" class="btn-secondary">
            {reset_text}
        </button>
    </div>

    <!-- Loading Indicator -->
    <div id="{indicator_id}" class="htmx-indicator korean-text">
        {loading_text}
    </div>
</form>

<style>
.form-group {{
    margin-bottom: var(--space-4);
}}

.form-group label {{
    display: block;
    margin-bottom: var(--space-2);
    font-weight: var(--font-medium);
}}

.form-input {{
    width: 100%;
    padding: var(--space-3);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    font-size: var(--font-base);
}}

.form-input:focus {{
    outline: none;
    border-color: var(--color-primary);
    box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
}}

.form-error {{
    color: var(--color-error);
    font-size: var(--font-sm);
    margin-top: var(--space-1);
    display: none;
}}

.form-error:not(:empty) {{
    display: block;
}}

.form-actions {{
    display: flex;
    gap: var(--space-3);
    margin-top: var(--space-6);
}}
</style>
''',
        'go_handler': '''package handlers

import (
\t"encoding/json"
\t"net/http"
)

type FormData struct {{
\t{FieldName} string `json:"{field_name}"`
}}

type ValidationError struct {{
\tField   string `json:"field"`
\tMessage string `json:"message"`
}}

// {HandlerName} handles form submission with validation
// HTMX endpoint: POST {api_endpoint}
func (h *Handler) {HandlerName}(w http.ResponseWriter, r *http.Request) {{
\t// Parse form data
\terr := r.ParseForm()
\tif err != nil {{
\t\tw.WriteHeader(http.StatusBadRequest)
\t\treturn
\t}}

\tformData := FormData{{
\t\t{FieldName}: r.FormValue("{field_name}"),
\t}}

\t// Validate form data
\tif errors := h.validateForm(formData); len(errors) > 0 {{
\t\t// Return form with validation errors
\t\th.renderFormWithErrors(w, formData, errors)
\t\treturn
\t}}

\t// Process form data (implement your logic)
\terr = h.formService.Submit(r.Context(), formData)
\tif err != nil {{
\t\tw.WriteHeader(http.StatusInternalServerError)
\t\tw.Write([]byte("<p class='form-error korean-text'>{error_message}</p>"))
\t\treturn
\t}}

\t// Return success message
\tw.Header().Set("HX-Trigger", "formSubmitted")
\tw.Write([]byte("<p class='text-success korean-text'>{success_message}</p>"))
}}

func (h *Handler) validateForm(data FormData) []ValidationError {{
\terrors := []ValidationError{{}}
\t
\tif data.{FieldName} == "" {{
\t\terrors = append(errors, ValidationError{{
\t\t\tField:   "{field_name}",
\t\t\tMessage: "{required_message}",
\t\t}})
\t}}
\t
\treturn errors
}}
''',
        'params': {
            'form_id': 'data-form',
            'api_endpoint': '/api/form/submit',
            'field_id': 'title',
            'field_name': 'title',
            'FieldName': 'Title',
            'field_label': '제목',
            'submit_text': '저장',
            'reset_text': '초기화',
            'loading_text': '저장 중...',
            'indicator_id': 'form-loading',
            'error_message': '저장 중 오류가 발생했습니다',
            'success_message': '저장되었습니다',
            'required_message': '필수 입력 항목입니다',
        }
    },
}

# IME handling script for Korean input
IME_SCRIPT = '''
<script>
// Korean IME (Input Method Editor) handling
// Prevents premature AJAX requests during Hangul composition
(function() {
    const input = document.getElementById('{input_id}');
    if (!input) return;

    let isComposing = false;

    input.addEventListener('compositionstart', () => {
        isComposing = true;
    });

    input.addEventListener('compositionend', () => {
        isComposing = false;
        // Trigger HTMX after composition completes
        htmx.trigger(input, 'keyup');
    });

    // Prevent triggering during composition
    input.addEventListener('keyup', (e) => {
        if (isComposing) {
            e.stopImmediatePropagation();
        }
    });
})();
</script>
'''

def generate_component(component_type, name, korean=False, go_handler=False, output_dir=None):
    """Generate HTMX component files"""

    if component_type not in COMPONENTS:
        print(f"Error: Unknown component type '{component_type}'")
        print(f"Available types: {', '.join(COMPONENTS.keys())}")
        return False

    component = COMPONENTS[component_type]
    params = component['params'].copy()

    # Add timestamp
    params['timestamp'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    # Add IME script if Korean
    if korean and 'input_id' in params:
        params['ime_script'] = IME_SCRIPT.format(input_id=params['input_id'])
    else:
        params['ime_script'] = ''

    # Update names
    if 'api_endpoint' in params:
        params['api_endpoint'] = params['api_endpoint'].replace('/api/', f'/api/{name}/')

    # Generate handler name
    handler_name = ''.join(word.capitalize() for word in name.split('-'))
    params['HandlerName'] = handler_name

    # Generate HTML
    html_content = component['html'].format(**params)
    html_filename = f"{name}.html"

    # Generate Go handler if requested
    go_content = None
    go_filename = None
    if go_handler and 'go_handler' in component:
        go_content = component['go_handler'].format(**params)
        go_filename = f"{name.replace('-', '_')}_handler.go"

    # Write files
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        html_path = output_path / html_filename
        with open(html_path, 'w', encoding='utf-8') as f:
            f.write(html_content)
        print(f"✅ Generated HTML: {html_path}")

        if go_content:
            go_path = output_path / go_filename
            with open(go_path, 'w', encoding='utf-8') as f:
                f.write(go_content)
            print(f"✅ Generated Go handler: {go_path}")
    else:
        # Print to stdout
        print(f"\n{'='*60}")
        print(f"HTML Component: {html_filename}")
        print(f"{'='*60}")
        print(html_content)

        if go_content:
            print(f"\n{'='*60}")
            print(f"Go Handler: {go_filename}")
            print(f"{'='*60}")
            print(go_content)

    # Generate integration instructions
    print(f"\n{'='*60}")
    print("Integration Instructions")
    print(f"{'='*60}")
    print(f"1. Add HTML component to your template:")
    print(f"   {{{{template \"{name}\" .}}}}")
    print(f"\n2. Add Go handler to your router (cmd/web/main.go):")
    print(f"   mux.Get(\"{params.get('api_endpoint', '/api/...')}\", handlers.{handler_name})")
    print(f"\n3. Test the component visually:")
    print(f"   python scripts/test_component.py --component {component_type} --output test-{name}.html")
    print(f"{'='*60}\n")

    return True

def main():
    parser = argparse.ArgumentParser(
        description='Generate HTMX components with optional Go handlers',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Available component types:
  {chr(10).join(f"  {k:15} - {COMPONENTS[k]['params'].get('description', 'Component')}" for k in COMPONENTS.keys())}

Examples:
  # Simple component
  python generate_component.py --type inline-edit --name post-title

  # With Korean optimization
  python generate_component.py --type search --name topic-search --korean

  # With Go handler
  python generate_component.py --type infinite-scroll --name content-list --go-handler

  # Complete component
  python generate_component.py --type search --name header-search --korean --go-handler --output /path/to/project/
        '''
    )

    parser.add_argument('--type', required=True, choices=COMPONENTS.keys(),
                        help='Type of component to generate')
    parser.add_argument('--name', required=True,
                        help='Name for the component (e.g., topic-search)')
    parser.add_argument('--korean', action='store_true',
                        help='Include Korean IME handling and localized messages')
    parser.add_argument('--go-handler', action='store_true',
                        help='Generate matching Go handler code')
    parser.add_argument('--output', type=str,
                        help='Output directory (if not specified, prints to stdout)')

    args = parser.parse_args()

    success = generate_component(
        component_type=args.type,
        name=args.name,
        korean=args.korean,
        go_handler=args.go_handler,
        output_dir=args.output
    )

    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
