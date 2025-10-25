# Documentation Templates

This file contains comprehensive templates for all project documentation files maintained by this skill.

## CLAUDE.md Template

**Location**: Project root

```markdown
# Project Name

> Brief, compelling description of what this project does

**Version**: vX.Y.Z
**Tech Stack**: [Primary technologies used]

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
- Main entry: `src/main.ext`
- Documentation: `docs/`

See [docs/CODE-INDEX.md](docs/CODE-INDEX.md) for complete code structure.

## Quick Reference

### Architecture

[2-3 sentence summary of the system architecture and key design patterns]

See [docs/ONBOARDING.md](docs/ONBOARDING.md) for detailed architecture documentation.

### Key Concepts

- **Concept 1**: Brief explanation of important domain concept
- **Concept 2**: Brief explanation of another key concept
- **Concept 3**: Brief explanation of architectural pattern

### Common Tasks

- Run development server: `command here`
- Run tests: `command here`
- Build for production: `command here`
- Deploy: `command here`

See [README.md](README.md) for detailed setup and usage instructions.

## Current Focus

**Active Development**: [Brief description of current work]

See [docs/PROGRESS.md](docs/PROGRESS.md) for detailed status and upcoming work.
```

## docs/DEVLOG.md Template

**Location**: `docs/DEVLOG.md`

```markdown
# Development Log

> Version-based record of development decisions, changes, and progress.

## [vX.Y.Z] - Feature/Change Title

### Context
Why this change was needed or what problem it solves.

### Changes Made
- Specific changes implemented
- Files modified
- New dependencies or tools added

### Technical Decisions
Key architectural or implementation decisions with rationale.

### Impact
- Areas of the codebase affected
- Breaking changes (if any)
- Migration notes (if applicable)

### References
- Related issues/tickets
- PR links
- Documentation links

---

## Archive

Older entries moved here to keep main log focused on recent work.
```

## README.md Template

**Location**: Project root

```markdown
# Project Name

> Brief, compelling description of what the project does

## Overview

1-2 paragraphs explaining:
- What the project does
- Why it exists
- Who it's for

## Features

- Feature 1: Brief description
- Feature 2: Brief description
- Feature 3: Brief description

## Quick Start

### Prerequisites

- Requirement 1 (version)
- Requirement 2 (version)
- Requirement 3 (version)

### Installation

\`\`\`bash
# Step 1
command here

# Step 2
command here
\`\`\`

### Basic Usage

\`\`\`language
# Simple example showing core functionality
code example
\`\`\`

## Project Structure

\`\`\`
project-root/
├── src/           # Source code
├── tests/         # Test files
├── docs/          # Documentation
└── config/        # Configuration files
\`\`\`

## Configuration

How to configure the project (environment variables, config files, etc.)

## Documentation

- [Onboarding Guide](docs/ONBOARDING.md) - For new developers
- [Development Log](docs/DEVLOG.md) - Historical record
- [Code Index](docs/CODE-INDEX.md) - Source code overview
- [Project Progress](docs/PROGRESS.md) - Current status
- [API Documentation](docs/API.md) - API reference

## Contributing

Guidelines for contributing (if applicable)

## License

License information

## Support

How to get help or report issues
```

## docs/ONBOARDING.md Template

**Location**: `docs/ONBOARDING.md`

