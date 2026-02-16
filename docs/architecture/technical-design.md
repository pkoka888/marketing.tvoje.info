# Technical Design: Marketing Automation Platform (MVP)

**Version:** 1.0
**Date:** 2026-02-13
**Status:** Draft

## 1. System Overview

The platform uses a **Hybrid Monorepo** architecture:

- **Frontend**: Astro 5.0 (Static + Islands) for the Marketing Site and a React-based SPA for the Dashboard (`/app`).
- **Backend**: Python FastAPI service for business logic, orchestration, and proxying requests to AI/Automation providers.
- **Database**: Supabase (PostgreSQL) for relational data and Auth.
- **Orchestration**: Make.com triggers via Webhooks.

## 2. Architecture Diagram

```mermaid
graph TD
    User[User] -->|HTTPS| CDN[Vercel CDN]

    subgraph "Frontend (Astro)"
        Marketing[Marketing Site (/)]
        Dashboard[React Dashboard (/app)]
    end

    CDN --> Marketing
    CDN --> Dashboard

    subgraph "Backend (Railway/Vercel)"
        API[FastAPI Service]
        Auth[Supabase Auth Middleware]
    end

    Dashboard -->|REST API| API

    subgraph "Data & Infra"
        DB[(Supabase PostgreSQL)]
        Redis[(Redis Cache)]
    end

    API --> DB
    API --> Redis

    subgraph "External Services"
        Make[Make.com Webhooks]
        Groq[Groq AI API]
        Shoptet[Shoptet API]
    end

    API -->|Webhook| Make
    API -->|JSON| Groq
    API -->|REST| Shoptet
```

## 3. Data Flow

### 3.1. User Authentication

1. User logs in via Supabase Auth (Frontend).
2. JWT is sent to FastAPI backend in `Authorization` header.
3. Backend validates JWT using Supabase secret.

### 3.2. "Run Automation" Flow

1. User clicks "Generate Report" in Dashboard.
2. `POST /api/v1/automations/trigger` is called.
3. Backend verifies quota in `DB.users`.
4. Backend dispatches payload to Make.com Webhook.
5. Make.com processes data and callbacks to `POST /api/v1/webhooks/result`.
6. Backend updates `DB.reports` and notifies Frontend via WebSocket/Polling.

## 4. Database Schema (Supabase)

### `profiles` (extends auth.users)

- `id`: UUID (FK to auth.users)
- `tier`: enum (free, solo, team)
- `credits_remaining`: int
- `shoptet_id`: string (encrypted)

### `projects`

- `id`: UUID
- `user_id`: UUID
- `name`: string
- `type`: enum (eshop, leadgen)

### `automations`

- `id`: UUID
- `project_id`: UUID
- `type`: enum (seo_audit, content_gen, report)
- `status`: enum (queued, processing, completed, failed)
- `result_json`: jsonb
- `created_at`: timestamp

## 5. API Specification (FastAPI)

### Auth

- `GET /health`: System status.

### User

- `GET /api/v1/me`: User profile & credits.
- `PUT /api/v1/me/settings`: Update preferences.

### Projects

- `GET /api/v1/projects`: List all projects.
- `POST /api/v1/projects`: Create new project.

### Automations

- `POST /api/v1/automations/{type}`: Trigger a new flow.
- `GET /api/v1/automations/{id}`: Get status/result.

## 6. Security

- **secrets**: All API keys (Groq, Make, Shoptet) stored in Environment Variables.
- **cors**: Restricted to frontend domain.
- **rate_limit**: Redis-based rate limiting per user tier.
- **pii**: "Safe Mode" middleware scans all AI inputs for regex patterns (Email, Phone, RC) before sending to Groq.

## 7. Development Stack

- **Python**: 3.11+
- **Framework**: FastAPI
- **ORM**: SQLAlchemy (Async) or Supabase-py
- **Linter**: Ruff
- **Type Checking**: Mypy
