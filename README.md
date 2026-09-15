# FounderLog
A community-driven news platform featuring real project stories, earnings, sources, discussions, and user experiences.

FounderLog is a modular monolith backend built with **FastAPI**, **SQLAlchemy**, and **PostgreSQL**.

The project is intentionally organized by feature/module. It runs as a single application and uses a single database, while keeping functional areas isolated enough that they can be extracted into separate services later if necessary.

---

## Project Structure

```text
FounderLog/
│
├── backend/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── core/
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── config.py
│   │   ├── db.py
│   │   ├── registry.py
│   │   │
│   │   └── services/
│   │       ├── __init__.py
│   │       ├── comments.py
│   │       └── votes.py
│   │
│   └── modules/
│       ├── __init__.py
│       │
│       └── stories/
│           ├── __init__.py
│           ├── models.py
│           ├── repository.py
│           ├── router.py
│           ├── schemas.py
│           └── service.py
│
├── .env
├── .env.example
├── .gitignore
├── README.md
└── requirements.txt
```

---

# Application Architecture

The backend follows a simple layered architecture:

```text
HTTP Request
     │
     ▼
  Router
     │
     ▼
  Service
     │
     ▼
 Repository
     │
     ▼
 PostgreSQL
```

Each feature is kept inside its own module:

```text
backend/modules/<feature>/
```

For example:

```text
backend/modules/stories/
├── models.py
├── repository.py
├── router.py
├── schemas.py
└── service.py
```

This keeps feature-specific code together instead of creating global folders such as:

```text
routers/
models/
services/
repositories/
```

---

# Core

The `backend/core/` directory contains functionality shared by multiple modules.

```text
backend/core/
├── auth.py
├── config.py
├── db.py
├── registry.py
└── services/
    ├── comments.py
    └── votes.py
```

## `config.py`

Contains application configuration and environment variables.

Responsibilities:

- Application name
- Debug mode
- Database URL
- JWT configuration
- Environment loading

---

## `db.py`

Contains the SQLAlchemy database configuration.

Responsibilities:

- SQLAlchemy engine
- Session factory
- Declarative base
- Database dependency for FastAPI

Modules should use the shared database configuration instead of creating their own database connections.

---

## `auth.py`

Contains shared authentication functionality.

Authentication-related dependencies should live here so that individual modules do not need to implement their own authentication logic.

---

## `registry.py`

Contains the list of enabled application modules.

Example:

```python
from backend.modules.stories.router import router as stories_router


MODULES = [
    stories_router,
]
```

`main.py` uses this registry to include the routers.

This also makes it possible to temporarily disable a whole module without deleting its code.

---

## `core/services/`

This directory contains shared service interfaces used by multiple modules.

For example:

```text
comments.py
votes.py
```

A module should preferably interact with another feature through a shared service interface instead of importing another module's internal models or repositories.

Example:

```python
await comments_service.get_thread(
    target_type="story",
    target_id=story_id,
)
```

The caller does not need to know how comments are stored internally.

---

# Feature Modules

All functional areas live inside:

```text
backend/modules/
```

Each module should be as independent as reasonably possible.

Example:

```text
backend/modules/stories/
├── models.py
├── repository.py
├── router.py
├── schemas.py
└── service.py
```

## `router.py`

Contains FastAPI endpoints.

Responsibilities:

- HTTP routes
- Request dependencies
- Authentication dependencies
- Calling the service layer
- Returning response schemas

The router should contain as little business logic as possible.

---

## `schemas.py`

Contains Pydantic schemas.

Responsibilities:

- Request validation
- Response serialization
- API contracts

Example:

```python
class StoryCreate(BaseModel):
    title: str
    content: str
```

---

## `models.py`

Contains SQLAlchemy database models belonging to the module.

Example:

```python
class Story(Base):
    __tablename__ = "stories"
```

Models should normally stay inside their owning module.

Shared entities that are used throughout the application can live in `core`.

---

## `service.py`

Contains business logic.

Example responsibilities:

- Creating a story
- Updating a story
- Validating business rules
- Calling repositories
- Using shared services

The service layer should not depend on HTTP-specific logic.

---

## `repository.py`

Contains database access for the module.

Responsibilities:

- Queries
- Inserts
- Updates
- Deletes
- Database-specific operations

The repository should handle persistence, while the service handles business rules.

---

# Module Dependency Rules

The most important architectural rule is:

> A module should not directly depend on another module's internal implementation.

Avoid:

```python
from backend.modules.comments.models import Comment
```

from inside another feature module.

Prefer:

```python
from backend.core.services.comments import CommentsService
```

This keeps module boundaries clear.

A simplified dependency direction is:

```text
modules
   │
   ▼
core services
   │
   ▼
database
```

Modules should not form a chain of direct dependencies such as:

```text
stories → community → comments → stories
```

