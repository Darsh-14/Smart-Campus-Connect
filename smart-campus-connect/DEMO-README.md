# 🎭 Smart Campus Connect - DEMO MODE

## 🚀 Quick Start

Simply **double-click** `RUN-DEMO.bat` to start both servers!

Or manually:

### Backend (Terminal 1)
```powershell
cd src\backend
python -m uvicorn app.main:app --reload
```

### Frontend (Terminal 2)
```powershell
cd src\frontend
npm run dev
```

## 🌐 Access Points

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000  
- **API Docs**: http://localhost:8000/docs

## 🔑 Demo Accounts

| Role | Email | Password |
|------|-------|----------|
| Admin | admin@demo.com | admin123 |
| Teacher | teacher@demo.com | admin123 |
| Student | student@demo.com | admin123 |

## ⚠️ Important Notes

- **Data is NOT saved!** This uses an in-memory database
- Data resets when you restart the backend server
- You can create new accounts, but they'll be lost on restart
- For production use, set up Supabase (see main README.md)

## ✨ What You Can Test

### As Admin
- ✅ Create resources (PDFs/videos)
- ✅ Manage resources
- ✅ View all data

### As Teacher
- ✅ Create assignments
- ✅ Add Google Meet links
- ✅ Record attendance
- ✅ Record marks

### As Student
- ✅ View assignments
- ✅ Submit assignments
- ✅ View resources
- ✅ Check attendance & marks

## 🛑 To Stop Servers

Press **Ctrl+C** in each terminal window, or close the windows.

## 🔧 Troubleshooting

**Port already in use?**
- Make sure no other apps are using port 3000 or 8000
- Close any previously running instances

**Backend won't start?**
- Make sure you're in the correct directory
- Check that Python dependencies are installed

**Frontend won't start?**
- Make sure Node.js dependencies are installed
- Run `npm install` in src/frontend if needed

## 📚 Next Steps

Ready for production? See `docs/SETUP.md` for Supabase setup instructions.
