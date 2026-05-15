# Deployment Guide

This document describes how to deploy the Rate My Dining Hall application to production.

## Backend Deployment (Render)

### Render Prerequisites

- Render account
- GitHub repository connected to Render

### Render Steps

1. **Create a PostgreSQL Database**

   - Go to Render Dashboard → New → PostgreSQL
   - Name: `rmdh-db`
   - Database: `rmdh`
   - User: Auto-generated
   - Region: Choose closest to your users
   - Plan: Free or Starter
   - Save the Internal Database URL

2. **Create a Web Service**

   - Go to Render Dashboard → New → Web Service
   - Connect your GitHub repository
   - Name: `rmdh-backend`
   - Environment: `Python 3`
   - Region: Same as database
   - Branch: `main` or `develop`
   - Root Directory: `backend`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `alembic upgrade head && python seed.py && uvicorn app.main:app --host 0.0.0.0 --port $PORT`

3. **Set Environment Variables**

   ```env
   DATABASE_URL=<paste-internal-database-url>
   JWT_SECRET=<generate-secure-random-string>
   ALLOWED_EMAIL_DOMAIN=vanderbilt.edu
   PYTHON_VERSION=3.11
   ```

4. **Deploy**

   - Click "Create Web Service"
   - Wait for deployment to complete
   - Note the service URL (e.g., `https://rmdh-backend.onrender.com`)

### Important Notes

- The free tier may have cold starts (services sleep after 15 minutes of inactivity)
- Database URL should use the Internal Database URL for better performance
- Generate a secure JWT_SECRET using: `openssl rand -hex 32`

## Frontend Deployment (Vercel)

### Vercel Prerequisites

- Vercel account
- GitHub repository connected to Vercel

### Vercel Steps

1. **Create a New Project**

   - Go to Vercel Dashboard → Add New → Project
   - Import your GitHub repository
   - Framework Preset: Vite
   - Root Directory: `frontend`

2. **Configure Build Settings**

   - Build Command: `npm run build`
   - Output Directory: `dist`
   - Install Command: `npm install`

3. **Set Environment Variables**

   ```env
   VITE_API_BASE_URL=https://rmdh-backend.onrender.com
   ```

   Replace with your actual backend URL from Render

4. **Deploy**

   - Click "Deploy"
   - Wait for deployment to complete
   - Your app will be available at a URL like: `https://rmdh-frontend.vercel.app`

### Custom Domain (Optional)

- Go to Project Settings → Domains
- Add your custom domain
- Follow DNS configuration instructions

## Post-Deployment

### CORS Configuration

Update the backend's `app/config.py` to include your frontend URL:

```python
BACKEND_CORS_ORIGINS: list[str] = [
    "http://localhost:5173",
    "http://localhost:3000",
    "https://your-app.vercel.app",  # Add your Vercel URL
]
```

### Database Migrations

When updating database models:

1. Create a new migration locally:

   ```bash
   cd backend
   alembic revision --autogenerate -m "description"
   ```

2. Commit and push the migration file

3. Render will automatically run `alembic upgrade head` on deploy

## Monitoring

### Backend (Render)

- Logs: Render Dashboard → Your Service → Logs
- Metrics: Available in Render Dashboard

### Frontend (Vercel)

- Deployments: Vercel Dashboard → Your Project → Deployments
- Analytics: Available in Vercel Dashboard (may require upgrade)

## Troubleshooting

### Backend Issues

- Check logs in Render Dashboard
- Verify DATABASE_URL is correct
- Ensure all environment variables are set
- Check database connection from Render shell

### Frontend Issues

- Verify VITE_API_BASE_URL is correct
- Check browser console for errors
- Ensure CORS is configured correctly on backend
- Test API endpoints directly (use Postman or curl)

### Database Issues

- Check database connection string
- Verify migrations ran successfully
- Check seed script output in logs
- Ensure PostgreSQL version compatibility

## Scaling Considerations

### Backend

- Upgrade to paid Render plan for:
  - No cold starts
  - More resources
  - Better performance
- Consider Redis for caching (future enhancement)
- Add database connection pooling

### Frontend

- Vercel handles scaling automatically
- Consider CDN for static assets
- Optimize bundle size with code splitting

### Database

- Upgrade PostgreSQL plan as needed
- Add read replicas for scaling reads
- Enable backups on paid plans
- Monitor query performance

## Security Checklist

- [ ] Change JWT_SECRET to a secure random value
- [ ] Use HTTPS for all connections
- [ ] Keep dependencies updated
- [ ] Review and restrict CORS origins
- [ ] Enable database backups
- [ ] Monitor error logs regularly
- [ ] Implement rate limiting (future enhancement)
