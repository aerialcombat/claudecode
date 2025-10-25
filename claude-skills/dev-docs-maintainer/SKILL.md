---
name: dev-docs-maintainer
description: Automatically maintain comprehensive development documentation across seven core files in docs/ folder (DEVLOG.md, ONBOARDING.md, CODE-INDEX.md, PROGRESS.md, API.md) plus root-level files (CLAUDE.md, README.md). This skill should be used proactively whenever significant code changes occur, including new features, refactoring, bug fixes, architecture changes, or API modifications. Trigger this skill after completing implementation work to ensure documentation stays synchronized with the codebase.
---

# Development Documentation Maintainer

## Overview

Maintain a comprehensive, consistent documentation system across seven interconnected documentation files that serve different audiences and purposes. This skill ensures documentation remains accurate, complete, and up-to-date by automatically updating relevant files in response to code changes. Most documentation lives in the `docs/` folder, with CLAUDE.md and README.md at the project root for easy discovery.

The skill manages documentation files in the `docs/` folder:
- **docs/DEVLOG.md**: Version-based development changelog
- **docs/ONBOARDING.md**: Architecture guide for new developers
- **docs/CODE-INDEX.md**: Comprehensive source code mapping
- **docs/PROGRESS.md**: Current project status and roadmap
- **docs/API.md**: Complete API reference (when applicable)
- **CLAUDE.md**: Project guide for Claude Code (root level)
- **README.md**: Project overview and quick start (root level)

## When to Use This Skill

Trigger this skill proactively in these scenarios:

- **After Feature Implementation**: New features, enhancements, or capabilities added
- **After Refactoring**: Code structure, architecture, or module organization changes
- **After Bug Fixes**: Fixes that reveal design issues or affect documented behavior
- **After API Changes**: Any modifications to public interfaces or endpoints
- **After Configuration Updates**: Changes to setup, environment, or deployment
- **After Dependency Changes**: Major dependency updates or additions
- **When Project Status Changes**: Milestone completion, sprint changes, or blockers
- **When Asked**: User explicitly requests documentation update

**Do NOT trigger for**:
- Trivial typo fixes in code
- Minor dependency patch updates
- Work-in-progress commits
- Experimental or temporary code

## Documentation Workflow

### Step 1: Analyze Changes

Before updating documentation, analyze what changed:

1. **Review recent commits** (if using version control):
   ```bash
   git log --oneline -10
   git diff HEAD~5..HEAD --stat
   ```

2. **Identify change categories**:
   - New features or modules
   - Architecture or structure changes
   - API endpoint modifications
   - Configuration or setup changes
   - Bug fixes with design implications
   - Performance optimizations
   - Dependency updates

3. **Determine affected audiences**:
   - New users (README)
   - Claude Code / AI assistants (CLAUDE.md)
   - New developers (docs/ONBOARDING.md)
   - Current team (docs/DEVLOG.md, docs/PROGRESS.md)
   - API consumers (docs/API.md)
   - Future maintainers (docs/CODE-INDEX.md)

### Step 2: Determine Which Documents to Update

Based on the change analysis, decide which documentation files need updates:

| Change Type | DEVLOG | README | CLAUDE.md | ONBOARDING | CODE-INDEX | PROGRESS | API |
|-------------|--------|--------|-----------|------------|------------|----------|-----|
| New feature | ✅ | ✅ | ✅ | Maybe | ✅ | ✅ | If API |
| Refactoring | ✅ | No | Maybe | ✅ | ✅ | Maybe | No |
| Bug fix | If significant | No | No | No | No | ✅ | No |
| API change | ✅ | If public | ✅ | Maybe | ✅ | ✅ | ✅ |
| Architecture change | ✅ | Maybe | ✅ | ✅ | ✅ | Maybe | No |
| Config/setup change | ✅ | ✅ | ✅ | ✅ | No | No | No |
| New module/file | ✅ | No | ✅ | ✅ | ✅ | ✅ | No |
| Performance optimization | ✅ | No | No | No | No | ✅ | No |

