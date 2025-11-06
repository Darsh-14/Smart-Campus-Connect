# Smart Campus Connect

🏫 A comprehensive role-based college management platform built with **FastAPI** and **React**.

## 🚀 Features

- **🔐 Role-Based Access Control**: Admin, Class Teacher, Teacher, and Student roles with specific permissions
- **📝 Assignment Management**: Create, manage, and submit assignments with due dates
- **⏰ Automated Reminders**: Students receive notifications 2 days before assignment deadlines
- **📚 Resource Sharing**: Upload and share PDFs and video links
- **📊 Attendance Tracking**: Teachers record and students view attendance
- **🎯 Marks Management**: Record and view student marks by subject
- **🔒 JWT Authentication**: Secure token-based authentication
- **🔗 Google Meet Integration**: Add meeting links to assignments

## 🛠️ Technology Stack

### Backend
- **FastAPI** - Modern Python web framework
- **Supabase** - PostgreSQL database
- **JWT** - Authentication
- **APScheduler** - Background task scheduling

### Frontend
- **React 18** - UI library
- **Vite** - Build tool
- **Tailwind CSS** - Styling
- **Axios** - HTTP client
- **React Router** - Navigation

### DevOps
- **Docker** - Containerization
- **Docker Compose** - Multi-container orchestration

## 📸 Screenshots

### Student Dashboard
View assignments, resources, attendance, and marks in one place.

### Teacher Dashboard
Create assignments, record attendance, and manage student marks.

### Admin Dashboard
Manage resources and configure system-wide settings.

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- Node.js 18+
- Docker & Docker Compose (optional)
- Supabase account

### 1. Clone Repository
```bash
git clone https://github.com/yourusername/smart-campus-connect.git
cd smart-campus-connect
```

### 2. Set Up Database
1. Create a Supabase project at [supabase.com](https://supabase.com)
2. Run the SQL schema from `docs/database/schema.sql`
3. Get your API credentials

### 3. Configure Environment

**Backend** (`src/backend/.env`):
```env
SUPABASE_URL=your_supabase_url
SUPABASE_KEY=your_anon_key
SUPABASE_SERVICE_KEY=your_service_key
JWT_SECRET_KEY=your_secret_key
```

**Frontend** (`src/frontend/.env`):
```env
VITE_API_URL=http://localhost:8000
```

### 4. Run with Docker (Recommended)
```bash
docker-compose up --build
```

Or run locally:

**Backend**:
```bash
cd src/backend
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Mac/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend**:
```bash
cd src/frontend
npm install
npm run dev
```

### 5. Access the Application
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Docs: http://localhost:8000/docs

## 📚 Documentation

- **[Setup Guide](docs/SETUP.md)** - Detailed installation instructions
- **[API Documentation](docs/API.md)** - Complete API reference
- **[WARP.md](WARP.md)** - Development guide for Warp AI
- **[Database Schema](docs/database/schema.sql)** - Database structure

## 💼 User Roles

### 👑 Admin
- Manage resources (PDFs, videos)
- Grant access to class teachers
- System-wide administration

### 👨‍🏫 Class Teacher
- View all student marks and attendance
- Assign teachers to subjects
- Manage class-level activities

### 🎓 Teacher
- Create and manage assignments
- Record student attendance
- Record student marks
- Add Google Meet links

### 👨‍🎓 Student
- View assignments with due dates
- Submit assignments
- Access learning resources
- View personal attendance and marks
- Receive assignment reminders

## 🛤️ Architecture

```
┌─────────────────┐
│  React Frontend  │
│  (Port 3000)    │
└────────┬────────┘
         │
         │ HTTP/REST
         │
┌────────┴────────┐
│  FastAPI Backend │
│  (Port 8000)     │
│  + APScheduler   │
└────────┬────────┘
         │
         │ SQL
         │
┌────────┴────────┐
│ Supabase (PG)   │
└─────────────────┘
```

## 💻 API Endpoints

### Authentication
- `POST /auth/signup` - Register new user
- `POST /auth/login` - Login user

### Admin
- `GET/POST/PUT/DELETE /admin/resources` - Manage resources
- `POST /admin/grant-access` - Grant class teacher access

### Teacher
- `GET/POST/PUT/DELETE /teacher/assignments` - Manage assignments
- `POST /teacher/attendance` - Record attendance
- `POST /teacher/marks` - Record marks

### Student
- `GET /student/assignments` - View assignments
- `GET /student/resources` - View resources
- `GET /student/attendance` - View attendance
- `GET /student/marks` - View marks
- `POST /student/assignments/{id}/submit` - Submit assignment

See [API Documentation](docs/API.md) for complete reference.

## 🧪 Testing

### Backend Tests
API testing via auto-generated docs at `/docs`

### Frontend Tests
```bash
npm run test
```

## 🚀 Deployment

### Backend
- **Recommended**: Railway, Render, Heroku
- Set environment variables
- Use production ASGI server

### Frontend
- **Recommended**: Vercel, Netlify, CloudFlare Pages
- Build: `npm run build`
- Deploy `dist/` folder

### Database
- Supabase handles hosting and scaling
- Configure RLS policies for security

## 🤝 Contributing

Contributions are welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License.

## 📧 Contact

For questions or support, please open an issue or contact the maintainers.

## 🚀 Roadmap

- [ ] Email notifications for assignments
- [ ] Mobile app (React Native)
- [ ] Real-time chat between teachers and students
- [ ] File upload for assignment submissions
- [ ] Analytics dashboard for admins
- [ ] Grade calculation and GPA tracking
- [ ] Calendar integration
- [ ] Push notifications

---

Built with ❤️ for modern education management
