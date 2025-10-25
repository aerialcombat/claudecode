# Documentation Cleanup Criteria

## Identification Guidelines

### Outdated Documents

A document is considered **outdated** if it contains:

1. **Stale dates**: "Last Updated" more than 3 months ago and doesn't reflect current state
2. **Obsolete references**:
   - References to code structures/files that no longer exist
   - Mentions of deprecated features or old architecture
   - Instructions for processes that have been replaced
3. **Superseded content**: A newer document covers the same topic with updated information
4. **Implementation guides**: Step-by-step guides for features that are now complete

**Examples of outdated docs:**
- `MIGRATION_GUIDE_v1_to_v2.md` (after migration is complete)
- `PHASE_1_IMPLEMENTATION.md` (after Phase 1 is done)
- `TEMPORARY_WORKAROUND.md` (after proper fix is implemented)
- `OLD_ARCHITECTURE.md` (after architecture has changed)

### Unnecessary Documents

A document is considered **unnecessary** if it:

1. **Temporary context**: Created to guide Claude through a specific task but no longer needed
   - `CONTEXT_FOR_BUG_123.md`
   - `IMPLEMENTATION_NOTES_FEATURE_X.md` (after feature is complete)
2. **Redundant information**: Content fully covered in other canonical docs
3. **Empty or stub files**: Placeholders that were never filled in
4. **Session-specific**: Created for a specific development session and not relevant beyond that

**Keep if:**
- Provides historical context that may be valuable later
- Documents architectural decisions (ADRs should be kept)
- Contains lessons learned or important patterns

### Duplicate Documents

Documents are considered **duplicates** if they:

1. **Cover the same topic** with significant overlap (>70% similar content)
2. **Serve the same purpose** but with different names
3. **Multiple versions** of the same document exist (e.g., `README.md` and `README_OLD.md`)

**Common duplicate patterns:**
- `SETUP.md` + `INSTALLATION.md` + `GETTING_STARTED.md`
- `API.md` + `API_REFERENCE.md` + `API_DOCS.md`
- `TESTING.md` + `TEST_GUIDE.md` + `HOW_TO_TEST.md`

**Consolidation strategy:**
- Keep the most comprehensive and up-to-date version
- Merge unique content from others
- Use the clearest name

## Archive vs Delete

**Move to archive/** (recoverable):
- Outdated but might have historical value
- Temporary guides that document completed work
- Old versions of consolidated docs
- Implementation plans for completed features

**Delete** (permanent):
- Empty stub files
- Pure duplicates with no unique content
- Session-specific temporary files
- Clearly wrong or misleading information

## Reorganization Principles

### Modularity (DRY)

1. **Single source of truth**: Each piece of information should exist in exactly one place
2. **Clear hierarchy**: Related docs should be grouped in subdirectories
3. **Cross-references**: Use links instead of duplicating content
4. **Separation of concerns**: Different aspects (setup, API, testing) in separate files

### Recommended Structure

```
docs/
├── README.md                   # Overview and navigation
├── ARCHITECTURE.md             # System design (canonical)
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

archive/                        # Hidden from Claude Code
├── old-migrations/
├── completed-implementations/
└── superseded-guides/
```

### Content Organization

**Core project files (root level):**
- `README.md` - Project overview, quick start
- `ARCHITECTURE.md` - High-level system design
- `SCHEMA.md` - Database schema (if applicable)

**Detailed documentation (docs/):**
- Organized by concern/topic
- Each subdirectory has its own README for navigation
- ADRs in dedicated folder

**Developer guides:**
- `docs/developer/` or `docs/development/`
- Testing, debugging, contributing guides

**API documentation:**
- `docs/api/` for API references
- Separate from implementation guides

## Update Priorities

After cleanup, prioritize updates for:

1. **ARCHITECTURE.md** - Must reflect current system state
2. **README.md** - First impression, must be accurate
3. **API documentation** - Critical for integration
4. **Getting started guides** - Onboarding new developers
5. **Testing guides** - Maintaining code quality

Use the doc-maintainer agent for comprehensive updates after cleanup.
