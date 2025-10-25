#!/usr/bin/env python3
"""
HTMX Component Test Page Generator

Generates standalone HTML test pages for HTMX components with mock data and server responses.

Usage:
    python test_component.py --component search --output test-search.html
"""

import argparse
import sys
from datetime import datetime

# Test page template
TEST_PAGE_TEMPLATE = '''<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{component_title} - HTMX Component Test</title>

    <!-- HTMX -->
    <script src="https://unpkg.com/htmx.org@1.9.10"></script>

    <!-- Dark v2 CSS (for styling) -->
    <style>
{css_styles}
    </style>
</head>
<body>
    <div class="container" style="max-width: 1200px; margin: 2rem auto; padding: 0 1rem;">
        <header style="margin-bottom: 2rem; padding-bottom: 1rem; border-bottom: 2px solid var(--border);">
            <h1 class="korean-text">Test: {component_title}</h1>
            <p class="text-muted">Generated: {timestamp}</p>
        </header>

        <main>
            <section class="test-section">
                <h2>Component Preview</h2>
                <div class="component-container" style="background: var(--color-bg-secondary); padding: 2rem; border-radius: var(--radius-lg); margin-bottom: 2rem;">
{component_html}
                </div>
            </section>

            <section class="test-section">
                <h2>Test Controls</h2>
                <div style="display: flex; gap: 1rem; margin-bottom: 2rem;">
                    <button onclick="clearResults()" class="btn-secondary">Clear Results</button>
                    <button onclick="toggleMockServer()" class="btn-secondary" id="mock-toggle">Disable Mock Server</button>
                    <button onclick="showNetworkLog()" class="btn-secondary">Show Network Log</button>
                </div>
            </section>

            <section class="test-section">
                <h2>Network Log</h2>
                <div id="network-log" style="background: #1e1e1e; color: #d4d4d4; padding: 1rem; border-radius: var(--radius-md); font-family: monospace; font-size: 0.875rem; max-height: 300px; overflow-y: auto; display: none;">
                    <!-- Network requests will be logged here -->
                </div>
            </section>
        </main>
    </div>

    <!-- Mock Server -->
    <script>
{mock_server_script}
    </script>

    <!-- Test Utilities -->
    <script>
let mockServerEnabled = true;
let networkLog = [];

function clearResults() {{
    const target = document.querySelector('{result_selector}');
    if (target) {{
        target.innerHTML = '';
    }}
    networkLog = [];
    document.getElementById('network-log').innerHTML = '';
    console.log('Results cleared');
}}

function toggleMockServer() {{
    mockServerEnabled = !mockServerEnabled;
    const btn = document.getElementById('mock-toggle');
    btn.textContent = mockServerEnabled ? 'Disable Mock Server' : 'Enable Mock Server';
    console.log('Mock server', mockServerEnabled ? 'enabled' : 'disabled');
}}

function showNetworkLog() {{
    const logDiv = document.getElementById('network-log');
    logDiv.style.display = logDiv.style.display === 'none' ? 'block' : 'none';
}}

function logNetworkRequest(method, url, response) {{
    const timestamp = new Date().toISOString();
    const logEntry = `[${timestamp}] ${method} ${url}\\n${response}\\n`;
    networkLog.push(logEntry);

    const logDiv = document.getElementById('network-log');
    logDiv.innerHTML += `<div style="margin-bottom: 1rem; padding-bottom: 1rem; border-bottom: 1px solid #333;">${logEntry}</div>`;
    logDiv.scrollTop = logDiv.scrollHeight;
}}

// Listen to HTMX events
document.body.addEventListener('htmx:beforeRequest', function(evt) {{
    console.log('HTMX Request:', evt.detail);
}});

document.body.addEventListener('htmx:afterSwap', function(evt) {{
    console.log('HTMX Response:', evt.detail);
}});

document.body.addEventListener('htmx:responseError', function(evt) {{
    console.error('HTMX Error:', evt.detail);
    alert('Request failed. Check console for details.');
}});
    </script>
</body>
</html>
'''

