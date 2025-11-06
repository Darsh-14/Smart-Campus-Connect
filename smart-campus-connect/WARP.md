# WARP.md

This file provides guidance to WARP (warp.dev) when working with code in this repository.

## Project Overview

Smart Campus Connect is a role-based college management platform built with FastAPI (backend) and React (frontend), using Supabase for data storage. The platform enables:
- Real-time assignment management with automated reminders
- Resource sharing (PDFs and videos)
- Attendance and marks tracking
- Role-based access control (Admin, Class Teacher, Teacher, Student)
- Secure JWT-based authentication

## Technology Stack

- **Backend**: FastAPI, Python 3.11+
- **Frontend**: React 18, Vite, Tailwind CSS
- **Database**: Supabase (PostgreSQL)
- **Authentication**: JWT tokens
- **Scheduler**: APScheduler
- **Containerization**: Docker, Docker Compose

## Repository Structure

```
smart-campus-connect/
├── src/
│   ├── backend/              # FastAPI application
│   │   ├── app/
│   │   │   ├── routers/      # API endpoints (auth, admin, teacher, student)
│   │   │   ├── main.py       # Application entry point
│   │   │   ├── auth.py       # JWT authentication
│   │   │   ├── models.py     # Pydantic models
│   │   │   ├── database.py   # Supabase connection
│   │   │   ├── config.py     # Settings management
│   │   │   └── scheduler.py  # Assignment reminders
│   │   ├── requirements.txt  # Python dependencies
│   │   ├── Dockerfile
│   │   └── .env.example
│   └── frontend/             # React application
│       ├── src/
│       │   ├── pages/        # Dashboard pages for each role
│       │   ├── components/   # Reusable UI components
│       │   ├── context/      # Auth context
│       │   └── utils/        # API utilities
│       ├── package.json
│       ├── Dockerfile
│       └── vite.config.js
├── docs/
│   └── database/
│       └── schema.sql        # Supabase database schema
├── docker-compose.yml        # Multi-container setup
└── README.md
```

## Development Setup

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (for containerized setup)
- Supabase account

### Backend Setup

```powershell
# Navigate to backend directory
cd src/backend

# Create virtual environment
python -m venv venv
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file and configure
cp .env.example .env
# Edit .env with your Supabase credentials

# Run development server
uvicorn app.main:app --reload
```

Backend runs on: http://localhost:8000
API Documentation: http://localhost:8000/docs

### Frontend Setup

```powershell
# Navigate to frontend directory
cd src/frontend

# Install dependencies
npm install

# Copy environment file
cp .env.example .env

# Run development server
npm run dev
```

Frontend runs on: http://localhost:3000

### Database Setup

1. Create a Supabase project at https://supabase.com
2. Run the SQL schema from `docs/database/schema.sql` in Supabase SQL Editor
3. Copy Supabase URL and Keys to backend `.env` file

### Docker Setup

```powershell
# Build and run all services
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop services
docker-compose down
```

## Common Commands

### Backend
```powershell
# Run server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run with logs
uvicorn app.main:app --reload --log-level debug

# Install new dependency
pip install <package>
pip freeze > requirements.txt
```

### Frontend
```powershell
# Development server
npm run dev

# Build for production
npm run build

# Preview production build
npm run preview

# Lint code
npm run lint
```

## Architecture

### Backend Architecture

**API Structure**: RESTful API with role-based routers:
- `/auth/*` - Authentication endpoints (signup, login)
- `/admin/*` - Admin-only endpoints (resource management)
- `/class-teacher/*` - Class teacher endpoints (view marks/attendance)
- `/teacher/*` - Teacher endpoints (assignments, marks, attendance)
- `/student/*` - Student endpoints (view assignments, resources, marks)

**Authentication Flow**:
1. User signs up or logs in with email/password
2. Backend hashes password and stores in Supabase
3. JWT token generated and returned to client
4. Client stores token and includes in Authorization header
5. Protected routes verify token and check role permissions

**Background Scheduler**:
- APScheduler runs daily to check assignments due in 2 days
- Creates notification records in database for pending assignments
- Students receive reminders via notification system

### Frontend Architecture

**State Management**: React Context API for authentication state

**Routing**: React Router with protected routes based on user role

**API Communication**: Axios with interceptors for:
- Automatic token injection in requests
- 401 error handling (auto-logout)

**Role-Based Dashboards**:
- **Admin**: Manage resources (PDFs, videos), grant access to class teachers
- **Class Teacher**: View student marks and attendance, assign teachers to subjects
- **Teacher**: Create/manage assignments, record attendance and marks
- **Student**: View assignments, resources, attendance, marks

### Database Schema

Key tables:
- `users` - User accounts with roles
- `resources` - PDFs and video links
- `assignments` - Teacher-created assignments
- `student_assignments` - Assignment submissions tracking
- `attendance` - Student attendance records
- `marks` - Student marks per subject
- `notifications` - Assignment reminders

See `docs/database/schema.sql` for complete schema.

## Role-Based Access Control

**Roles**:
1. **Admin** - Full platform control
2. **Class Teacher** - Manages class, views all student data
3. **Teacher** - Creates assignments, records marks/attendance
4. **Student** - Views assignments, resources, personal data

**Middleware**: `require_role()` dependency injection validates user role for each endpoint.

## Assignment Reminder System

When a teacher creates an assignment:
1. Assignment stored with due date
2. Daily scheduler job checks for assignments due in 2 days
3. Notification records created for all students with pending submissions
4. Frontend displays notifications in dashboard

## Environment Variables

**Backend (.env)**:
```
SUPABASE_URL=<your-supabase-url>
SUPABASE_KEY=<anon-key>
SUPABASE_SERVICE_KEY=<service-role-key>
JWT_SECRET_KEY=<random-secret-key>
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

**Frontend (.env)**:
```
VITE_API_URL=http://localhost:8000
```

## Testing & Debugging

**API Testing**: Use FastAPI's auto-generated docs at `/docs`

**Frontend Debugging**: React DevTools + browser console

**Backend Logs**: Check terminal output for uvicorn logs

## Common Issues

**CORS errors**: Ensure backend CORS middleware includes frontend URL

**401 Unauthorized**: Check JWT token expiration, verify Supabase credentials

**Database errors**: Verify schema is properly set up in Supabase

**Port conflicts**: Ensure ports 3000 (frontend) and 8000 (backend) are available
