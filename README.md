# Vandy Eats

A full-stack web app where Vanderbilt students review and rate campus dining halls — post 1–5 star reviews, and upvote or downvote what other students say.

## Overview

Students authenticate with their `@vanderbilt.edu` email, browse dining halls (Commons, E. Bronson Ingram, Rand, 2301), post reviews, and vote on each other's feedback. The schema is school-scoped (`School → DiningHall → Review → Vote`), so adding another university is a data change, not a rewrite.

## Features

- Email authentication restricted to `@vanderbilt.edu`, with JWT sessions (7-day expiry)
- 1–5 star reviews with text, and delete-your-own-review support
- Upvoting/downvoting on reviews from other students
- Live average rating per dining hall
- Responsive UI (Tailwind) with loading and error states throughout

## Tech Stack

| Layer    | Tech |
| -------- | ---- |
| Frontend | React, TypeScript, Vite, Tailwind CSS, TanStack Query, React Router |
| Backend  | FastAPI, SQLModel + Pydantic, PostgreSQL, Alembic migrations, JWT (python-jose), passlib |
| DevOps   | Docker Compose, GitHub Actions CI, Render (backend), Vercel (frontend) |

## Database Schema

```text
School (id, name, allowed_domain)
  ↓ 1:N
DiningHall (id, name, school_id)
  ↓ 1:N
Review (id, user_id, dining_hall_id, rating, text, created_at)
  ↓ 1:N
Vote (id, user_id, review_id, value)

User (id, email, hashed_password, school_id, created_at)
  ↓ 1:N Reviews, Votes
```

## Quick Start

### Prerequisites

- Docker + Docker Compose

### Setup

1. **Clone and enter the repo**

   ```bash
   git clone https://github.com/brianntangg/vandy-eats.git
   cd vandy-eats
   ```

2. **Configure environment**

   ```bash
   cp .env.example .env
   openssl rand -hex 32   # paste output into JWT_SECRET in .env (required)
   ```

3. **Start everything**

   ```bash
   docker-compose up
   ```

4. **Open the app**

   - Frontend: <http://localhost:5173>
   - API docs (Swagger): <http://localhost:8000/docs>
   - Health check: <http://localhost:8000/ping>

First startup automatically runs migrations and seeds Vanderbilt's dining halls. For manual (non-Docker) setup, see [DEVELOPMENT.md](DEVELOPMENT.md).

## API

| Method | Endpoint                        | Description |
|--------|---------------------------------|-------------|
| POST   | `/api/auth/register`            | Register with `@vanderbilt.edu` email |
| POST   | `/api/auth/login`               | Login, receive JWT |
| GET    | `/api/auth/me`                  | Current user profile |
| GET    | `/api/schools`                  | List schools |
| GET    | `/api/dining-halls`             | List dining halls (filter by `school_id`) |
| GET    | `/api/dining-halls/{id}`        | Dining hall with average rating |
| GET    | `/api/reviews`                  | List reviews (filter by `dining_hall_id`, paginated) |
| POST   | `/api/reviews`                  | Create review (auth) |
| DELETE | `/api/reviews/{id}`             | Delete your own review (auth) |
| POST   | `/api/votes`                    | Upvote or downvote |
| GET    | `/api/votes/{review_id}/votes`  | Vote summary for a review |

Full interactive docs at `/docs` when running.

## Testing & CI

```bash
cd backend
pytest -v                                    # run tests
pytest --cov=app --cov-report=html           # with coverage
```

GitHub Actions runs the test suite on every push and pull request (`.github/workflows/ci.yml`).

## Roadmap

Image uploads (Cloudinary), Redis caching, review editing, admin panel, multi-school rollout, email verification.

## Project Structure

```text
vandy-eats/
├── backend/              # FastAPI
│   ├── app/
│   │   ├── models/       # SQLModel database models
│   │   ├── routers/      # API endpoints
│   │   └── schemas/      # Pydantic schemas
│   ├── alembic/          # Migrations
│   └── tests/            # Pytest
├── frontend/             # React + TypeScript
│   └── src/              # api/, components/, contexts/, pages/
├── docker-compose.yml
└── .env.example
```

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) — backend on Render, frontend on Vercel, PostgreSQL on Render.
