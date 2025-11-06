from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth_simple as auth, admin, class_teacher, teacher, student
from app.scheduler import start_scheduler, shutdown_scheduler
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Smart Campus Connect API",
    description="Role-based college management platform API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],  # React frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(admin.router)
app.include_router(class_teacher.router)
app.include_router(teacher.router)
app.include_router(student.router)


@app.on_event("startup")
async def startup_event():
    """Start background tasks on application startup"""
    logger.info("Starting Smart Campus Connect API...")
    start_scheduler()


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on application shutdown"""
    logger.info("Shutting down Smart Campus Connect API...")
    shutdown_scheduler()


@app.get("/")
async def root():
    return {
        "message": "Smart Campus Connect API",
        "version": "1.0.0",
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    return {"status": "healthy"}