**Note**: All docs except README and CLAUDE.md are in the `docs/` folder.

### Step 3: Update Each Document

For each document that needs updating, follow the specific workflow below.

## Document-Specific Workflows

### CLAUDE.md Workflow

**Purpose**: Project guide for Claude Code and AI assistants

**Location**: Project root (`CLAUDE.md`)

**When to Update**:
- New features or major functionality added
- Architecture or technology stack changes
- New modules, services, or components created
- Configuration or setup changes
- API changes
- Documentation structure changes

**Process**:

1. **Read current CLAUDE.md** to understand existing content

2. **Update Project Overview section**:
   - Brief project description
   - Current version
   - Tech stack summary

3. **Update Documentation Map section**:
   - Ensure all documentation files are listed with descriptions
   - Verify paths to docs/ folder are correct
   - Add new documentation files if created
   - **IMPORTANT**: Include clear descriptions of WHEN to use each doc:
     - **docs/DEVLOG.md**: "When to check: To understand historical decisions and development context"
     - **docs/ONBOARDING.md**: "When to use: Setting up development environment, understanding architecture"
     - **docs/CODE-INDEX.md**: "When to use: Finding specific code locations, understanding module structure"
     - **docs/PROGRESS.md**: "When to check: Understanding current project status and priorities"
     - **docs/API.md**: "When to use: Working with API endpoints, integrating with the service"
     - **README.md**: "When to use: Quick start, basic project overview"

4. **Update Key Locations section**:
   - Add new important directories or files
   - Update module locations if restructured
   - Reference docs/CODE-INDEX.md for comprehensive mapping

5. **Update Quick Reference section**:
   - Add new key concepts or patterns
   - Update architecture notes
   - Add new important commands or operations

6. **Keep CLAUDE.md concise**:
   - Under 200 lines total
   - High-level overview only
   - Link to detailed docs in docs/ folder
   - Focus on what Claude needs to know to help effectively

**Example Structure**:
```markdown
# Project Name

> Brief description of what this project does

**Version**: vX.Y.Z
**Tech Stack**: [Primary technologies]

## Documentation Map

For comprehensive project documentation, see the `docs/` folder:

- **[docs/DEVLOG.md](docs/DEVLOG.md)**: Development history and technical decisions
  - *When to use*: Understanding past decisions, historical context, why things were built a certain way
- **[docs/ONBOARDING.md](docs/ONBOARDING.md)**: Architecture guide and complete setup for new developers
  - *When to use*: Setting up development environment, understanding system architecture, learning key concepts
- **[docs/CODE-INDEX.md](docs/CODE-INDEX.md)**: Comprehensive source code mapping with all classes, methods, and modules
  - *When to use*: Finding specific code locations, understanding module structure, navigating the codebase
- **[docs/PROGRESS.md](docs/PROGRESS.md)**: Current project status, active work, and roadmap
  - *When to use*: Understanding current priorities, checking project status, seeing what's in progress
- **[docs/API.md](docs/API.md)**: Complete API reference with endpoints and examples
  - *When to use*: Working with API endpoints, integrating with the service, understanding request/response formats
- **[README.md](README.md)**: Quick start guide and project overview
  - *When to use*: Initial project setup, basic usage examples, getting started quickly

## Key Locations

- Source code: `src/`
- Tests: `tests/`
- Configuration: `config/`
- Main entry: `src/main.ts`

See docs/CODE-INDEX.md for complete code structure.

## Quick Reference

### Architecture

[Brief architecture summary - 2-3 sentences]

See docs/ONBOARDING.md for detailed architecture.

### Key Concepts

- **Concept 1**: Brief explanation
- **Concept 2**: Brief explanation

### Common Tasks

- Run dev: `npm run dev`
- Run tests: `npm test`
- Build: `npm run build`
```

### docs/DEVLOG.md Workflow

**Purpose**: Create historical record of changes and decisions

**When to Update**: After every significant change

**Location**: `docs/DEVLOG.md`

**Process**:

1. **Read current docs/DEVLOG.md** to understand entry format and style

