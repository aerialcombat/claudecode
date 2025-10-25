---
name: css-mimic
description: This skill should be used when creating accurate CSS files for webpages by analyzing target websites through screenshots, live URLs, or code snippets. Use when the user requests to "mimic a website's design", "generate CSS based on a site", or "create styles matching a target website". Particularly useful for the Dark project topic portals where consistent, professional styling is needed. Triggers include requests mentioning "CSS generation", "website mimicry", "design extraction", or "style matching".
---

# CSS Mimic

Generate accurate, production-ready CSS for your webpages by analyzing target websites and mapping their design to your HTML structure.

## Overview

The CSS Mimic skill enables comprehensive CSS generation from target websites using multiple input methods (screenshots, live URLs, code snippets) and produces organized, modern CSS that matches your HTML structure. Specifically optimized for the Dark project's topic portal designs but applicable to any web project.

## When to Use This Skill

Activate this skill when:
- "Create CSS based on [website/screenshot]"
- "Mimic the design of [URL]"
- "Generate styles for my topic portal like [example site]"
- "Extract design tokens from [website]"
- "Match my HTML to this website's design"

## Workflow Decision Tree

```
User provides target website info
    ↓
┌─────────────────────────────────┐
│ What inputs are available?      │
└─────────────────────────────────┘
    ↓
    ├─→ Live URL?
    │   └─→ Use extract_css.py (Playwright extraction)
    │
    ├─→ Screenshot?
    │   └─→ Use analyze_colors.py (color palette extraction)
    │
    ├─→ Code snippets?
    │   └─→ Manual analysis + pattern matching
    │
    └─→ User's HTML structure?
        └─→ Check references/dark_project_html.md for alignment
    ↓
Combine extracted design tokens
    ↓
Generate CSS using generate_css_template.py
    ↓
Manual refinement + testing
    ↓
Final CSS integrated with project
```

## Step-by-Step Workflow

### Step 1: Gather Inputs

Collect all available information about the target design:

**Required:**
- User's HTML structure (the code that needs styling)
- Target website information (URL, screenshot, or code snippets)

**Optional but helpful:**
- Specific design aspects to focus on (layout, colors, typography, responsive)
- Existing CSS or design system to integrate with
- Browser/viewport requirements

**Questions to ask:**
- "What website would you like to mimic?"
- "Do you have a live URL or screenshots?"
- "Can you share your HTML structure?"
- "Which aspects are most important (layout, colors, typography, all)?"

### Step 2: Extract Design Tokens

Use the appropriate extraction method based on available inputs:

#### Option A: Extract from Live URL (Most Comprehensive)

```bash
# Run the Playwright-based extraction script
python3 scripts/extract_css.py https://target-website.com --output design_tokens.json

# This extracts:
# - All colors used on the page
# - Font families, sizes, and weights
# - Spacing values (margins, padding)
# - Border radii
# - Box shadows
# - CSS custom properties
# - Layout patterns (flexbox, grid)
```

**Output:** `design_tokens.json` with complete design system

#### Option B: Extract from Screenshots (Visual Analysis)

```bash
# Analyze screenshot for color palette
python3 scripts/analyze_colors.py screenshot.png --output colors.css --json

# This extracts:
# - Dominant color palette
# - Primary, neutral, and accent colors
# - Color categorization
# - CSS variable suggestions
```

**Output:** `colors.css` and `colors.json` with color tokens

#### Option C: Manual Analysis (Code Snippets)

When only code snippets are available:

1. **Inspect the provided CSS/HTML**
2. **Identify patterns:**
   - Color scheme (primary, secondary, neutrals)
   - Typography system (fonts, sizes, weights)
   - Spacing scale (look for repeated values)
   - Layout approach (flexbox vs grid)
3. **Extract tokens manually** into a similar JSON structure
4. **Reference `references/design_tokens.md`** for guidance

### Step 3: Analyze User's HTML Structure

**Critical:** Map target design to user's actual HTML structure.

**For Dark Project:**
1. **Read `references/dark_project_html.md`**
2. **Identify HTML elements:**
   - `.container` - Page width constraint
   - `.sticky-header` - Fixed header
   - `.content-preview` - Content cards
   - `.meta-bar` - Metadata display
   - `.keywords` - Tag display
   - Utility classes (`.flex`, `.text-xl`, etc.)
3. **Match target design to these elements**

**For Other Projects:**
1. **Read user's HTML file**
2. **Identify structure:**
   - Container/wrapper elements
   - Navigation components
   - Content sections
   - Repeated patterns (cards, lists, grids)