# CSS styles (simplified dark-v2.css)
CSS_STYLES = '''
:root {
    --color-primary: #3b82f6;
    --color-bg: #ffffff;
    --color-bg-secondary: #f9fafb;
    --color-text: #111827;
    --foreground-muted: #6b7280;
    --border: #e5e7eb;
    --border-light: #f3f4f6;
    --radius-sm: 0.25rem;
    --radius-md: 0.5rem;
    --radius-lg: 0.75rem;
    --space-1: 0.25rem;
    --space-2: 0.5rem;
    --space-3: 0.75rem;
    --space-4: 1rem;
    --space-6: 1.5rem;
    --transition-base: 200ms ease;
}

* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Apple SD Gothic Neo", "Nanum Gothic", "Malgun Gothic", sans-serif;
    line-height: 1.6;
    color: var(--color-text);
    background: var(--color-bg);
}

.korean-text {
    word-break: keep-all;
    letter-spacing: -0.3px;
}

.text-muted {
    color: var(--foreground-muted);
}

.btn-secondary {
    padding: 0.5rem 1rem;
    background: var(--color-bg-secondary);
    border: 1px solid var(--border);
    border-radius: var(--radius-md);
    cursor: pointer;
    font-size: 0.875rem;
}

.btn-secondary:hover {
    background: var(--border-light);
}

.htmx-indicator {
    display: none;
    opacity: 0;
}

.htmx-request .htmx-indicator {
    display: block;
    opacity: 1;
    transition: opacity var(--transition-base);
}

.test-section {
    margin-bottom: 3rem;
}

.test-section h2 {
    margin-bottom: 1rem;
    font-size: 1.25rem;
    color: var(--color-text);
}
'''

