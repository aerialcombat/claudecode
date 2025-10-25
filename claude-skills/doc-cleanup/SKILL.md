---
name: doc-cleanup
description: Systematic documentation cleanup and reorganization skill for managing project documentation. Use when user requests "clean the documentation", "cleanup docs", "organize documentation", or when documentation has become cluttered with outdated, duplicate, or unnecessary files. Performs discovery, analysis, archival, consolidation, reorganization, and updates to maintain DRY documentation structure.
---

# Documentation Cleanup

## Overview

Systematically clean, consolidate, and reorganize project documentation to reduce context usage and maintain documentation quality. This skill moves outdated documents to `archive/` (hidden from Claude Code), consolidates duplicates, enforces DRY principles, and updates remaining documentation using the doc-maintainer agent.

## When to Use

Invoke this skill when:
- User explicitly requests documentation cleanup ("clean the docs", "organize documentation")
- Documentation has accumulated temporary context files, implementation guides, or outdated references
- Multiple documents cover the same topics with significant overlap
- Documentation structure has become unclear or disorganized
- Context usage is high due to excessive documentation files

## Cleanup Workflow

Follow these steps in order for systematic documentation cleanup.

### Step 1: Discovery and Inventory

First, create a comprehensive inventory of all documentation files.

**Actions:**
1. Use Glob to find all markdown files: `**/*.md`
2. List all documentation files with their locations
3. Group files by category:
   - Core project docs (root level: README.md, ARCHITECTURE.md, etc.)
   - Developer guides (docs/development/, docs/developer/)
   - API documentation (docs/api/, API.md, etc.)
   - Implementation plans/guides (IMPLEMENTATION_*, PHASE_*, etc.)
   - ADRs (docs/decisions/, docs/adr/)
   - Miscellaneous (everything else)

**Output:**
Present the inventory to the user showing:
- Total number of documentation files
- Files grouped by category
- Total size/line count if helpful

**Example:**
```
Documentation Inventory:
- Core (5 files): README.md, ARCHITECTURE.md, SCHEMA.md, ...
- Developer guides (8 files): docs/TESTING.md, docs/SETUP.md, ...
- Implementation guides (12 files): PHASE_1_IMPL.md, MIGRATION_GUIDE.md, ...
- ADRs (3 files): docs/ADR-001-*.md, ...
- Miscellaneous (7 files): NOTES.md, CONTEXT_*.md, ...

Total: 35 documentation files
```

### Step 2: Analysis and Classification

Analyze each document using the criteria in `references/cleanup-criteria.md` to classify documents.

**Read the cleanup criteria:**
```
Read references/cleanup-criteria.md
```

**Classification categories:**
1. **Keep as-is** - Current, unique, well-organized
2. **Archive** - Outdated but potentially valuable
3. **Consolidate** - Duplicate/overlapping content
4. **Update** - Needs content refresh
5. **Delete** - Empty stubs or clearly wrong

**Analysis checklist for each document:**
- [ ] Read first 50 lines and last 20 lines (or full file if small)
- [ ] Check "Last Updated" date (if present)
- [ ] Identify references to code/features/architecture
- [ ] Compare with other documents for overlap
- [ ] Assess current relevance

**Output:**
Present classification results to the user:
```
Classification Results:

Archive (8 files):
- PHASE_1_IMPLEMENTATION.md (completed feature)
- MIGRATION_V1_TO_V2.md (migration complete)
- OLD_ARCHITECTURE.md (superseded)
...

Consolidate (6 files into 2):
- SETUP.md + INSTALLATION.md + GETTING_STARTED.md → GETTING_STARTED.md
- API.md + API_REFERENCE.md → API.md
...

Update (5 files):
- ARCHITECTURE.md (references old structure)
- README.md (stale quickstart)
...

Keep as-is (12 files):
- SCHEMA.md
- docs/ADR-001-*.md
...

Delete (4 files):
- EMPTY_STUB.md
- TEMP_NOTES.md
...
```

