# Development Guide

This guide will help you set up the Rate My Dining Hall application for local development.

## Prerequisites

- Docker and Docker Compose
- Git

## Quick Start with Docker

1. **Clone the repository**

   ```bash
   git clone <your-repo-url>
   cd rate-my-dining-hall
   ```

2. **Create and configure environment file**

   ```bash
   cp .env.example .env
   ```

   Then generate and set a secret key (required — Docker will refuse to start without it):

   ```bash
   openssl rand -hex 32  # copy the output into JWT_SECRET in .env
   ```

3. **Start all services**

   ```bash
   docker-compose up
   ```

   This will start:

   - PostgreSQL database on port 5432
   - Backend API on <http://localhost:8000>
   - Frontend on <http://localhost:5173>

4. **Access the application**

   - Frontend: <http://localhost:5173>
   - Backend API docs: <http://localhost:8000/docs>
   - Backend health check: <http://localhost:8000/ping>

## Manual Setup (Without Docker)

### Backend Setup

1. **Create a virtual environment**

   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set up PostgreSQL**

   - Install PostgreSQL locally
   - Create a database: `createdb rmdh`
   - Update DATABASE_URL in .env

4. **Run migrations**

   ```bash
   alembic upgrade head
   ```

5. **Seed the database**

   ```bash
   python seed.py
   ```

6. **Start the backend**

   ```bash
   uvicorn app.main:app --reload
   ```

### Frontend Setup

1. **Install Node.js** (version 20 or higher)

2. **Install dependencies**

   ```bash
   cd frontend
   npm install
   ```

3. **Start the development server**

   ```bash
   npm run dev
   ```

   The frontend will be available at <http://localhost:5173>

## Running Tests

### Backend Tests

> **Note:** Backend tests use an in-memory SQLite database — no PostgreSQL required. However, `JWT_SECRET` must be exported in your shell before running tests: `export JWT_SECRET=any-test-value`

```bash
cd backend
pytest -v
```

Run with coverage:

```bash
pytest --cov=app --cov-report=html
```

### Frontend Tests

Frontend tests are not yet implemented.

## Database Migrations

### Create a new migration

```bash
cd backend
alembic revision --autogenerate -m "Description of changes"
```

### Apply migrations

```bash
alembic upgrade head
```

### Rollback migrations

```bash
alembic downgrade -1  # Go back one migration
alembic downgrade <revision>  # Go to specific revision
```

## Project Structure

```text
rate-my-dining-hall/
├── backend/
│   ├── app/
│   │   ├── models/          # SQLModel database models
│   │   ├── routers/         # API route handlers
│   │   ├── schemas/         # Pydantic request/response schemas
│   │   ├── auth.py          # Authentication utilities
│   │   ├── config.py        # Configuration settings
│   │   ├── database.py      # Database connection
│   │   └── main.py          # FastAPI application
│   ├── alembic/             # Database migrations
│   ├── tests/               # Pytest tests
│   ├── requirements.txt     # Python dependencies
│   └── seed.py              # Database seed script
├── frontend/
│   ├── src/
│   │   ├── api/             # API client functions
│   │   ├── components/      # React components
│   │   ├── contexts/        # React contexts
│   │   ├── pages/           # Page components
│   │   ├── types/           # TypeScript types
│   │   ├── App.tsx          # Main app component
│   │   └── main.tsx         # Entry point
│   ├── package.json         # Node dependencies
│   └── vite.config.ts       # Vite configuration
├── docker-compose.yml       # Docker Compose configuration
├── .env.example             # Environment variables template
└── README.md                # Project overview
```

## API Documentation

When the backend is running, visit <http://localhost:8000/docs> for interactive API documentation (Swagger UI).

Key endpoints:

### Authentication

- `POST /api/auth/register` - Register a new user
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user (requires auth)

### Schools & Dining Halls

- `GET /api/schools` - List all schools
- `GET /api/dining-halls` - List dining halls
- `GET /api/dining-halls/{id}` - Get a dining hall with average rating

### Reviews

- `POST /api/reviews` - Create a review (requires auth)
- `GET /api/reviews?dining_hall_id={id}` - Get reviews for a dining hall
- `GET /api/reviews/{id}` - Get a single review
- `DELETE /api/reviews/{id}` - Delete a review (requires auth, owner only)

### Votes

- `POST /api/votes` - Vote on a review (requires auth)
- `GET /api/reviews/{id}/votes` - Get vote counts for a review

## Environment Variables

### Backend (.env)

```env
DATABASE_URL=postgresql://rmdh_user:rmdh_password@db:5432/rmdh
JWT_SECRET=<generate with: openssl rand -hex 32>
ALLOWED_EMAIL_DOMAIN=vanderbilt.edu
```

### Frontend (.env)

```env
VITE_API_BASE_URL=http://localhost:8000
```

## Common Issues

### Port already in use

If you get a "port already in use" error:

```bash
# Find and kill the process using the port
lsof -ti:8000 | xargs kill  # Backend
lsof -ti:5173 | xargs kill  # Frontend
lsof -ti:5432 | xargs kill  # PostgreSQL
```

### Database connection error

- Ensure PostgreSQL is running
- Check DATABASE_URL is correct
- Verify database exists: `psql -l`

### Docker issues

- Restart Docker: `docker-compose down && docker-compose up`
- Rebuild containers: `docker-compose up --build`
- Clear volumes: `docker-compose down -v`

### Node modules issues

```bash
cd frontend
rm -rf node_modules package-lock.json
npm install
```

## Code Style

### Backend (Python)

- Follow PEP 8
- Use type hints
- Document functions with docstrings
- Keep functions focused and small

### Frontend (TypeScript)

- Use TypeScript strict mode
- Define interfaces for all data types
- Use functional components with hooks
- Follow React best practices

## Git Workflow

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push to GitHub: `git push origin feature/your-feature`
4. Create a Pull Request
5. Wait for CI checks to pass
6. Merge to develop/main

## Adding New Features

### Adding a new model

1. Create model in `backend/app/models/`
2. Import in `backend/app/models/__init__.py`
3. Create migration: `alembic revision --autogenerate -m "Add new model"`
4. Apply migration: `alembic upgrade head`

### Adding a new API endpoint

1. Create router in `backend/app/routers/`
2. Include router in `backend/app/main.py`
3. Add tests in `backend/tests/`
4. Document in API docs

### Adding a new page

1. Create page component in `frontend/src/pages/`
2. Add route in `frontend/src/App.tsx`
3. Add navigation if needed
4. Create API functions in `frontend/src/api/`

## Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [SQLModel Documentation](https://sqlmodel.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [TanStack Query Documentation](https://tanstack.com/query/latest)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
