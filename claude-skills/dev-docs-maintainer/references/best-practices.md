# Documentation Best Practices

> Comprehensive guidelines for maintaining high-quality development documentation.

## Core Principles

### 1. Documentation as Code

- Store documentation in version control alongside code
- Review documentation changes in pull requests
- Keep documentation in sync with code changes
- Automate documentation updates where possible

### 2. Progressive Disclosure

- Start with high-level overview
- Provide increasingly detailed information
- Use table of contents for navigation
- Link between related documents

### 3. Audience-Specific Content

- **README.md**: New users and external visitors
- **ONBOARDING.md**: New team members
- **DEVLOG.md**: Current team and future maintainers
- **CODE-INDEX.md**: Developers navigating codebase
- **PROGRESS.md**: Stakeholders and project managers
- **API Docs**: API consumers and integrators

### 4. Maintainability

- Write documentation that's easy to update
- Avoid duplication across documents
- Use cross-references instead of copying
- Automate what can be automated

## Writing Style Guidelines

### Clarity and Conciseness

**Do**:
- Use clear, direct language
- Keep sentences under 20 words when possible
- Use active voice
- Define technical terms on first use

**Don't**:
- Use jargon without explanation
- Write long paragraphs (>5 sentences)
- Assume prior knowledge
- Use ambiguous pronouns (it, that, this)

### Structure

**Do**:
- Use descriptive headings
- Break content into scannable sections
- Include table of contents for long documents
- Use lists for sequential or related items

**Don't**:
- Create deeply nested sections (>3 levels)
- Mix different topics in one section
- Skip heading levels (h1 → h3)

### Code Examples

**Do**:
- Include complete, runnable examples
- Show expected output
- Explain what the code does
- Use realistic examples

**Don't**:
- Use placeholder values without explanation
- Show only fragments without context
- Skip error handling in examples

### Formatting

**Do**:
- Use code blocks with language tags
- Use tables for structured data
- Use bold for emphasis sparingly
- Use emoji for status indicators (✅ ⏳ 🔴 🟡 🟢)

**Don't**:
- Use images for code (use text)
- Overuse formatting
- Use all caps for emphasis

## Document-Specific Guidelines

### CLAUDE.md Best Practices

**Purpose**: Project guide for Claude Code and AI assistants

**Location**: Project root

**Update Frequency**: When project structure, architecture, or key features change

**What to Include**:
- Project overview (name, brief description)
- Current version number
- Tech stack summary
- Documentation map with links to all docs/ files
  - **IMPORTANT**: Include "When to use" guidance for each doc
  - This helps Claude understand which doc to reference for different tasks
- Key directory locations
- Architecture summary (2-3 sentences)
- Key concepts (3-5 bullet points)
- Common commands

**What to Exclude**:
- Detailed implementation (use docs/CODE-INDEX.md)
- Full architecture docs (use docs/ONBOARDING.md)
- Historical changes (use docs/DEVLOG.md)
- Detailed API specs (use docs/API.md)
- Long explanations (keep concise, link to detailed docs)

**Length**: Keep under 200 lines

**Good Example**:
```markdown
# MyApp

> Real-time collaboration platform for distributed teams

**Version**: v2.3.0
**Tech Stack**: Go, React, PostgreSQL, Redis

## Documentation Map

- **[docs/DEVLOG.md](docs/DEVLOG.md)**: Development history and technical decisions
  - *When to use*: Understanding past decisions, historical context
- **[docs/ONBOARDING.md](docs/ONBOARDING.md)**: Setup and architecture guide
  - *When to use*: Setting up development environment, understanding architecture
- **[docs/CODE-INDEX.md](docs/CODE-INDEX.md)**: Comprehensive code structure mapping
  - *When to use*: Finding specific code locations, navigating the codebase
- **[docs/PROGRESS.md](docs/PROGRESS.md)**: Current status and roadmap
  - *When to use*: Understanding current priorities and project status
- **[docs/API.md](docs/API.md)**: Complete API reference
  - *When to use*: Working with API endpoints, integration

## Key Locations

- Backend: `server/`
- Frontend: `client/`
- Shared types: `types/`

## Quick Reference

### Architecture

WebSocket-based real-time sync with CRDT conflict resolution. Event-driven
backend using Redis pub/sub for scaling across multiple instances.

### Key Concepts

- **CRDT Operations**: Conflict-free replicated data types for concurrent edits
- **Event Sourcing**: All changes stored as immutable events
- **Connection Pool**: Reusable WebSocket connections per user

### Common Tasks

- Dev server: `make dev`
- Run tests: `make test`
- Build: `make build`
```

**Bad Example**:
```markdown
# MyApp

This is my app. It does stuff.

Run it with: npm start
```

### docs/DEVLOG.md Best Practices