**Ask for user confirmation before proceeding.**

### Step 3: Execute Archival

Move outdated and unnecessary documents to `archive/` directory.

**Actions:**
1. Ensure `archive/` directory exists (create if needed)
2. Organize archive with subdirectories:
   - `archive/completed-implementations/` - Implementation guides for done features
   - `archive/old-migrations/` - Completed migration guides
   - `archive/superseded/` - Documents replaced by newer versions
   - `archive/context/` - Session-specific context files
3. Move files using Bash `mv` command
4. Track all moved files for the final report

**Example:**
```bash
mkdir -p archive/completed-implementations
mv PHASE_1_IMPLEMENTATION.md archive/completed-implementations/
mv PHASE_2_NOTES.md archive/completed-implementations/
```

**Output:**
Report each file moved:
```
Archived 8 files:
✓ PHASE_1_IMPLEMENTATION.md → archive/completed-implementations/
✓ MIGRATION_V1_TO_V2.md → archive/old-migrations/
...
```

### Step 4: Consolidate Duplicates

Merge duplicate documents into single authoritative sources.

**For each consolidation group:**
1. Read all files in the group completely
2. Identify the best target file (most comprehensive, clearest name)
3. Extract unique content from other files
4. Use Edit tool to merge content into target file
5. Add a note at the top documenting the consolidation
6. Move consolidated files to archive (don't delete - recoverable)

**Consolidation note format:**
```markdown
<!-- Consolidated from: FILE1.md, FILE2.md on YYYY-MM-DD -->
```

**Example workflow:**
```
Consolidating: SETUP.md + INSTALLATION.md + GETTING_STARTED.md

1. Read all three files
2. Target: GETTING_STARTED.md (most comprehensive)
3. Unique content from SETUP.md: Docker setup section
4. Unique content from INSTALLATION.md: Troubleshooting tips
5. Edit GETTING_STARTED.md to add unique content
6. Move SETUP.md and INSTALLATION.md to archive/superseded/
```

**Output:**
Report consolidation actions:
```
Consolidated 6 files into 2:
✓ SETUP.md + INSTALLATION.md → GETTING_STARTED.md
  - Added Docker setup section from SETUP.md
  - Added troubleshooting from INSTALLATION.md
  - Archived SETUP.md, INSTALLATION.md
...
```

### Step 5: Reorganize for DRY Structure

Reorganize remaining documentation into a modular, hierarchical structure following DRY principles.

**Recommended structure** (from `references/cleanup-criteria.md`):
```
docs/
├── README.md                   # Overview and navigation
├── getting-started/
│   ├── INSTALLATION.md
│   └── QUICK_START.md
├── development/
│   ├── TESTING.md
│   ├── DEBUGGING.md
│   └── CONTRIBUTING.md
├── api/
│   ├── REST_API.md
│   └── WEBHOOKS.md
├── deployment/
│   ├── DOCKER.md
│   └── PRODUCTION.md
└── decisions/                  # ADRs
    ├── ADR-001-*.md
    └── ADR-002-*.md
```

**Actions:**
1. Create necessary subdirectories in `docs/`
2. Move files to appropriate locations using Bash `mv`
3. Update cross-references in moved files (find `](../" or `](/` patterns)
4. Create/update navigation files (docs/README.md, main README.md)

**Example:**
```bash
mkdir -p docs/{getting-started,development,api,deployment,decisions}
mv TESTING.md docs/development/
mv API.md docs/api/
# Update relative links in moved files
```

**Output:**
Show new structure:
```
Reorganized documentation structure:

docs/
├── README.md (updated with navigation)
├── getting-started/
│   ├── INSTALLATION.md (moved from root)
│   └── QUICK_START.md (consolidated)
├── development/
│   ├── TESTING.md (moved from root)
│   └── DEBUGGING.md (moved from docs/)
...
```

### Step 6: Update Documentation Content

Use the doc-maintainer agent to update outdated content in remaining documentation.

**Actions:**
1. Invoke the doc-maintainer agent via Task tool:
   ```
   Use Task tool with subagent_type="doc-maintainer"
   ```
2. Provide context about:
   - Recent code changes (if applicable)
   - Files that need updating (from Step 2 classification)
   - Specific sections that are outdated
3. Let doc-maintainer update:
   - ARCHITECTURE.md
   - README.md
   - Getting started guides
   - API documentation

**Prompt for doc-maintainer:**
```
Documentation cleanup has been performed. Please update the following files to reflect current state:

Priority updates:
1. ARCHITECTURE.md - ensure it reflects current system architecture
2. README.md - update quick start and overview
3. docs/getting-started/INSTALLATION.md - verify setup steps
4. docs/api/*.md - check API endpoint accuracy

Context:
- Archived: [list of archived files]
- Consolidated: [list of consolidations]
- Reorganized: [description of new structure]

Please review and update these files for accuracy and completeness.
```

**Output:**
Report doc-maintainer results or skip if user prefers manual updates.

### Step 7: Generate Cleanup Summary

Create a comprehensive summary of all cleanup actions performed.

**Summary format:**
```markdown
# Documentation Cleanup Summary
Date: YYYY-MM-DD

## Actions Performed

### Archived (X files)
- file1.md → archive/category/
- file2.md → archive/category/
...

### Consolidated (X files → Y files)
- source1.md + source2.md → target.md
  Details: [what was merged]
...

### Reorganized
- Old: flat structure with N files in root
- New: modular docs/ structure with subdirectories

Files moved:
- file1.md → docs/category/
...

### Updated (via doc-maintainer)
- ARCHITECTURE.md
- README.md
...

### Deleted (X files)
- stub1.md (empty stub)
...

## Results

- Before: X total documentation files
- After: Y documentation files
- Reduction: Z files (P%)
- Files in archive: A files

## New Documentation Structure

[tree showing final structure]

## Next Steps

- [ ] Review updated documentation for accuracy
- [ ] Consider adding missing sections identified during cleanup
- [ ] Establish documentation update cadence
```

**Actions:**
1. Write summary to `CLEANUP_SUMMARY_YYYY_MM_DD.md` in project root
2. Display summary to user
3. Move summary to archive/ after user reviews (or keep if user prefers)

## Resources

### references/cleanup-criteria.md

Comprehensive criteria for identifying outdated, unnecessary, and duplicate documentation. Includes:
- Identification guidelines (outdated, unnecessary, duplicates)
- Archive vs delete decisions
- Reorganization principles and recommended structure
- Update priorities

Load this file at the start of Step 2 (Analysis) to inform classification decisions.

## Integration with doc-maintainer

This skill works complementarily with the doc-maintainer agent:
- **doc-cleanup**: Structural organization, archival, consolidation
- **doc-maintainer**: Content updates, accuracy verification, ongoing maintenance

Use doc-cleanup first to organize the documentation landscape, then use doc-maintainer to keep content current.

## Best Practices

1. **Always ask for user confirmation** before archiving or consolidating files
2. **Move to archive/ instead of deleting** - provides recovery option
3. **Document consolidations** - add notes showing what was merged
4. **Update cross-references** - fix links when moving files
5. **Create navigation** - add README.md files to help users find docs
6. **Verify critical docs** - ensure ARCHITECTURE.md, README.md, SCHEMA.md are accurate after cleanup

## Example Invocations

**User:** "Clean the documentation"
→ Execute full workflow (Steps 1-7)

**User:** "Organize the docs"
→ Execute full workflow

**User:** "The docs are getting cluttered again"
→ Execute full workflow

**User:** "Archive old implementation guides"
→ Focus on Step 1-3 (Discovery, Analysis, Archival)

**User:** "Consolidate duplicate documentation"
→ Focus on Step 1, 2, 4 (Discovery, Analysis, Consolidation)
