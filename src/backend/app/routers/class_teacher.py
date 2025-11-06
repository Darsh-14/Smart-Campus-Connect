from fastapi import APIRouter, Depends, HTTPException
from app.models import TeacherAssign, AttendanceResponse, MarksResponse
from app.database import supabase
from app.auth import require_role
from uuid import UUID
from typing import List

router = APIRouter(prefix="/class-teacher", tags=["Class Teacher"])


@router.post("/teachers", dependencies=[Depends(require_role(["class_teacher"]))])
async def add_teacher(teacher: TeacherAssign, current_user: dict = Depends(require_role(["class_teacher"]))):
    # Verify teacher exists
    teacher_response = supabase.table("users").select("*").eq("id", str(teacher.teacher_id)).eq("role", "teacher").execute()
    
    if not teacher_response.data:
        raise HTTPException(status_code=404, detail="Teacher not found")
    
    # Assign teacher to subject
    assignment_data = {
        "teacher_id": str(teacher.teacher_id),
        "subject": teacher.subject,
        "assigned_by": str(current_user["id"])
    }
    
    response = supabase.table("teacher_assignments").insert(assignment_data).execute()
    
    return {"message": "Teacher assigned successfully", "data": response.data[0]}


@router.get("/marks", response_model=List[MarksResponse], dependencies=[Depends(require_role(["class_teacher"]))])
async def get_student_marks(current_user: dict = Depends(require_role(["class_teacher"]))):
    # Get all marks for students in the class
    response = supabase.table("marks").select("*").execute()
    return response.data


@router.get("/marks/{student_id}", response_model=List[MarksResponse], dependencies=[Depends(require_role(["class_teacher"]))])
async def get_student_marks_by_id(student_id: UUID, current_user: dict = Depends(require_role(["class_teacher"]))):
    response = supabase.table("marks").select("*").eq("student_id", str(student_id)).execute()
    return response.data


@router.get("/attendance", response_model=List[AttendanceResponse], dependencies=[Depends(require_role(["class_teacher"]))])
async def get_student_attendance(current_user: dict = Depends(require_role(["class_teacher"]))):
    response = supabase.table("attendance").select("*").execute()
    return response.data


@router.get("/attendance/{student_id}", response_model=List[AttendanceResponse], dependencies=[Depends(require_role(["class_teacher"]))])
async def get_student_attendance_by_id(student_id: UUID, current_user: dict = Depends(require_role(["class_teacher"]))):
    response = supabase.table("attendance").select("*").eq("student_id", str(student_id)).execute()
    return response.data
