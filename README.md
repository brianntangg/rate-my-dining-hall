# Vandy Eats

**A full-stack web application for Vanderbilt University students to review and rate campus dining halls with upvoting/downvoting functionality.**

## Overview

Vandy Eats is an MVP web application that enables Vanderbilt students to authenticate with their `@vanderbilt.edu` email, browse dining halls, post reviews with 1-5 star ratings, and upvote/downvote other students' reviews. The architecture is designed to be scalable to multiple universities.

## Features

- ✅ Email authentication with `@vanderbilt.edu` domain validation
- ✅ JWT-based authentication with 7-day expiry
- ✅ Browse Vanderbilt dining halls (Commons, E. Bronson Ingram, Rand, 2301)
- ✅ Post 1-5 star reviews with text (minimum 10 characters)
- ✅ Upvote and downvote reviews from other students
- ✅ Delete your own reviews
- ✅ View average ratings for each dining hall
- ✅ Responsive UI with Tailwind CSS
- ✅ Real-time loading and error states

## Planned Features (Post-MVP)

- Image uploads with reviews (Cloudinary)
- Redis caching for performance
- Review editing
- Admin panel for managing dining halls
- Multi-school support
- Email verification

## Tech Stack

### Frontend

- React + TypeScript
- Vite
- Tailwind CSS
- TanStack Query (React Query)
- Axios
- React Router DOM
- React Toastify

### Backend

- FastAPI
- SQLModel + Pydantic
- PostgreSQL
- Alembic (migrations)
- python-jose (JWT)
- passlib (password hashing)

### DevOps

- Docker + Docker Compose
- GitHub Actions (CI)
- Render (backend deployment)
- Vercel (frontend deployment)

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

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd rate-my-dining-hall
   ```

2. **Create and configure environment file**

   ```bash
   cp .env.example .env
   ```

   Then generate and set a secret key (required — the app will not start without it):

   ```bash
   openssl rand -hex 32  # copy the output into JWT_SECRET in .env
   ```

3. **Start all services**

   ```bash
   docker-compose up
   ```

4. **Access the application**

   - Frontend: <http://localhost:5173>
   - Backend API docs: <http://localhost:8000/docs>
   - Health check: <http://localhost:8000/ping>

### First Time Setup

The application will automatically:

- Run database migrations
- Seed Vanderbilt University and dining halls
- Start the backend and frontend servers

For detailed setup instructions, see [DEVELOPMENT.md](DEVELOPMENT.md)

## API Endpoints

### Auth & User

| Method | Endpoint             | Description                            |
|--------|----------------------|----------------------------------------|
| POST   | `/api/auth/register` | Register with `@vanderbilt.edu` email  |
| POST   | `/api/auth/login`    | Login and receive JWT                  |
| GET    | `/api/auth/me`       | Get current user profile               |

### Schools & Dining Halls

| Method | Endpoint                  | Description                      |
|--------|---------------------------|----------------------------------|
| GET    | `/api/schools`            | List all schools                 |
| GET    | `/api/dining-halls`       | List all dining halls (filterable by school_id) |
| GET    | `/api/dining-halls/{id}`  | Get a dining hall with average rating |

### Reviews

| Method | Endpoint                | Description                   |
|--------|-------------------------|-------------------------------|
| GET    | `/api/reviews`          | List reviews (filtered by dining_hall_id, paginated) |
| GET    | `/api/reviews/{id}`     | Get a specific review         |
| POST   | `/api/reviews`          | Create a new review (auth required) |
| DELETE | `/api/reviews/{id}`     | Delete your own review (auth required) |

### Votes

| Method | Endpoint                        | Description                    |
|--------|---------------------------------|--------------------------------|
| POST   | `/api/votes`                    | Submit an upvote or downvote   |
| GET    | `/api/votes/{review_id}/votes`  | Get vote summary for a review  |

### Misc

| Method | Endpoint     | Description           |
|--------|--------------|-----------------------|
| GET    | `/ping`      | Health check endpoint |
| GET    | `/docs`      | Swagger/OpenAPI docs  |

## Environment Variables

See `.env.example` for all available variables. Key variables:

```env
# Backend
DATABASE_URL=postgresql://rmdh_user:rmdh_password@db:5432/rmdh
JWT_SECRET=<generate with: openssl rand -hex 32>
ALLOWED_EMAIL_DOMAIN=vanderbilt.edu
BACKEND_CORS_ORIGINS=http://localhost:5173,http://localhost:3000

# Frontend
VITE_API_BASE_URL=http://localhost:8000
```

## Testing

### Backend Tests

```bash
cd backend
pytest -v
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

### CI/CD

GitHub Actions automatically runs tests on push and pull requests. See `.github/workflows/ci.yml` for configuration.

## Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for detailed deployment instructions to:

- Backend: Render
- Frontend: Vercel
- Database: Render PostgreSQL

## Development

For detailed development instructions, including manual setup without Docker, database migrations, and contribution guidelines, see [DEVELOPMENT.md](DEVELOPMENT.md).

## Project Structure

```text
rate-my-dining-hall/
├── backend/              # FastAPI backend
│   ├── app/
│   │   ├── models/      # SQLModel database models
│   │   ├── routers/     # API endpoints
│   │   ├── schemas/     # Pydantic schemas
│   │   └── ...
│   ├── alembic/         # Database migrations
│   ├── tests/           # Pytest tests
│   └── requirements.txt
├── frontend/            # React frontend
│   ├── src/
│   │   ├── api/        # API client
│   │   ├── components/ # React components
│   │   ├── contexts/   # React contexts
│   │   ├── pages/      # Page components
│   │   └── ...
│   └── package.json
├── docker-compose.yml   # Docker Compose config
└── .env.example         # Environment variables template
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## Support

For issues and questions, please open a GitHub issue.