because this quickly creates circular dependencies and tightly coupled code.

---

# Database

The project uses a single PostgreSQL database.

All modules use the same database and database schema.

Conceptually:

```text
                 PostgreSQL
                     │
        ┌────────────┼────────────┐
        │            │            │
     stories      users       community
        │
     tags
```

The database is shared, but ownership of tables remains clear.

For example:

```text
stories module
    └── stories table

community module
    └── projects table

core
    └── users table
```

A module owns its own tables and database logic.

---

# Application Entry Point

The application starts from:

```text
backend/main.py
```

The entry point creates the FastAPI application and registers enabled modules.

Conceptually:

```python
from fastapi import FastAPI

from backend.core.config import settings
from backend.core.registry import MODULES


app = FastAPI(
    title=settings.app_name,
    debug=settings.debug,
)

for router in MODULES:
    app.include_router(router)
```

The application therefore remains a single FastAPI process.

---

# Local Development

## Requirements

Install:

- Python 3.11+
- PostgreSQL
- Git

Create a virtual environment:

### Windows

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Configuration

Create a `.env` file in the project root.

Example:

```env
APP_NAME=FounderLog
DEBUG=true

DATABASE_URL=postgresql+asyncpg://postgres:postgres@localhost:5432/founderlog

JWT_SECRET=change-me
JWT_ALGORITHM=HS256
```

Never commit `.env` to Git.

Use `.env.example` as the template for required environment variables.

---

# Database Setup

Make sure PostgreSQL is running.

Create the database:

```text
founderlog
```

The connection string should match the `.env` configuration:

```text
postgresql+asyncpg://postgres:postgres@localhost:5432/founderlog
```

---

# Running the Application

From the project root:

```text
FounderLog/
```

activate the virtual environment and run:

```bash
uvicorn backend.main:app --reload
```

The API will be available at:

```text
http://127.0.0.1:8000
```

Swagger documentation:

```text
http://127.0.0.1:8000/docs
```

ReDoc:

```text
http://127.0.0.1:8000/redoc
```

---

# Adding a New Module

To add a new feature, create a new directory:

```text
backend/modules/<feature>/
```

Example:

```text
backend/modules/community/
├── __init__.py
├── models.py
├── repository.py
├── router.py
├── schemas.py
└── service.py
```

Then register its router in:

```text
backend/core/registry.py
```

Example:

```python
from backend.modules.community.router import router as community_router


MODULES = [
    stories_router,
    community_router,
]
```

No changes should normally be required inside existing modules unless the new feature actually needs to interact with them.

---

# Disabling a Module

A module can be disabled by removing its router from the registry.

For example:

```python
MODULES = [
    stories_router,
]
```

If `community_router` is removed, the Community API is no longer mounted.

The module's code can remain in the repository and be enabled again later.

---

# Testing

Tests should follow the same module structure:

```text
tests/
├── stories/
│   ├── test_router.py
│   ├── test_service.py
│   └── test_repository.py
│
├── community/
│   └── ...
│
└── integration/
    ├── test_comments.py
    └── test_votes.py
```

Unit tests should remain close to the module they test.

Integration tests should be used for shared services and interactions between modules.

---

# Git Workflow

`main` is the stable branch.

Do not develop directly on `main`.

Create a branch for each task:

```bash
git switch main
git pull origin main
git switch -c feature/<feature-name>
```

Work on the feature, then:

```bash
git add .
git commit -m "Add <feature>"
git push -u origin feature/<feature-name>
```

Create a Pull Request:

```text
feature/<feature-name> → main
```

After review, merge the Pull Request into `main`.

---

# Development Rules

1. Keep `main` stable.
2. Do not commit directly to `main`.
3. Create a separate branch for each task.
4. Start new branches from the latest `main`.
5. Do not commit `.env`.
6. Do not commit local database files or Docker volumes.
7. Keep migrations in Git.
8. Keep feature-specific code inside its module.
9. Avoid direct imports from another module's internal implementation.
10. Use shared services for cross-module functionality.
11. Keep routers thin and business logic inside services.
12. Keep database operations inside repositories.

---

# Current Modules

Currently implemented:

```text
stories
```

Planned modules can be added independently, for example:

```text
community
tags
notifications
stats
collections
```

The exact module list should grow with the application instead of being created in advance without implementation.

---

# Long-Term Architecture

The current architecture is a **modular monolith**.

Initially:

```text
                    FounderLog
                        │
                 FastAPI application
                        │
        ┌───────────────┼───────────────┐
        │               │               │
     Stories         Community         Tags
        │               │               │
        └───────────────┼───────────────┘
                        │
                    PostgreSQL
```

If a particular module eventually requires independent scaling or deployment, it can be extracted into a separate service.

The goal is to keep the module boundaries clear enough that this can be done without rewriting the entire application.