**Purpose**: Historical record of development decisions and changes

**Location**: `docs/DEVLOG.md`

**Update Frequency**: After each significant change or decision

**What to Include**:
- Version number (vX.Y.Z format)
- Clear, descriptive title
- Context explaining why change was needed
- Technical decisions with rationale
- Files/areas affected
- Breaking changes
- Migration notes

**What to Exclude**:
- Minor bug fixes (unless they reveal design issues)
- Trivial updates (dependency bumps, typo fixes)
- Work-in-progress notes
- Future plans (use PROGRESS.md)

**Good Entry Example**:
```markdown
## [v1.5.0] - Migrated Authentication to JWT

### Context
Session-based auth was causing scaling issues with multiple server instances.
Users were being logged out when requests hit different servers.

### Changes Made
- Replaced express-session with JWT tokens
- Added refresh token rotation
- Updated login/logout endpoints
- Modified auth middleware

### Technical Decisions
- Used RS256 (asymmetric) instead of HS256 to support multiple services
- Set access token expiry to 15 minutes, refresh to 7 days
- Stored refresh tokens in Redis for revocation capability

### Impact
- Breaking change: clients must update auth flow
- Migration: existing sessions invalidated on deployment
- Performance: reduced database queries by 40%

### References
- PR #234
- Design doc: docs/auth-migration.md
```

**Bad Entry Example**:
```markdown
## [v1.5.0] - Fixed auth

Changed auth to use JWT. Works better now.
```

### README.md Best Practices

**Purpose**: First impression and quick start guide

**Location**: Project root

**Update Frequency**: When setup process or core features change

**What to Include**:
- Compelling project description (1-2 paragraphs)
- Key features list
- Quick start with minimal steps
- Prerequisites with versions
- Basic usage example
- Links to detailed documentation
- Support/contact information

**What to Exclude**:
- Detailed architecture (use ONBOARDING.md)
- Complete API reference (use API docs)
- Historical decisions (use DEVLOG.md)
- Internal development notes

**Structure Tips**:
- Keep README under 500 lines
- Put advanced topics in separate docs
- Use badges sparingly (build status, version)
- Include a visual (screenshot/diagram) if helpful

### docs/ONBOARDING.md Best Practices

**Purpose**: Comprehensive guide for new developers

**Location**: `docs/ONBOARDING.md`

**Update Frequency**: When architecture, setup, or key concepts change

**What to Include**:
- High-level architecture overview
- Technology stack with rationale
- Complete development environment setup
- Key concepts and design patterns
- Development workflow
- Testing strategy
- Deployment process
- Team communication channels

**What to Exclude**:
- Marketing content
- Basic Git/programming tutorials
- Content that duplicates README
- Historical context (use DEVLOG.md)

**Organization Tips**:
- Follow logical learning progression
- Link to CODE-INDEX.md for code navigation
- Include diagrams for complex architecture
- Provide checkboxes for setup steps
- Anticipate common questions

**Testing Onboarding Docs**:
- Have new team members follow it
- Note where they get stuck
- Update based on feedback
- Review quarterly

### docs/CODE-INDEX.md Best Practices

**Purpose**: Comprehensive source code navigation reference

**Location**: `docs/CODE-INDEX.md`

**Update Frequency**: After code structure changes, new modules, or refactoring

**Detail Level**: Comprehensive - include all classes, key methods, and relationships

**What to Include**:
- Complete directory structure with descriptions
- All modules with purposes
- Public classes and interfaces
- Key methods with signatures
- Data models with field descriptions
- API endpoints mapped to controllers
- Service layer documentation
- Dependencies between modules
- Entry points and initialization flow
- Configuration locations