# Component-specific configurations
COMPONENT_CONFIGS = {
    'search': {
        'title': 'Live Search',
        'result_selector': '#search-results',
        'html': '''
<form class="search-form korean-text"
      role="search"
      hx-get="/api/search"
      hx-trigger="keyup changed delay:500ms"
      hx-target="#search-results"
      hx-indicator="#search-loading">

    <label for="search-input" class="sr-only">콘텐츠 검색</label>
    <input type="search"
           id="search-input"
           name="q"
           placeholder="검색어를 입력하세요..."
           style="width: 100%; padding: 0.75rem; border: 1px solid var(--border); border-radius: var(--radius-md); font-size: 1rem;">
</form>

<div id="search-results" style="margin-top: 1rem;">
    <!-- Results will appear here -->
</div>

<div id="search-loading" class="htmx-indicator korean-text" style="text-align: center; padding: 1rem; color: var(--foreground-muted);">
    검색 중...
</div>
''',
        'mock_server': '''
// Mock search results
const SAMPLE_CONTENT = [
    { id: 1, title: 'HTMX를 사용한 동적 웹 애플리케이션 개발', type: 'Article' },
    { id: 2, title: 'Go와 템플릿으로 서버 사이드 렌더링', type: 'Tutorial' },
    { id: 3, title: 'Korean 텍스트 최적화 방법', type: 'Guide' },
    { id: 4, title: '다크 모드 구현하기', type: 'Article' },
    { id: 5, title: '무한 스크롤 패턴', type: 'Pattern' },
];

document.body.addEventListener('htmx:configRequest', function(evt) {
    if (!mockServerEnabled) return;

    const url = evt.detail.path;
    if (url.includes('/api/search')) {
        evt.preventDefault();

        const query = new URLSearchParams(evt.detail.parameters).get('q');
        let html = '';

        if (!query) {
            html = '<p class="text-muted korean-text">검색어를 입력하세요</p>';
        } else {
            const results = SAMPLE_CONTENT.filter(item =>
                item.title.toLowerCase().includes(query.toLowerCase())
            );

            if (results.length === 0) {
                html = `<p class="text-muted korean-text">"${query}"에 대한 검색 결과가 없습니다</p>`;
            } else {
                html = '<div style="display: flex; flex-direction: column; gap: 0.75rem;">';
                results.forEach(item => {
                    html += `
                        <div style="padding: 1rem; background: white; border: 1px solid var(--border); border-radius: var(--radius-md);">
                            <h3 style="margin-bottom: 0.5rem; font-size: 1rem;">${item.title}</h3>
                            <span style="font-size: 0.75rem; color: var(--foreground-muted);">${item.type}</span>
                        </div>
                    `;
                });
                html += '</div>';
            }
        }

        logNetworkRequest('GET', url, `Query: ${query}, Results: ${results ? results.length : 0}`);

        setTimeout(() => {
            evt.detail.target.innerHTML = html;
            document.body.dispatchEvent(new CustomEvent('htmx:afterSwap', {
                detail: { target: evt.detail.target }
            }));
        }, 300);
    }
});
'''
    },

    'infinite-scroll': {
        'title': 'Infinite Scroll',
        'result_selector': '#content-list',
        'html': '''
<div id="content-list" style="display: flex; flex-direction: column; gap: 1rem;">
    <div class="content-item" style="padding: 1.5rem; background: white; border: 1px solid var(--border); border-radius: var(--radius-md);">
        <h3>초기 콘텐츠 항목 1</h3>
        <p class="text-muted korean-text">Infinite scroll은 사용자가 스크롤할 때 자동으로 더 많은 콘텐츠를 로드합니다</p>
    </div>
</div>

<div hx-get="/api/content?page=2"
     hx-trigger="revealed"
     hx-swap="afterend"
     hx-target="#content-list"
     hx-indicator="#scroll-loading">
</div>

<div id="scroll-loading" class="htmx-indicator korean-text" style="text-align: center; padding: 2rem; color: var(--foreground-muted);">
    로딩 중...
</div>
''',
        'mock_server': '''
let currentPage = 1;
const MAX_PAGES = 5;

document.body.addEventListener('htmx:configRequest', function(evt) {
    if (!mockServerEnabled) return;

    const url = evt.detail.path;
    if (url.includes('/api/content')) {
        evt.preventDefault();

        const pageMatch = url.match(/page=(\\d+)/);
        const page = pageMatch ? parseInt(pageMatch[1]) : 1;

        let html = '';
        if (page <= MAX_PAGES) {
            for (let i = 0; i < 3; i++) {
                const itemNum = (page - 1) * 3 + i + 1;
                html += `
                    <div class="content-item" style="padding: 1.5rem; background: white; border: 1px solid var(--border); border-radius: var(--radius-md); margin-bottom: 1rem;">
                        <h3>콘텐츠 항목 ${itemNum}</h3>
                        <p class="text-muted korean-text">페이지 ${page}의 콘텐츠입니다. 스크롤하면 더 많은 콘텐츠가 로드됩니다.</p>
                    </div>
                `;
            }

            if (page < MAX_PAGES) {
                html += `
                    <div hx-get="/api/content?page=${page + 1}"
                         hx-trigger="revealed"
                         hx-swap="afterend"
                         hx-target="#content-list"
                         hx-indicator="#scroll-loading">
                    </div>
                `;
            } else {
                html += '<div class="text-center text-muted korean-text" style="padding: 2rem;">모든 콘텐츠를 불러왔습니다</div>';
            }
        }

        logNetworkRequest('GET', url, `Page: ${page}, Items: 3`);

        setTimeout(() => {
            const target = document.getElementById('content-list');
            target.insertAdjacentHTML('beforeend', html);
            document.body.dispatchEvent(new CustomEvent('htmx:afterSwap', {
                detail: { target: target }
            }));
        }, 500);
    }
});
'''
    },

    'modal': {
        'title': 'Modal Dialog',
        'result_selector': '#modal-container',
        'html': '''
<button hx-get="/api/content/123/modal"
        hx-target="#modal-container"
        hx-swap="innerHTML"
        style="padding: 0.75rem 1.5rem; background: var(--color-primary); color: white; border: none; border-radius: var(--radius-md); cursor: pointer; font-size: 1rem;">
    Open Modal
</button>

<div id="modal-container"></div>
''',
        'mock_server': '''
document.body.addEventListener('htmx:configRequest', function(evt) {
    if (!mockServerEnabled) return;

    const url = evt.detail.path;
    if (url.includes('/modal')) {
        evt.preventDefault();

        const html = `
            <div class="modal-backdrop" onclick="this.parentElement.remove()" style="position: fixed; top: 0; left: 0; width: 100%; height: 100%; background: rgba(0,0,0,0.5); display: flex; align-items: center; justify-content: center;">
                <div class="modal-dialog" onclick="event.stopPropagation()" style="background: white; border-radius: var(--radius-lg); max-width: 600px; width: 90%; max-height: 80vh; overflow-y: auto;">
                    <div class="modal-header" style="display: flex; align-items: center; justify-content: space-between; padding: 1.5rem; border-bottom: 1px solid var(--border);">
                        <h2 class="modal-title korean-text" style="margin: 0;">콘텐츠 상세보기</h2>
                        <button onclick="this.closest('.modal-backdrop').remove()" style="background: none; border: none; font-size: 1.5rem; cursor: pointer;">✕</button>
                    </div>
                    <div class="modal-body korean-text" style="padding: 1.5rem;">
                        <p>이것은 모달 콘텐츠입니다. HTMX를 사용하여 서버에서 동적으로 로드되었습니다.</p>
                        <p style="margin-top: 1rem;">모달 외부를 클릭하거나 ESC 키를 누르면 닫힙니다.</p>
                    </div>
                    <div class="modal-footer" style="padding: 1.5rem; border-top: 1px solid var(--border); display: flex; justify-content: flex-end; gap: 0.75rem;">
                        <button onclick="this.closest('.modal-backdrop').remove()" style="padding: 0.5rem 1rem; background: var(--color-bg-secondary); border: 1px solid var(--border); border-radius: var(--radius-md); cursor: pointer;">닫기</button>
                    </div>
                </div>
            </div>
        `;

        logNetworkRequest('GET', url, 'Modal content loaded');

        setTimeout(() => {
            evt.detail.target.innerHTML = html;
            document.body.dispatchEvent(new CustomEvent('htmx:afterSwap', {
                detail: { target: evt.detail.target }
            }));
        }, 200);
    }
});

// Close modal on ESC
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        const modal = document.querySelector('.modal-backdrop');
        if (modal) modal.remove();
    }
});
'''
    },
}

