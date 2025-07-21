# 🍽️ Rate My Dining Hall

**A full-stack web application that allows students to review and rate college dining halls using their `.edu` email, complete with pictures, voting, and multi-campus support.**

## 🧠 Overview

Rate My Dining Hall enables authenticated students to post reviews, upload optional images, and upvote/downvote dining hall experiences across different campuses. Designed to be lightweight and scalable, the app makes it easy to add new schools and their dining locations.

## 🚀 Features

- 🔐 Sign up with `.edu` email authentication
- 🏫 Support for multiple schools and dining halls
- ✍️ Post dining hall reviews with optional photos
- 👍👎 Upvote and downvote reviews
- 📸 Upload images with reviews (Cloudinary or S3)
- 📦 Easy admin-driven or self-service addition of schools and halls

## 🛠 Tech Stack

**Frontend**
- React + TypeScript
- Vite
- Tailwind CSS or Material UI
- TanStack Query

**Backend**
- FastAPI
- SQLAlchemy or SQLModel + Pydantic
- PostgreSQL
- Redis

**DevOps**
- Docker
- GitHub Actions
- Azure WebApps or Render

## 🏗️ Architecture

```text
             ┌────────────────────────────┐
             │     Client (React App)     │
             │  (Vite + TypeScript + UI)  │
             └────────────┬───────────────┘
                          │  REST API
                          ▼
             ┌────────────────────────────┐
             │      FastAPI Backend       │
             │  (Python + Pydantic + ORM) │
             └────────────┬───────────────┘
          ┌───────────────┴───────────────┐
          ▼                               ▼
┌─────────────────┐           ┌────────────────────┐
│   PostgreSQL    │           │       Redis        │
│ (Review Storage)│           │ (Cache, Rate Limit)│
└─────────────────┘           └────────────────────┘
```

## 🧰 Getting Started
Prerequisites
- Docker + Docker Compose
- Node.js ≥ 18.x
- Python ≥ 3.11

Setup
```bash
git clone https://github.com/yourname/rate-my-dining-hall.git
cd rate-my-dining-hall
cp .env.example .env
```

Start App
```
# From root directory
docker-compose up --build
```
- Frontend: http://localhost:5173
- Backend: http://localhost:8000/docs

## 🧩 API Endpoints

### 🔐 Auth & User

| Method | Endpoint             | Description                            |
|--------|----------------------|----------------------------------------|
| POST   | `/api/auth/register` | Register with `.edu` email             |
| POST   | `/api/auth/login`    | Login and receive JWT                  |
| GET    | `/api/users/me`      | Get current user profile               |

### 🏫 Schools & Dining Halls

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| GET    | `/api/schools`            | List all schools                 |
| POST   | `/api/schools`            | Add a new school *(admin)*       |
| GET    | `/api/dining-halls`       | List all dining halls            |
| POST   | `/api/dining-halls`       | Add a new dining hall *(admin)* |

### ✍️ Reviews

| Method | Endpoint                | Description                   |
|--------|-------------------------|-------------------------------|
| GET    | `/api/reviews`          | List all reviews              |
| GET    | `/api/reviews/{id}`     | Get a specific review         |
| POST   | `/api/reviews`          | Create a new review           |
| PATCH  | `/api/reviews/{id}`     | Edit an existing review       |
| DELETE | `/api/reviews/{id}`     | Delete a review               |

### 👍👎 Votes

| Method | Endpoint                      | Description                       |
|--------|-------------------------------|-----------------------------------|
| POST   | `/api/votes`                  | Submit an upvote or downvote      |
| GET    | `/api/reviews/{id}/votes`     | Get vote summary for a review     |

### 📦 Misc

| Method | Endpoint     | Description           |
|--------|--------------|-----------------------|
| GET    | `/ping`      | Health check endpoint |
| GET    | `/docs`      | Swagger/OpenAPI docs  |

## 🔐 Environment Variables
Create a .env file in the root with the following:
```dotenv
# Shared
JWT_SECRET=your-secret
ALLOWED_EMAIL_DOMAIN=.edu

# Backend
DATABASE_URL=postgresql://user:pass@db:5432/rmdh
REDIS_URL=redis://redis:6379/0
CLOUDINARY_URL=cloudinary://...

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## ✅ Testing
Run unit and integration tests:
```bash
# Backend
cd backend
pytest

# Frontend
cd frontend
npm test
```

Linting and formatting:
```bash
# Backend
ruff . && black .

# Frontend
npm run lint && npm run format
```

## 🚀 Deployment
Use GitHub Actions to deploy Docker containers:
- Backend to Azure WebApps or Render
- Frontend to Vercel or Netlify
- Configure CI to run tests and linting on pull requests