2. **Create new entry** at the top with current version:
   ```markdown
   ## [vX.Y.Z] - Clear, Descriptive Title
   ```

3. **Include these sections**:
   - **Context**: Why this change was needed
   - **Changes Made**: What was implemented (list of changes)
   - **Technical Decisions**: Key choices and rationale
   - **Impact**: Areas affected, breaking changes, migration notes
   - **References**: Links to PRs, issues, related docs

4. **Follow best practices**:
   - Focus on "why" not just "what"
   - Include file paths and affected modules
   - Document alternatives considered
   - Note any tradeoffs made
   - Reference CODE-INDEX for specific locations

5. **Archive old entries** if docs/DEVLOG.md exceeds 1000 lines:
   - Move entries from older major versions to "Archive" section at bottom

6. **Update CLAUDE.md if needed**:
   - If this is a major version change, update version in CLAUDE.md

**Example Entry**:
```markdown
## [v1.2.0] - Implemented User Authentication System

### Context
Application needed secure user authentication to support multi-user features
and role-based access control planned for v2.0.

### Changes Made
- Added UserService (src/services/user_service.ts:15)
- Created authentication middleware (src/middleware/auth.ts:8)
- Implemented JWT token generation and validation
- Added user registration and login endpoints
- Created User model with password hashing

### Technical Decisions
- Chose JWT over sessions for stateless architecture
- Used bcrypt for password hashing (cost factor: 12)
- Access tokens expire in 15 minutes, refresh in 7 days
- Stored refresh tokens in Redis for revocation capability

### Impact
- New dependencies: jsonwebtoken, bcrypt, redis
- Database migration required: users table
- All protected routes now require authentication header
- See ONBOARDING.md for local Redis setup

### References
- PR #42: https://github.com/user/repo/pull/42
- API docs updated: docs/api/authentication.md
```

### README.md Workflow

**Purpose**: Provide project overview and quick start

**Location**: Project root (`README.md`)

**When to Update**:
- New features that change core value proposition
- Setup process changes
- Prerequisite changes
- Major architectural shifts

**Process**:

1. **Read current README.md** to understand existing content

2. **Update relevant sections**:

   **Features Section**:
   - Add new features to bullet list
   - Keep list under 10 items (move minor features to docs)
   - Lead with most important features

   **Quick Start/Installation**:
   - Update commands if changed
   - Add new prerequisites with versions
   - Update example usage if different

   **Project Structure** (if included):
   - Add new major directories
   - Update descriptions if purpose changed

   **Documentation Links**:
   - Ensure all links work
   - Add links to new documentation in docs/ folder
   - Link to docs/ONBOARDING.md for detailed setup

3. **Keep README concise**:
   - Under 500 lines total
   - Move detailed content to docs/ONBOARDING.md
   - Link to docs/ folder instead of duplicating

4. **Maintain consistency**:
   - Match existing tone and style
   - Use same formatting as existing sections
   - Keep code examples in same language/format

5. **Update CLAUDE.md** if major changes:
   - Sync version number
   - Update tech stack if changed
   - Update documentation links

### docs/ONBOARDING.md Workflow

**Purpose**: Comprehensive guide for new developers

**Location**: `docs/ONBOARDING.md`

**When to Update**:
- Architecture changes
- New modules or services
- Setup process changes
- New key concepts introduced
- Technology stack changes

**Process**:

1. **Read current docs/ONBOARDING.md** to understand structure

2. **Update affected sections**:

   **Architecture Overview**:
   - Update diagrams if architecture changed
   - Add new components to component list
   - Explain new architectural patterns

   **Technology Stack**:
   - Add new technologies with brief rationale
   - Update versions if significantly changed
   - Note deprecated technologies

   **Codebase Structure**:
   - Update directory descriptions
   - Add new modules with purposes
   - Update module responsibilities

   **Key Concepts**:
   - Add new domain concepts or patterns
   - Explain non-obvious design decisions
   - Document important abstractions

   **Development Environment**:
   - Update setup steps if changed
   - Add new environment variables
   - Update configuration instructions

