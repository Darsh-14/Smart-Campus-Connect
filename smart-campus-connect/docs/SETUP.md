# Smart Campus Connect - Setup Guide

## Quick Start

### 1. Clone the Repository
```bash
git clone <repository-url>
cd smart-campus-connect
```

### 2. Set Up Supabase Database

1. Create a new project at [supabase.com](https://supabase.com)
2. Navigate to SQL Editor
3. Run the schema from `docs/database/schema.sql`
4. Get your project credentials:
   - Project URL
   - Anon/Public Key
   - Service Role Key

### 3. Configure Environment Variables

**Backend** (`src/backend/.env`):
```env
SUPABASE_URL=https://xxxxx.supabase.co
SUPABASE_KEY=your_anon_key_here
SUPABASE_SERVICE_KEY=your_service_role_key_here
JWT_SECRET_KEY=your_random_secret_key_here
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Generate a secure JWT secret:
```powershell
python -c "import secrets; print(secrets.token_urlsafe(32))"
```

**Frontend** (`src/frontend/.env`):
```env
VITE_API_URL=http://localhost:8000
```

### 4. Option A: Run with Docker (Recommended)

```powershell
# Build and start all services
docker-compose up --build

# Access the application:
# Frontend: http://localhost:3000
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### 4. Option B: Run Locally

**Terminal 1 - Backend**:
```powershell
cd src/backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Terminal 2 - Frontend**:
```powershell
cd src/frontend
npm install
npm run dev
```

## First Steps

### Create Admin Account
1. Navigate to http://localhost:3000
2. Click "Sign Up"
3. Fill in details:
   - Name: Admin User
   - Email: admin@college.edu
   - Password: (your password)
   - Role: Admin
4. Click "Sign Up"

### Create Test Users
Repeat signup for other roles:
- **Teacher**: teacher@college.edu
- **Class Teacher**: classteacher@college.edu
- **Student**: student@college.edu

## Testing the Application

### As Admin
1. Login with admin credentials
2. Navigate to Resources tab
3. Add sample PDFs and video links
4. Test resource management (create, edit, delete)

### As Teacher
1. Login with teacher credentials
2. Create a new assignment:
   - Title: "Python Basics Assignment"
   - Description: "Complete exercises 1-10"
   - Due Date: (2 days from now)
   - Meeting Link: https://meet.google.com/xxx
3. Record student attendance
4. Record student marks

### As Student
1. Login with student credentials
2. View assignments (should see teacher's assignment)
3. View resources shared by admin
4. Check personal attendance and marks

## Development Workflow

### Backend Development
1. Make changes to Python files
2. Server auto-reloads with `--reload` flag
3. Test API endpoints at http://localhost:8000/docs
4. Check logs in terminal

### Frontend Development
1. Make changes to React components
2. Vite hot-reloads automatically
3. Check browser console for errors
4. Use React DevTools for debugging

### Adding New Features

**New Backend Endpoint**:
1. Create route function in appropriate router file
2. Add Pydantic models if needed
3. Implement business logic
4. Test using FastAPI docs

**New Frontend Component**:
1. Create component file in `src/components/`
2. Import and use in appropriate page
3. Style with Tailwind CSS classes
4. Test in browser

## Troubleshooting

### Backend Issues

**"Module not found" error**:
```powershell
pip install -r requirements.txt
```

**Database connection error**:
- Verify Supabase credentials in `.env`
- Check internet connection
- Ensure Supabase project is active

**Port 8000 already in use**:
```powershell
# Find and kill process on Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F
```

### Frontend Issues

**"Cannot find module" error**:
```powershell
rm -rf node_modules
npm install
```

**API calls failing (CORS)**:
- Verify backend is running
- Check VITE_API_URL in `.env`
- Ensure CORS is configured in backend

**Port 3000 already in use**:
```powershell
# Change port in vite.config.js
server: {
  port: 3001  # or any available port
}
```

### Docker Issues

**Containers not starting**:
```powershell
# Check logs
docker-compose logs

# Rebuild from scratch
docker-compose down -v
docker-compose up --build
```

**Database connection in Docker**:
- Ensure `.env` file exists in `src/backend/`
- Check environment variables in `docker-compose.yml`

## Database Management

### View Data
1. Login to Supabase Dashboard
2. Navigate to Table Editor
3. Select table to view/edit data

### Backup Database
```sql
-- In Supabase SQL Editor, export tables:
SELECT * FROM users;
SELECT * FROM resources;
SELECT * FROM assignments;
-- etc.
```

### Reset Database
Run the schema file again from SQL Editor (will drop and recreate tables).

## Production Deployment

### Backend (FastAPI)
- Deploy to: Heroku, Railway, Render, or AWS
- Set environment variables
- Use production ASGI server: `gunicorn -w 4 -k uvicorn.workers.UvicornWorker app.main:app`

### Frontend (React)
- Build: `npm run build`
- Deploy static files to: Vercel, Netlify, or CloudFlare Pages
- Update `VITE_API_URL` to production backend URL

### Database
- Supabase handles scaling automatically
- Set up RLS policies for production security
- Enable connection pooling if needed

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Supabase Documentation](https://supabase.com/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
