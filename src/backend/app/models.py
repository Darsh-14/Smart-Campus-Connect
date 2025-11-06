from pydantic import BaseModel, EmailStr
from typing import Optional, Literal
from datetime import datetime, date
from uuid import UUID


# User Models
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: Literal["admin", "class_teacher", "teacher", "student"]
    name: str
    department: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    role: str
    name: str
    department: Optional[str] = None


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserResponse


# Resource Models
class ResourceCreate(BaseModel):
    title: str
    resource_type: Literal["pdf", "video"]
    link: str


class ResourceResponse(BaseModel):
    id: UUID
    title: str
    resource_type: str
    link: str
    uploaded_by: UUID
    created_at: datetime


# Assignment Models
class AssignmentCreate(BaseModel):
    title: str
    description: str
    due_date: date
    meet_link: Optional[str] = None


class AssignmentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[date] = None
    meet_link: Optional[str] = None


class AssignmentResponse(BaseModel):
    id: UUID
    title: str
    description: str
    due_date: date
    meet_link: Optional[str]
    created_by: UUID
    created_at: datetime


# Teacher Management
class TeacherAssign(BaseModel):
    teacher_id: UUID
    subject: str


# Attendance Models
class AttendanceCreate(BaseModel):
    student_id: UUID
    subject: str
    present_days: int
    total_days: int


class AttendanceResponse(BaseModel):
    id: UUID
    student_id: UUID
    subject: str
    present_days: int
    total_days: int


# Marks Models
class MarksCreate(BaseModel):
    student_id: UUID
    subject: str
    marks_obtained: int
    total_marks: int


class MarksResponse(BaseModel):
    id: UUID
    student_id: UUID
    subject: str
    marks_obtained: int
    total_marks: int


# Access Grant
class GrantAccess(BaseModel):
    class_teacher_id: UUID
    class_name: str