**What to Exclude**:
- Implementation details (use code comments)
- Private/internal implementation methods
- Temporary or experimental code
- Generated code (unless it's important)

**Maintenance Strategy**:
- Update when adding new modules
- Update when refactoring structure
- Review when onboarding reveals gaps
- Automate extraction where possible

**Comprehensive Example for a Class**:
```markdown
### UserService

**File**: `src/services/user_service.ts:15`

**Purpose**: Manages user account operations including registration, authentication, profile updates, and account deletion

**Dependencies**:
- `UserRepository` (src/repositories/user_repository.ts:10)
- `EmailService` (src/services/email_service.ts:8)
- `AuthService` (src/services/auth_service.ts:12)

**Used By**:
- `UserController` (src/api/controllers/user_controller.ts:20)
- `AdminController` (src/api/controllers/admin_controller.ts:45)

**Public Methods**:

##### createUser(userData: CreateUserDTO): Promise<User>

**Purpose**: Create a new user account with email verification

**Parameters**:
- `userData` (CreateUserDTO): User registration data
  - `email` (string, required): User email address
  - `password` (string, required): Plain text password (min 8 chars)
  - `name` (string, required): Full name

**Returns**: Promise<User> - Created user object without password

**Throws**:
- `ValidationError`: If email invalid or password too weak
- `DuplicateEmailError`: If email already exists
- `EmailServiceError`: If verification email fails to send

**Key Logic**:
1. Validates email format and password strength
2. Checks for existing user with same email
3. Hashes password using bcrypt
4. Creates user record in database
5. Sends verification email
6. Returns user object (password excluded)

**Used In**:
- POST /api/users (src/api/routes/user_routes.ts:12)
- Admin user creation (src/api/routes/admin_routes.ts:34)

##### updateUserProfile(userId: string, updates: UpdateUserDTO): Promise<User>

[Similar detail level]
```

### docs/PROGRESS.md Best Practices

**Purpose**: Current status and forward-looking roadmap

**Location**: `docs/PROGRESS.md`

**Update Frequency**: Weekly or after significant progress/changes

**What to Include**:
- Current sprint/phase status
- Work in progress with owners
- Recently completed items
- Upcoming work prioritized
- Milestones with progress
- Active blockers
- Key metrics (velocity, coverage, etc.)
- Team capacity

**What to Exclude**:
- Historical sprints (archive old ones)
- Detailed technical implementation
- Code-level decisions (use DEVLOG.md)
- Individual task minutiae

**Status Indicators**:
- 🟢 On Track
- 🟡 At Risk (needs attention)
- 🔴 Blocked (immediate action needed)
- ✅ Completed
- ⏳ In Progress
- ⏸️ Paused

**Metrics to Track**:
- Sprint velocity (stories/week)
- Test coverage percentage
- Open bug count
- Technical debt items
- Release cadence

### docs/API.md Best Practices

**Purpose**: Complete API reference for consumers

**Location**: `docs/API.md`

**Update Frequency**: With every API change (breaking or non-breaking)

**What to Include**:
- All endpoints with examples
- Request/response schemas
- Authentication requirements
- Rate limiting details
- Error codes and handling
- Versioning strategy
- Deprecation notices
- Complete workflow examples

**What to Exclude**:
- Internal implementation details
- Database schema (unless public)
- Future/planned endpoints
- Deprecated endpoints (after sunset)

**Example Quality**:
- Show requests in multiple languages
- Include realistic data (not foo/bar)
- Show error responses, not just success
- Provide complete working examples

**Versioning**:
- Document version in URL or header
- Keep docs for all supported versions
- Clearly mark deprecated features
- Provide migration guides

## Cross-Document Consistency

### Linking Strategy

**Always Link To**:
- README → ONBOARDING.md for new developers
- README → API docs for API users
- ONBOARDING → CODE-INDEX.md for code navigation
- ONBOARDING → DEVLOG.md for recent changes
- PROGRESS → DEVLOG.md for context on decisions
- CODE-INDEX → API docs for endpoint details
- DEVLOG → CODE-INDEX for affected files

**Link Format**:
- Use relative paths: `[DEVLOG](DEVLOG.md)`
- Include anchor links: `[Setup Guide](ONBOARDING.md#development-environment)`
- Keep links DRY (Don't Repeat Yourself)

### Avoiding Duplication

**Single Source of Truth**:
- Architecture overview: ONBOARDING.md
- API specs: API documentation
- Historical decisions: DEVLOG.md
- Code structure: CODE-INDEX.md
- Current status: PROGRESS.md
- Quick start: README.md

**When Information Overlaps**:
- Put detailed version in primary location
- Put summary in secondary location with link
- Example: README has quick start, ONBOARDING has complete setup

### Version Information

**Where to Track**:
- Current version: README.md
- Version history: DEVLOG.md or CHANGELOG.md
- API version: API documentation
- Migration guides: Individual docs per major version

## Automation Opportunities

### What to Automate

**High Value**:
- CODE-INDEX.md generation from source code
- API documentation from code annotations
- Table of contents generation
- Link validation
- Code example testing

**Medium Value**:
- DEVLOG.md entries from git commits
- Changelog generation from PRs
- Dependency version updates in README
- Test coverage in PROGRESS.md

**Low Value** (manual is better):
- Architectural decisions
- Context and rationale
- Design pattern explanations
- Onboarding narrative

### Automation Tools

- **Code extraction**: AST parsers, reflection APIs
- **API docs**: Swagger/OpenAPI, JSDoc, Pydoc
- **ToC generation**: markdown-toc, doctoc
- **Link checking**: markdown-link-check
- **Example testing**: doctest, jest-runner

## Review and Maintenance

### Documentation Review Checklist

**Before Merging Code**:
- [ ] README updated if setup/features changed
- [ ] DEVLOG entry added for significant changes
- [ ] CODE-INDEX updated if structure changed
- [ ] API docs updated if API changed
- [ ] PROGRESS updated if affects current work
- [ ] ONBOARDING updated if architecture changed

**Quality Checks**:
- [ ] All links work
- [ ] Code examples are runnable
- [ ] No outdated information
- [ ] Consistent formatting
- [ ] Clear and concise language
- [ ] Appropriate level of detail

### Regular Maintenance Schedule

**Weekly**:
- Update PROGRESS.md with current status
- Review DEVLOG for week's changes
- Check PROGRESS blockers and metrics

**Monthly**:
- Review CODE-INDEX for accuracy
- Update ONBOARDING if gaps found
- Check all documentation links
- Review and archive old PROGRESS entries

**Quarterly**:
- Comprehensive documentation audit
- Have new team member test ONBOARDING
- Review and update templates
- Clean up outdated information

**Annually**:
- Major documentation refactor if needed
- Update all examples and screenshots
- Validate all external links
- Review documentation strategy

## Common Pitfalls to Avoid

### 1. Documentation Rot

**Problem**: Documentation becomes outdated quickly

**Solutions**:
- Make docs part of Definition of Done
- Review docs in code review
- Set up automated reminders
- Track docs as technical debt

### 2. Over-Documentation

**Problem**: Too much documentation is hard to maintain

**Solutions**:
- Focus on "why" not "what" (code shows what)
- Avoid documenting obvious things
- Use code comments for implementation details
- Keep docs focused on their audience

### 3. Under-Documentation

**Problem**: Missing critical information

**Solutions**:
- Document design decisions immediately
- Note "gotchas" and non-obvious behavior
- Explain architectural choices
- Document the "why" behind the code

### 4. Duplication

**Problem**: Same information in multiple places

**Solutions**:
- Establish single source of truth
- Link instead of copying
- Use includes/references where possible
- Regular deduplication reviews

### 5. Wrong Audience

**Problem**: Documentation doesn't match reader needs

**Solutions**:
- Define clear audience per document
- Use progressive disclosure
- Separate user docs from developer docs
- Get feedback from actual audience

### 6. Stale Examples

**Problem**: Examples don't work anymore

**Solutions**:
- Test examples in CI/CD
- Use actual project code as examples
- Review examples in code review
- Update examples with refactoring

### 7. Missing Context

**Problem**: Documentation assumes too much knowledge

**Solutions**:
- Define terms on first use
- Link to prerequisite knowledge
- Explain the "why" behind decisions
- Include background in ONBOARDING

### 8. Poor Discoverability

**Problem**: Users can't find documentation

**Solutions**:
- Clear README with links to all docs
- Consistent naming conventions
- Table of contents in long docs
- Cross-references between related docs

## Measuring Documentation Quality

### Quantitative Metrics

- **Onboarding time**: How long for new dev to be productive
- **Support questions**: Frequency of documentation-related questions
- **Link health**: Percentage of working links
- **Coverage**: Percentage of code/features documented
- **Freshness**: Average age of documentation updates

### Qualitative Metrics

- **Clarity**: Can readers understand it?
- **Completeness**: Does it answer all questions?
- **Accuracy**: Is it correct and current?
- **Usefulness**: Does it help achieve goals?
- **Accessibility**: Can target audience find and use it?

### Feedback Mechanisms

- Ask new team members about ONBOARDING
- Track documentation-related support tickets
- Include docs feedback in retrospectives
- Add "Was this helpful?" to docs
- Review documentation in 1:1s

## Documentation Culture

### Making Docs Part of Development

- Include documentation in Definition of Done
- Discuss docs in sprint planning
- Allocate time for documentation
- Celebrate good documentation
- Make it easy to contribute

### Encouraging Contributions

- Lower barrier to contribution
- Provide templates and examples
- Review doc changes constructively
- Recognize documentation contributions
- Make it part of performance reviews

### Leading by Example

- Managers write documentation
- Senior developers maintain docs
- Document as you code
- Share well-documented code in reviews
- Highlight good documentation

## Templates and Standards

### When to Use Templates

Templates ensure consistency and completeness. Use them for:
- New documentation files
- Recurring document types (DEVLOG entries, API endpoints)
- Standardized sections (installation, configuration)

### Customizing Templates

- Adapt templates to project needs
- Remove sections that don't apply
- Add project-specific sections
- Update templates based on feedback

### Enforcing Standards

- Documentation style guide
- Linters for markdown
- Templates in repository
- Review checklist
- Automated checks in CI/CD

## Conclusion

Good documentation is:
- **Accurate**: Reflects current state
- **Complete**: Answers all questions
- **Clear**: Easy to understand
- **Discoverable**: Easy to find
- **Maintainable**: Easy to update
- **Appropriate**: Right detail for audience

Invest in documentation as much as code. Future you (and your team) will thank you.