3. **Cross-reference docs/CODE-INDEX.md**:
   - Link to docs/CODE-INDEX.md for detailed code locations
   - Don't duplicate comprehensive code mapping
   - Provide high-level overview only

4. **Maintain learning flow**:
   - Ensure sections build on each other
   - Start high-level, get progressively detailed
   - Keep prerequisite knowledge in order

5. **Update CLAUDE.md** if major architectural changes:
   - Add new key concepts to Quick Reference
   - Update architecture summary
   - Update tech stack if changed

### docs/CODE-INDEX.md Workflow

**Purpose**: Comprehensive source code mapping

**Location**: `docs/CODE-INDEX.md`

**When to Update**:
- New files, modules, or directories added
- Code structure refactored
- Classes or interfaces added/changed
- API endpoints added/modified
- Data models created or updated
- Service layer changes
- Entry points changed

**Process**:

1. **Scan codebase structure**:
   - List all directories and their purposes
   - Identify all modules and their responsibilities
   - Map out file organization

2. **Document comprehensively**:

   **Directory Structure**:
   - Complete tree with all directories
   - One-line purpose for each directory
   - Indicate what types of files belong

   **For Each Module**:
   - Location and file paths
   - Purpose and responsibilities
   - Key classes and their roles
   - Public methods with signatures
   - Dependencies (what it uses)
   - Dependents (what uses it)

   **For Each Class/Service**:
   - File location with line number
   - Purpose statement
   - Public methods with:
     - Method signature
     - Purpose
     - Parameters with types and descriptions
     - Return value description
     - Exceptions thrown
     - Usage context
   - Dependencies
   - Used by (which files reference it)

   **For Each Model**:
   - Complete structure with field types
   - Field descriptions
   - Validation rules
   - Relationships to other models
   - Database mapping (if applicable)

   **For Each API Endpoint** (if applicable):
   - HTTP method and path
   - Controller and method handling it
   - File location with line number
   - Purpose
   - Parameters
   - Request/response format
   - Related services

3. **Include line numbers**:
   ```markdown
   **File**: `src/services/user_service.ts:15`
   ```

4. **Show relationships**:
   - Dependency graphs
   - Module interactions
   - Data flow between components

5. **Keep it comprehensive**:
   - This is THE reference for code navigation
   - Include all public interfaces
   - Document all modules, even small ones
   - Show how pieces fit together

6. **Update metadata**:
   ```markdown
   **Last Updated**: vX.Y.Z
   ```

7. **Update CLAUDE.md** if major structure changes:
   - Update Key Locations section with new directories
   - Update key module references
   - Keep CLAUDE.md high-level, link to docs/CODE-INDEX.md for details

**Example Section**:
```markdown
### UserService

**File**: `src/services/user_service.ts:15`

**Purpose**: Manages user account operations including registration, authentication,
profile updates, and account deletion.

**Dependencies**:
- UserRepository (src/repositories/user_repository.ts:10)
- EmailService (src/services/email_service.ts:8)
- AuthService (src/services/auth_service.ts:12)

**Used By**:
- UserController (src/api/controllers/user_controller.ts:20)
- AdminController (src/api/controllers/admin_controller.ts:45)

**Public Methods**:

##### createUser(userData: CreateUserDTO): Promise<User>

**Purpose**: Create new user account with email verification

**Parameters**:
- `userData` (CreateUserDTO): User registration data
  - `email` (string, required): User email address
  - `password` (string, required): Plain text password (min 8 chars)
  - `name` (string, required): Full name

**Returns**: Promise<User> - Created user object without password field

**Throws**:
- ValidationError: If email invalid or password too weak
- DuplicateEmailError: If email already exists

**Key Logic**:
1. Validates email format and password strength
2. Checks for existing user with same email
3. Hashes password using bcrypt
4. Creates user record in database
5. Sends verification email
6. Returns user object (password excluded)

**Used In**:
- POST /api/users (src/api/routes/user_routes.ts:12)
```

### docs/PROGRESS.md Workflow

**Purpose**: Track current status and upcoming work