3. **Note class names and hierarchy**

### Step 4: Generate CSS Template

Use the extraction script to generate organized CSS:

```bash
# Generate complete CSS from extracted tokens
python3 scripts/generate_css_template.py design_tokens.json --output styles.css

# Optional flags:
# --no-reset       Skip CSS reset
# --no-utilities   Skip utility classes
# --html file.html Include HTML analysis
```

**Output:** `styles.css` with:
- Modern CSS reset
- Custom properties (design tokens)
- Layout patterns (from target site)
- Typography styles
- Responsive breakpoints
- Utility classes

**OR start with base template:**

If extraction isn't available, copy `assets/base_template.css` and customize:
1. Update `:root` CSS variables
2. Modify color palette
3. Adjust typography scale
4. Add component styles

### Step 5: Map CSS to HTML Structure

**Critical step:** Ensure generated CSS matches user's HTML.

**Mapping process:**

1. **Compare class names:**
   ```
   Generated: .card { ... }
   User HTML: <div class="content-preview"> ... </div>
   Action: Rename .card → .content-preview
   ```

2. **Check element hierarchy:**
   ```html
   <!-- User's structure -->
   <div class="meta-bar">
       <span class="content-type">Article</span>
   </div>
   ```
   ```css
   /* Ensure CSS matches */
   .meta-bar {
       display: flex;
       gap: var(--space-2);
   }
   .content-type {
       background: var(--color-primary);
   }
   ```

3. **Preserve existing patterns:**
   - If Dark project: maintain utility class system
   - If custom: match user's naming conventions
   - Don't introduce conflicting class names

4. **Refer to references:**
   - `references/css_patterns.md` - Layout patterns
   - `references/dark_project_html.md` - Dark project specifics
   - `references/design_tokens.md` - Token organization

### Step 6: Refine and Test

**Manual refinement:**

1. **Review generated CSS:**
   - Remove unused styles
   - Consolidate duplicate rules
   - Optimize specificity
   - Add missing component styles

2. **Test responsive behavior:**
   ```css
   /* Ensure breakpoints work */
   @media (max-width: 768px) {
       .container {
           padding-inline: var(--space-4);
       }
   }
   ```

3. **Verify color contrast:**
   - Check text readability (WCAG 4.5:1 for normal text)
   - Test dark mode if applicable
   - Ensure interactive elements are visible

4. **Check browser compatibility:**
   - Use modern CSS features appropriately
   - Provide fallbacks if needed
   - Test in target browsers

**Testing checklist:**
- [ ] All HTML elements have corresponding styles
- [ ] Layout matches target website
- [ ] Colors match target (or are intentionally different)
- [ ] Typography scale is consistent
- [ ] Responsive design works (mobile, tablet, desktop)
- [ ] Dark mode works (if applicable)
- [ ] Interactive states (hover, focus, active) are styled
- [ ] No CSS errors in browser console

### Step 7: Document and Deliver

**Provide user with:**

1. **Final CSS file** with comments explaining sections
2. **Usage instructions:**
   - How to link CSS to HTML
   - CSS variable customization
   - Dark mode activation (if included)
3. **Customization guide:**
   - Which variables to change for colors
   - How to adjust spacing scale
   - Adding custom components
4. **Example HTML** (if requested) showing proper usage

**Example delivery:**

```css
/* ==========================================
   Generated CSS for [Project Name]
   Target: [Website URL or description]
   Generated: [Date]
   ========================================== */

/* To customize:
   1. Edit CSS variables in :root
   2. Adjust spacing scale as needed
   3. Add custom components at bottom
*/

/* ... CSS content ... */
```

## Common Patterns

### Pattern 1: Dark Project Topic Portal

**Scenario:** User wants CSS for a Dark topic portal page.

**Workflow:**
1. Ask for target website URL or screenshot
2. Run `extract_css.py` if URL available
3. **Read `references/dark_project_html.md`** for HTML structure
4. Generate CSS matching Dark's utility class system
5. Ensure Korean typography support
6. Include `data-theme` dark mode
7. Test with `assets/example_portal.html`

**Key considerations:**
- Maintain `.container`, `.sticky-header` patterns
- Use utility classes (`.flex`, `.text-xl`, `.mb-4`)
- Support Korean fonts
- Include HTMX-friendly styling

### Pattern 2: Landing Page from Screenshot

**Scenario:** User provides screenshot, wants landing page CSS.