def generate_test_page(component_type, output_file):
    """Generate test page for component"""

    if component_type not in COMPONENT_CONFIGS:
        print(f"Error: Unknown component type '{component_type}'")
        print(f"Available types: {', '.join(COMPONENT_CONFIGS.keys())}")
        return False

    config = COMPONENT_CONFIGS[component_type]

    # Generate HTML
    html = TEST_PAGE_TEMPLATE.format(
        component_title=config['title'],
        timestamp=datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        css_styles=CSS_STYLES,
        component_html=config['html'],
        result_selector=config['result_selector'],
        mock_server_script=config['mock_server']
    )

    # Write to file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Generated test page: {output_file}")
    print(f"\nTo test:")
    print(f"1. Open {output_file} in your browser")
    print(f"2. Interact with the component")
    print(f"3. Check Network Log to see HTMX requests")
    print(f"4. Toggle mock server to test real endpoints\n")

    return True

def main():
    parser = argparse.ArgumentParser(
        description='Generate test pages for HTMX components',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=f'''
Available component types:
  {chr(10).join(f"  {k:15} - {COMPONENT_CONFIGS[k]['title']}" for k in COMPONENT_CONFIGS.keys())}

Examples:
  python test_component.py --component search --output test-search.html
  python test_component.py --component infinite-scroll --output test-scroll.html
  python test_component.py --component modal --output test-modal.html
        '''
    )

    parser.add_argument('--component', required=True, choices=COMPONENT_CONFIGS.keys(),
                        help='Component type to test')
    parser.add_argument('--output', required=True, type=str,
                        help='Output HTML file path')

    args = parser.parse_args()

    success = generate_test_page(args.component, args.output)
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