**Location**: `docs/PROGRESS.md`

**When to Update**:
- Task completion
- New blockers identified
- Sprint/phase changes
- Milestone progress
- Status changes (on track → at risk)

**Process**:

1. **Read current docs/PROGRESS.md** to understand current state

2. **Update relevant sections**:

   **Quick Summary**:
   - Update 1-paragraph overview of current state
   - Highlight most significant recent accomplishment

   **Current Sprint/Phase**:
   - Move completed items from "In Progress" to "Recently Completed"
   - Add new tasks to "In Progress"
   - Update status descriptions
   - Add/remove blockers
   - Update ETAs

   **Recently Completed**:
   - Add just-completed items with completion version
   - Note outcomes and impact
   - Keep only last 5-10 items (archive older ones)

   **Upcoming Work**:
   - Add new planned items
   - Reprioritize based on changes
   - Remove items that started (moved to In Progress)

   **Milestones**:
   - Update progress percentages
   - Mark milestones as completed
   - Adjust target versions if needed

   **Metrics**:
   - Update test coverage if changed significantly
   - Update open issue count
   - Update velocity if sprint completed

   **Blockers & Risks**:
   - Add new blockers
   - Remove resolved blockers
   - Update blocker status

3. **Update metadata**:
   ```markdown
   **Last Updated**: vX.Y.Z
   **Overall Status**: 🟢 On Track
   ```

4. **Archive old sections**:
   - Move completed phases to "Historical Progress" section
   - Keep only current and upcoming content visible

### docs/API.md Workflow

**Purpose**: Complete API reference for consumers

**Location**: `docs/API.md`

**When to Update**:
- New endpoints added
- Endpoint parameters or responses changed
- Authentication changes
- Rate limiting changes
- New error codes
- Breaking changes

**Process**:

1. **Read current docs/API.md** to understand structure

2. **For new endpoints**:
   - Add to appropriate resource section
   - Include complete specification:
     - HTTP method and path
     - Description
     - Parameters (path, query, body)
     - Request example with curl
     - Response examples (success and errors)
     - Authentication requirements
     - Related endpoints

3. **For endpoint changes**:
   - Update affected sections
   - Add deprecation notices if applicable
   - Update examples to reflect changes
   - Note breaking changes prominently

4. **For authentication changes**:
   - Update authentication section
   - Update all affected endpoint docs
   - Provide migration guide if breaking

5. **Update data models**:
   - Add new models with complete schemas
   - Update changed models
   - Show validation rules

6. **Update changelog**:
   - Add entry for this version
   - Note added/changed/deprecated/removed items

7. **Update version number** if applicable

8. **Update CLAUDE.md** if API changes significantly:
   - Note that API documentation is in docs/API.md
   - Add API base URL to Quick Reference if applicable

## File Creation Guidelines

When documentation files don't exist, create them using the templates.

### Creating New Documentation Files

1. **Create docs/ folder** if it doesn't exist:
   ```bash
   mkdir -p docs
   ```

2. **Check which files exist**:
   ```bash
   ls -la *.md docs/*.md
   ```

3. **If file doesn't exist, read template**:
   - Read `references/doc-templates.md`
   - Find template for the file type needed

4. **Create file with proper structure**:
   - Use template as starting point
   - Customize sections for current project
   - Remove template placeholders
   - Fill in actual project information
   - Create in correct location (root vs docs/)

5. **Initialize with current state**:
   - **CLAUDE.md** (root): Project guide for Claude Code
   - **README.md** (root): Project overview and setup
   - **docs/DEVLOG.md**: First entry about project start
   - **docs/ONBOARDING.md**: Document current architecture
   - **docs/CODE-INDEX.md**: Map existing codebase comprehensively
   - **docs/PROGRESS.md**: Document current status
   - **docs/API.md**: Document existing endpoints (if applicable)

### Initial Documentation Population

When creating documentation from scratch, follow this order:

1. **Create CLAUDE.md** (root):
   - Brief project description
   - Current version
   - Tech stack
   - Documentation map pointing to docs/ folder
   - Key locations (src/, tests/, config/)
   - Quick reference (architecture summary, common tasks)