```markdown
# Developer Onboarding Guide

> Everything a new developer needs to get started and understand the codebase.

## Welcome

Brief introduction to the project and team culture.

## Table of Contents

- [Architecture Overview](#architecture-overview)
- [Development Environment](#development-environment)
- [Codebase Structure](#codebase-structure)
- [Key Concepts](#key-concepts)
- [Development Workflow](#development-workflow)
- [Testing](#testing)
- [Deployment](#deployment)
- [Resources](#resources)

## Architecture Overview

### High-Level Architecture

\`\`\`
[Diagram or description of system architecture]

Component A ← → Component B
     ↓              ↓
Component C    Component D
\`\`\`

### Technology Stack

- **Frontend**: Technologies used
- **Backend**: Technologies used
- **Database**: Technologies used
- **Infrastructure**: Technologies used
- **Tools**: Development tools

### Design Patterns

Key architectural patterns and principles used:
- Pattern 1: Where and why it's used
- Pattern 2: Where and why it's used

## Development Environment

### Initial Setup

\`\`\`bash
# Clone repository
git clone [repository-url]

# Install dependencies
[installation commands]

# Configure environment
[configuration steps]
\`\`\`

### Environment Variables

| Variable | Description | Example |
|----------|-------------|---------|
| VAR_NAME | What it does | example_value |

### Running Locally

\`\`\`bash
# Development server
[command]

# With specific configuration
[command]
\`\`\`

## Codebase Structure

### Directory Organization

See [CODE-INDEX.md](CODE-INDEX.md) for comprehensive code mapping.

\`\`\`
src/
├── core/          # Core business logic
├── api/           # API endpoints
├── models/        # Data models
├── services/      # Business services
├── utils/         # Utility functions
└── config/        # Configuration
\`\`\`

### Module Responsibilities

- **Module A**: Handles X functionality
- **Module B**: Manages Y operations
- **Module C**: Implements Z features

## Key Concepts

### Concept 1: [Name]

Explanation of important domain concept or architectural decision.

### Concept 2: [Name]

Explanation of another key concept.

### Data Flow

How data moves through the system:
1. Step 1
2. Step 2
3. Step 3

## Development Workflow

### Branch Strategy

- `main` - Production-ready code
- `develop` - Integration branch
- `feature/*` - Feature branches
- `bugfix/*` - Bug fix branches

### Making Changes

1. Create feature branch from `develop`
2. Implement changes with tests
3. Run test suite locally
4. Create pull request
5. Code review
6. Merge after approval

### Code Standards

- Coding style guidelines
- Naming conventions
- Documentation requirements
- Review checklist

## Testing

### Running Tests

\`\`\`bash
# All tests
[command]

# Unit tests
[command]

# Integration tests
[command]
\`\`\`

### Writing Tests

Guidelines and examples for writing tests.

### Test Coverage

Expected coverage levels and how to check.

## Deployment

### Environments

- **Development**: Purpose and access
- **Staging**: Purpose and access
- **Production**: Purpose and access

### Deployment Process

Steps for deploying to each environment.

### Rollback Procedure

How to rollback a deployment if needed.

## Resources

### Documentation

- Internal wiki links
- API documentation
- Design documents

### Communication

- Team chat channels
- Meeting schedules
- Who to contact for what

### Helpful Commands

\`\`\`bash
# Frequently used commands
command1
command2
command3
\`\`\`

## Getting Help

- Ask in #team-channel
- Review [DEVLOG.md](DEVLOG.md) for recent changes
- Check [CODE-INDEX.md](CODE-INDEX.md) for code location
- Contact: [team lead/mentor]
```

## docs/CODE-INDEX.md Template

**Location**: `docs/CODE-INDEX.md`

```markdown
# Code Index

> Comprehensive mapping of the source code structure, classes, methods, and models.

**Last Updated**: vX.Y.Z

## Table of Contents

- [Directory Structure](#directory-structure)
- [Core Modules](#core-modules)
- [Models & Data Structures](#models--data-structures)
- [API Endpoints](#api-endpoints)
- [Services](#services)
- [Utilities](#utilities)
- [Key Dependencies](#key-dependencies)

## Directory Structure

\`\`\`
project-root/
├── src/
│   ├── core/
│   │   ├── module1/
│   │   │   ├── file1.ext      # Purpose
│   │   │   └── file2.ext      # Purpose
│   │   └── module2/
│   ├── api/
│   │   ├── routes/
│   │   └── controllers/
│   ├── models/
│   ├── services/
│   └── utils/
├── tests/
│   ├── unit/
│   └── integration/
└── config/
\`\`\`

## Core Modules

### Module 1: [Name]

**Location**: `src/core/module1/`

**Purpose**: Brief description of what this module does

#### Key Classes/Functions

##### ClassName / functionName

**File**: `src/core/module1/file1.ext:line`

**Purpose**: What this class/function does

**Methods/Functions**:
- `methodName(params)`: Description
  - Parameters: param descriptions
  - Returns: return value description
  - Usage: when/how to use

**Dependencies**:
- Depends on: other modules/classes

**Used By**:
- Referenced by: other modules/classes

### Module 2: [Name]

[Same structure as Module 1]

## Models & Data Structures

### ModelName

**File**: `src/models/model_name.ext:line`

**Description**: What this model represents

**Structure**:
\`\`\`language
{
  field1: type,      // Description
  field2: type,      // Description
  field3: {          // Nested structure
    subfield1: type,
    subfield2: type
  },
  relationships: [   // Relations to other models
    // RelatedModel references
  ]
}
\`\`\`

**Validation Rules**:
- field1: validation requirements
- field2: validation requirements

**Database Mapping** (if applicable):
- Table name: `table_name`
- Indexes: field list
- Constraints: constraint descriptions

**Methods**:
- `methodName()`: Description

## API Endpoints

### Endpoint Group: [Name]

#### GET /api/endpoint

**File**: `src/api/routes/route_file.ext:line`

**Purpose**: What this endpoint does

**Controller**: `ControllerName.methodName` in `src/api/controllers/controller.ext:line`

**Parameters**:
- `param1`: Description (type, required/optional)
- `param2`: Description (type, required/optional)

**Request Body** (if applicable):
\`\`\`json
{
  "field1": "value",
  "field2": "value"
}
\`\`\`

**Response**:
\`\`\`json
{
  "status": "success",
  "data": {}
}
\`\`\`

**Authentication**: Required/Optional

**Related Services**: ServiceName in `src/services/service.ext:line`

#### POST /api/endpoint

[Same structure]

## Services

### ServiceName

**File**: `src/services/service_name.ext:line`

**Purpose**: What this service handles

**Public Methods**:

##### methodName(parameters)

**Purpose**: What this method does

**Parameters**:
- `param1` (type): Description
- `param2` (type): Description

**Returns**: Return value description

**Throws**: Exception types and when

**Dependencies**:
- Uses: Other services/models

**Called By**:
- API endpoints
- Other services

**Key Logic**:
1. Step 1 of logic
2. Step 2 of logic
3. Step 3 of logic

## Utilities

### Utility Module: [Name]

**File**: `src/utils/util_name.ext`

**Purpose**: What utilities this module provides

**Functions**:

##### functionName(parameters)

**Purpose**: What this function does

**Parameters**: parameter descriptions

**Returns**: return value

**Usage Example**:
\`\`\`language
// Example code
\`\`\`

## Key Dependencies

### External Libraries

- **Library Name** (version): Purpose in project
  - Used in: file locations
  - Key functions used: list

### Internal Dependencies

Dependency graph of how modules relate:

\`\`\`
Module A → Module B → Module D
   ↓           ↓
Module C ←─────┘
\`\`\`

## Entry Points

### Main Application Entry

**File**: `src/main.ext:line`

**Initialization Flow**:
1. Load configuration
2. Initialize services
3. Setup routes
4. Start server

### CLI Entry Points

- **Command**: `command_name`
  - File: `src/cli/command.ext:line`
  - Purpose: What the command does

## Configuration

### Configuration Files

- `config/app.config`: Application settings
- `config/db.config`: Database settings

### Environment-Specific Code

Code that behaves differently per environment:
- File: location
- Condition: when it activates

## Testing Utilities

### Test Helpers

- **Helper Name**: `tests/helpers/helper.ext:line`
  - Purpose: What test helper provides
  - Usage: How to use in tests

### Mocks/Fixtures

- **Mock Name**: `tests/mocks/mock.ext:line`
  - Mocks: What it mocks
  - Usage: When to use
```

## docs/PROGRESS.md Template

**Location**: `docs/PROGRESS.md`

```markdown
# Project Progress

> Current status, completed work, and next steps.

**Last Updated**: vX.Y.Z
**Overall Status**: 🟢 On Track | 🟡 At Risk | 🔴 Blocked

## Quick Summary

One paragraph overview of current project state and recent accomplishments.

## Current Sprint/Phase

**Phase**: [Phase Name]
**Timeline**: vX.Y.Z - vX.Y.Z
**Goals**: Key objectives for this phase

### In Progress

- [ ] **Task 1** (Owner: Name)
  - Status: Description of current state
  - Blockers: Any blockers
  - ETA: Expected completion

- [ ] **Task 2** (Owner: Name)
  - Status: Description of current state
  - Blockers: Any blockers
  - ETA: Expected completion

### Recently Completed

- [x] **Task** (Completed: vX.Y.Z)
  - Outcome: What was delivered
  - Impact: What this enables

## Upcoming Work

### Next Sprint/Phase

**Planned Start**: vX.Y.Z

Priority items for next phase:

- **High Priority**
  - Item 1: Description
  - Item 2: Description

- **Medium Priority**
  - Item 1: Description
  - Item 2: Description

- **Low Priority / Nice-to-Have**
  - Item 1: Description
  - Item 2: Description

## Milestones

### Completed Milestones

- ✅ **Milestone 1** (vX.Y.Z)
  - Key deliverables
  - Impact

### Upcoming Milestones

- ⏳ **Milestone 2** (Target: vX.Y.Z)
  - Deliverables needed
  - Current progress: X%

- ⏳ **Milestone 3** (Target: vX.Y.Z)
  - Deliverables needed
  - Current progress: X%

## Metrics

### Development Velocity

- Stories/tasks completed this period: X
- Average completion time: X days
- Burn-down rate: X% of planned work

### Code Health

- Test coverage: X%
- Open issues: X
- Technical debt items: X

### Release Status

- Current version: vX.Y.Z
- Next release: vX.Y.Z (planned Date)
- Release candidate: Status

## Blockers & Risks

### Active Blockers

- **Blocker 1**: Description
  - Impact: How it affects progress
  - Mitigation: What's being done
  - Owner: Who's resolving

### Risks

- **Risk 1**: Description (Probability: High/Med/Low)
  - Impact if realized
  - Mitigation strategy

## Dependencies

### Waiting On

- External team/service: What we need
- Timeline: When expected

### Blocking Others

- Who we're blocking: What they need from us
- Timeline: When we'll deliver

## Team Capacity

- Available developers: X
- Upcoming time off: List
- Adjusted velocity: X

## Recent Decisions

Key decisions that affect progress:

- **Decision 1** (vX.Y.Z): What was decided and why
- **Decision 2** (vX.Y.Z): What was decided and why

## Notes

Additional context, observations, or concerns about project progress.

---

## Historical Progress

### [Phase Name] (vX.Y.Z - vX.Y.Z)

Summary of what was accomplished in previous phase.
```

## docs/API.md Template

**Location**: `docs/API.md`

```markdown
# API Documentation

> Comprehensive API reference and usage guide.

**Version**: X.Y.Z
**Base URL**: `https://api.example.com/v1`
**Last Updated**: vX.Y.Z

## Table of Contents

- [Overview](#overview)
- [Authentication](#authentication)
- [Rate Limiting](#rate-limiting)
- [Error Handling](#error-handling)
- [Endpoints](#endpoints)
- [Data Models](#data-models)
- [Examples](#examples)

## Overview

Brief description of what the API provides and its purpose.

### API Conventions

- Date format: ISO 8601 (YYYY-MM-DDTHH:mm:ssZ)
- All requests/responses use JSON
- All endpoints require authentication unless noted
- All timestamps are in UTC

### Supported Operations

- List of main capabilities

## Authentication

### Authentication Method

Description of authentication approach (API keys, OAuth, JWT, etc.)

**Header Format**:
\`\`\`
Authorization: Bearer YOUR_API_KEY
\`\`\`

**Obtaining Credentials**:
1. Step 1
2. Step 2

**Security Best Practices**:
- Never commit API keys
- Rotate keys regularly
- Use environment variables

## Rate Limiting

- Rate limit: X requests per minute
- Rate limit header: `X-RateLimit-Remaining`
- Reset time header: `X-RateLimit-Reset`

**Rate Limit Response** (429):
\`\`\`json
{
  "error": "Rate limit exceeded",
  "retry_after": 60
}
\`\`\`

## Error Handling

### Standard Error Response

\`\`\`json
{
  "error": {
    "code": "ERROR_CODE",
    "message": "Human-readable message",
    "details": {}
  }
}
\`\`\`

### Error Codes

| Code | Status | Description |
|------|--------|-------------|
| UNAUTHORIZED | 401 | Invalid or missing authentication |
| FORBIDDEN | 403 | Insufficient permissions |
| NOT_FOUND | 404 | Resource not found |
| VALIDATION_ERROR | 422 | Invalid request data |
| RATE_LIMIT | 429 | Too many requests |
| SERVER_ERROR | 500 | Internal server error |

## Endpoints

### Resource: [Resource Name]

#### List Resources

**Endpoint**: `GET /resources`

**Description**: Retrieve a list of resources

**Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| page | integer | No | Page number (default: 1) |
| limit | integer | No | Items per page (default: 20, max: 100) |
| filter | string | No | Filter criteria |

**Request Example**:
\`\`\`bash
curl -X GET "https://api.example.com/v1/resources?page=1&limit=20" \
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

**Response Example** (200 OK):
\`\`\`json
{
  "data": [
    {
      "id": "123",
      "name": "Resource 1",
      "created_at": "2024-01-01T00:00:00Z"
    }
  ],
  "pagination": {
    "page": 1,
    "limit": 20,
    "total": 100,
    "total_pages": 5
  }
}
\`\`\`

#### Get Resource

**Endpoint**: `GET /resources/{id}`

**Description**: Retrieve a specific resource by ID

**Path Parameters**:

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| id | string | Yes | Resource ID |

**Request Example**:
\`\`\`bash
curl -X GET "https://api.example.com/v1/resources/123" \
  -H "Authorization: Bearer YOUR_API_KEY"
\`\`\`

**Response Example** (200 OK):
\`\`\`json
{
  "id": "123",
  "name": "Resource 1",
  "description": "Description",
  "created_at": "2024-01-01T00:00:00Z",
  "updated_at": "2024-01-01T00:00:00Z"
}
\`\`\`

#### Create Resource

**Endpoint**: `POST /resources`

**Description**: Create a new resource

**Request Body**:
\`\`\`json
{
  "name": "New Resource",
  "description": "Description",
  "properties": {}
}
\`\`\`

**Request Example**:
\`\`\`bash
curl -X POST "https://api.example.com/v1/resources" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"name":"New Resource","description":"Description"}'
\`\`\`

**Response Example** (201 Created):
\`\`\`json
{
  "id": "124",
  "name": "New Resource",
  "description": "Description",
  "created_at": "2024-01-01T00:00:00Z"
}
\`\`\`

#### Update Resource

**Endpoint**: `PUT /resources/{id}` or `PATCH /resources/{id}`

**Description**: Update an existing resource (PUT = full update, PATCH = partial update)

**Request Body**:
\`\`\`json
{
  "name": "Updated Name",
  "description": "Updated description"
}
\`\`\`

**Response Example** (200 OK):
\`\`\`json
{
  "id": "123",
  "name": "Updated Name",
  "description": "Updated description",
  "updated_at": "2024-01-02T00:00:00Z"
}
\`\`\`

#### Delete Resource

**Endpoint**: `DELETE /resources/{id}`

**Description**: Delete a resource

**Response Example** (204 No Content)

### Resource: [Another Resource]

[Same structure as above]

## Data Models

### ResourceModel

\`\`\`json
{
  "id": "string",           // Unique identifier
  "name": "string",         // Resource name (required, max 255 chars)
  "description": "string",  // Description (optional, max 1000 chars)
  "status": "string",       // Status: "active" | "inactive" | "pending"
  "properties": {           // Custom properties (object)
    "key": "value"
  },
  "created_at": "string",   // ISO 8601 timestamp
  "updated_at": "string"    // ISO 8601 timestamp
}
\`\`\`

**Validation Rules**:
- `name`: Required, 1-255 characters
- `description`: Optional, max 1000 characters
- `status`: Must be one of: active, inactive, pending

## Examples

### Complete Workflow Example

\`\`\`python
import requests

# Configuration
API_KEY = "your_api_key"
BASE_URL = "https://api.example.com/v1"
headers = {"Authorization": f"Bearer {API_KEY}"}

# 1. Create a resource
response = requests.post(
    f"{BASE_URL}/resources",
    headers=headers,
    json={"name": "My Resource", "description": "Description"}
)
resource = response.json()
resource_id = resource["id"]

# 2. Get the resource
response = requests.get(f"{BASE_URL}/resources/{resource_id}", headers=headers)
print(response.json())

# 3. Update the resource
response = requests.patch(
    f"{BASE_URL}/resources/{resource_id}",
    headers=headers,
    json={"name": "Updated Resource"}
)
print(response.json())

# 4. List all resources
response = requests.get(f"{BASE_URL}/resources", headers=headers)
print(response.json())

# 5. Delete the resource
response = requests.delete(f"{BASE_URL}/resources/{resource_id}", headers=headers)
print(response.status_code)  # 204
\`\`\`

## Changelog

### Version X.Y.Z

- Added: New features
- Changed: Modifications
- Deprecated: Deprecated features
- Removed: Removed features
- Fixed: Bug fixes

## Support

- Documentation: URL
- GitHub Issues: URL
- Support Email: email@example.com
```

## Template Usage Guidelines

### When to Create Each File

- **CLAUDE.md** (root): Create at project start for Claude Code integration
- **README.md** (root): Create at project start, update when features/setup changes
- **docs/DEVLOG.md**: Create at project start, update after each significant change
- **docs/ONBOARDING.md**: Create when team grows beyond 1-2 people or codebase becomes complex
- **docs/CODE-INDEX.md**: Create when codebase has >10 files or multiple modules
- **docs/PROGRESS.md**: Create when actively tracking sprint/milestone progress
- **docs/API.md**: Create when building any API or public interface

### Maintenance Triggers

Update documentation when:
- New features are added
- Architecture changes
- Dependencies are updated
- Bug fixes that reveal design issues
- Performance optimizations
- API changes
- Directory structure changes
- Configuration changes

### Cross-References

Maintain consistency across docs:
- **CLAUDE.md** references all docs in Documentation Map
- **README** links to docs/ONBOARDING.md for new developers
- **docs/DEVLOG.md** references specific code locations from docs/CODE-INDEX.md
- **docs/ONBOARDING.md** references docs/CODE-INDEX.md for code navigation
- **docs/PROGRESS.md** links to docs/DEVLOG.md for historical context
- **docs/API.md** references models from docs/CODE-INDEX.md