**Workflow:**
1. Run `analyze_colors.py` on screenshot
2. Manually analyze layout (hero, features, CTA sections)
3. Ask for user's HTML structure
4. Copy `assets/base_template.css` as starting point
5. Update color variables from extracted palette
6. Add component styles (hero, cards, buttons)
7. Create responsive grid layout

**Key considerations:**
- Focus on visual accuracy
- Prioritize color matching
- Design effective hero section
- Ensure CTA buttons are prominent

### Pattern 3: Component Library Matching

**Scenario:** User wants to match an existing design system.

**Workflow:**
1. Extract tokens from target design system
2. Organize into tiered token system:
   - Tier 1: Brand/primitive tokens
   - Tier 2: Semantic tokens
   - Tier 3: Component tokens
3. Reference `references/design_tokens.md`
4. Generate comprehensive variable system
5. Create component styles
6. Document token usage

**Key considerations:**
- Maintain design system hierarchy
- Document token purpose
- Enable easy customization
- Provide usage examples

## Advanced Techniques

### Combining Multiple Inputs

When you have both URL and screenshots:

1. **Extract from URL first** (most accurate)
2. **Use screenshot for visual verification**
3. **Cross-reference** extracted colors with screenshot
4. **Prioritize** URL data for technical values, screenshot for aesthetics

### Handling Responsive Design

To mimic responsive behavior:

1. **Extract at multiple viewport sizes:**
   ```bash
   # Run extraction with different viewports
   python3 scripts/extract_css.py URL --viewport-width 1920
   python3 scripts/extract_css.py URL --viewport-width 768
   python3 scripts/extract_css.py URL --viewport-width 375
   ```

2. **Compare differences** in layout, spacing, typography
3. **Generate media queries** based on breakpoint changes

### Optimizing for Performance

Generated CSS optimization:

1. **Remove unused styles** (inspect user's HTML)
2. **Consolidate duplicate selectors**
3. **Use CSS custom properties** for repeated values
4. **Minify for production** (optional)
5. **Consider critical CSS** for above-the-fold content

## Troubleshooting

### Problem: Generated CSS doesn't match HTML

**Solution:**
- Re-read user's HTML structure
- Check class name mismatches
- Verify element hierarchy
- Manually map CSS selectors

### Problem: Colors don't look right

**Solution:**
- Re-run color extraction
- Verify screenshot quality
- Check color space (sRGB vs P3)
- Manually adjust color variables
- Test in different lighting conditions

### Problem: Layout breaks on mobile

**Solution:**
- Add responsive breakpoints
- Use flexbox `flex-wrap`
- Implement mobile-first approach
- Test with browser dev tools
- Add container queries for components

### Problem: Typography doesn't match

**Solution:**
- Verify font imports
- Check font-weight availability
- Adjust line-height values
- Consider font fallbacks
- Test with actual content length

## Resources

### Scripts

- **`scripts/extract_css.py`** - Playwright-based CSS extraction from live URLs
- **`scripts/analyze_colors.py`** - Color palette extraction from screenshots
- **`scripts/generate_css_template.py`** - Complete CSS generation from tokens

### References

- **`references/css_patterns.md`** - Common layout patterns (flexbox, grid, components)
- **`references/design_tokens.md`** - Design token organization and best practices
- **`references/dark_project_html.md`** - Dark project HTML structure reference

### Assets

- **`assets/base_template.css`** - Modern CSS boilerplate with design tokens
- **`assets/example_portal.html`** - Sample topic portal HTML

## Tips for Success

1. **Always start with understanding the user's HTML structure** - CSS must match HTML, not the other way around
2. **Use the scripts as starting points** - Manual refinement is always needed
3. **Test early and often** - Don't wait until the end to test responsiveness
4. **Document your work** - Comment the CSS to explain token usage and patterns
5. **Maintain design system consistency** - Use variables instead of hardcoded values
6. **Prioritize accessibility** - Check color contrast, focus states, semantic HTML
7. **Think mobile-first** - Start with mobile styles, enhance for larger screens
8. **Keep it maintainable** - Organize CSS logically, use clear naming conventions

## Final Checklist

Before delivering CSS to the user:

- [ ] CSS matches user's HTML structure (class names, hierarchy)
- [ ] Design tokens organized in `:root`
- [ ] Responsive breakpoints implemented
- [ ] Dark mode supported (if requested)
- [ ] All components from HTML are styled
- [ ] Color contrast meets accessibility standards
- [ ] Typography scale is consistent
- [ ] Layout works at all viewport sizes
- [ ] Interactive states styled (hover, focus, active)
- [ ] CSS is commented and documented
- [ ] Usage instructions provided
- [ ] Example or demo available