2. **Create README.md** (root):
   - Project description
   - Key features currently working
   - Installation steps
   - Basic usage example
   - Link to docs/ONBOARDING.md for detailed setup

3. **Create docs/CODE-INDEX.md**:
   - Scan entire codebase
   - Document all existing structure
   - Map all current modules, classes, methods
   - This is the most comprehensive effort

4. **Create docs/ONBOARDING.md**:
   - Document current architecture
   - Explain existing design patterns
   - Provide complete setup instructions
   - List key concepts
   - Link to docs/CODE-INDEX.md for code navigation

5. **Create docs/DEVLOG.md**:
   - Start with "Initial Project Setup" entry
   - Document current state
   - Note key architectural decisions already made

6. **Create docs/PROGRESS.md**:
   - Document current phase
   - List current work items
   - Set upcoming milestones

7. **Create docs/API.md** (if applicable):
   - Document all existing endpoints
   - Include authentication
   - Provide examples

## Cross-Document Consistency

Ensure consistency across all documentation:

### Single Source of Truth

- **Project guide for Claude**: CLAUDE.md (root level)
- **Quick start**: README.md (root level)
- **Architecture**: Detailed in docs/ONBOARDING.md, summarized in CLAUDE.md
- **Code locations**: Comprehensive in docs/CODE-INDEX.md, key locations in CLAUDE.md
- **Historical decisions**: Recorded in docs/DEVLOG.md, referenced elsewhere
- **Current status**: Tracked in docs/PROGRESS.md, referenced elsewhere
- **API specs**: Complete in docs/API.md, referenced elsewhere

### Linking Strategy

Always link between documents rather than duplicating:

```markdown
See [docs/ONBOARDING.md](docs/ONBOARDING.md#architecture-overview) for architecture details
See [docs/CODE-INDEX.md](docs/CODE-INDEX.md#userservice) for implementation details
See [docs/DEVLOG.md](docs/DEVLOG.md) entry from v1.2.0 for background
```

### Cross-References to Maintain

- **CLAUDE.md** → All docs/ files in Documentation Map
- **README** → docs/ONBOARDING.md for new developers
- **README** → docs/API.md for API information
- **docs/ONBOARDING.md** → docs/CODE-INDEX.md for code navigation
- **docs/ONBOARDING.md** → docs/DEVLOG.md for recent changes
- **docs/PROGRESS.md** → docs/DEVLOG.md for decision context
- **docs/DEVLOG.md** → docs/CODE-INDEX.md for file locations
- **docs/API.md** → docs/CODE-INDEX.md for implementation
- **All docs** → CLAUDE.md references for Claude-specific guidance

### Avoiding Duplication

- Put detailed information in ONE place
- Put summaries with links elsewhere
- Examples:
  - Architecture diagram: docs/ONBOARDING.md (detailed)
  - Architecture summary: CLAUDE.md (2-3 sentences + link)
  - Architecture mention: README.md (brief + link to docs/ONBOARDING.md)
  - Code structure: docs/CODE-INDEX.md (comprehensive)
  - Key locations: CLAUDE.md (high-level + link to docs/CODE-INDEX.md)

## Quality Checklist

Before completing documentation updates, verify:

**Content Quality**:
- [ ] Information is accurate and current
- [ ] Examples are complete and runnable
- [ ] Code references include file paths and line numbers
- [ ] Technical decisions include rationale
- [ ] No outdated information remains

**Consistency**:
- [ ] Terminology used consistently across docs
- [ ] Cross-references are bidirectional where appropriate
- [ ] No information duplication
- [ ] Formatting matches existing style

**Completeness**:
- [ ] All affected documents updated
- [ ] No broken links
- [ ] All new concepts explained
- [ ] All new code mapped in CODE-INDEX

**Clarity**:
- [ ] Language is clear and concise
- [ ] Audience-appropriate detail level
- [ ] Logical organization
- [ ] Scannable with good headings

**Maintainability**:
- [ ] Easy to update in future
- [ ] Uses templates/patterns
- [ ] Not overly detailed where code suffices
- [ ] Cross-references instead of duplication

## Using Bundled Resources

### references/doc-templates.md

**Contains**: Complete templates for all six documentation files

**When to use**:
- Creating new documentation files
- Ensuring consistent structure
- Understanding expected sections
- Reviewing what to include/exclude

**How to use**:
1. Read template for file type being created/updated
2. Use section structure as guide
3. Adapt template to project specifics
4. Remove template placeholders

### references/best-practices.md

**Contains**: Comprehensive documentation guidelines and best practices

**When to use**:
- Understanding documentation principles
- Deciding level of detail
- Learning document-specific best practices
- Reviewing quality criteria
- Avoiding common pitfalls

**How to use**:
1. Review relevant section before updating documentation
2. Follow guidelines for specific document type
3. Apply writing style guidelines
4. Use as quality checklist

## Automation Notes

Certain aspects of documentation can be automated or semi-automated:

**CODE-INDEX.md**:
- Can extract directory structure programmatically
- Can parse source files for class/function signatures
- Can identify imports for dependency mapping
- Still requires manual descriptions and context

**API Documentation**:
- Can generate from code annotations (Swagger/OpenAPI)
- Can extract endpoint definitions
- Still requires examples and explanations

**PROGRESS.md**:
- Can extract metrics from tools (coverage, issues)
- Can list recent commits
- Still requires human interpretation and context

**Manual is Better For**:
- Design decisions and rationale
- Architecture explanations
- Onboarding narrative
- Historical context
- Strategic direction

## Example Usage Scenario

**Scenario**: Just implemented user authentication system with JWT

**Step 1 - Analyze**:
- New feature: authentication
- New files: UserService, AuthMiddleware, User model
- New API endpoints: POST /api/auth/login, POST /api/auth/register
- New setup requirement: Redis for refresh tokens
- Affects: Architecture, setup process, API

**Step 2 - Determine Documents**:
- ✅ CLAUDE.md - Add auth to key concepts, update version
- ✅ README - Update features, prerequisites (Redis)
- ✅ docs/DEVLOG.md - Record decision to use JWT
- ✅ docs/ONBOARDING.md - Update architecture, setup steps
- ✅ docs/CODE-INDEX.md - Map new services, models, endpoints
- ✅ docs/PROGRESS.md - Mark authentication as completed
- ✅ docs/API.md - Document new auth endpoints

**Step 3 - Update Each**:

1. CLAUDE.md: Add authentication to key concepts, bump version to v1.2.0
2. README: Add authentication to features, Redis to prerequisites, link to docs/
3. docs/DEVLOG.md: Create v1.2.0 entry explaining why JWT, technical decisions
4. docs/ONBOARDING.md: Add auth system to architecture, Redis setup to environment
5. docs/CODE-INDEX.md: Map UserService, AuthMiddleware, User model with all methods
6. docs/PROGRESS.md: Move "Implement authentication" from In Progress to Completed
7. docs/API.md: Document login and register endpoints with examples

**Step 4 - Cross-reference**:
- CLAUDE.md links to docs/API.md for auth endpoints
- docs/DEVLOG.md entry references docs/CODE-INDEX.md for file locations
- README links to docs/API.md for auth details
- docs/ONBOARDING.md references docs/DEVLOG.md for decision context
- docs/API.md references docs/CODE-INDEX.md for implementation details

**Step 5 - Verify**:
- All seven documents updated appropriately
- Links between documents work (especially from root to docs/)
- CLAUDE.md provides quick overview with links to detailed docs
- No information duplicated
- Examples are complete
- Technical decisions explained

## Conclusion

Maintaining comprehensive documentation requires:
- **Proactive updates** after every significant change
- **Consistency** across all documents
- **Appropriate detail** for each audience
- **Cross-referencing** to avoid duplication
- **Quality focus** on clarity and accuracy

Use the templates and best practices provided to ensure documentation remains a valuable asset throughout the project's lifecycle.
