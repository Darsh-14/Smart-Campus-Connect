from fastapi import APIRouter, Depends, HTTPException
from app.models import AssignmentCreate, AssignmentUpdate, AssignmentResponse, AttendanceCreate, MarksCreate
from app.database import supabase
from app.auth import require_role
from uuid import UUID
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/teacher", tags=["Teacher"])


@router.post("/assignments", response_model=AssignmentResponse, dependencies=[Depends(require_role(["teacher"]))])
async def create_assignment(assignment: AssignmentCreate, current_user: dict = Depends(require_role(["teacher"]))):
    assignment_data = {
        "title": assignment.title,
        "description": assignment.description,
        "due_date": assignment.due_date.isoformat(),
        "meet_link": assignment.meet_link,
        "created_by": str(current_user["id"])
    }
    
    response = supabase.table("assignments").insert(assignment_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create assignment")
    
    created_assignment = response.data[0]
    
    # Create student assignment records for all students
    students_response = supabase.table("users").select("id").eq("role", "student").execute()
    
    if students_response.data:
        student_assignments = [
            {
                "assignment_id": created_assignment["id"],
                "student_id": str(student["id"]),
                "submitted": False
            }
            for student in students_response.data
        ]
        supabase.table("student_assignments").insert(student_assignments).execute()
    
    return created_assignment


@router.get("/assignments", response_model=List[AssignmentResponse], dependencies=[Depends(require_role(["teacher"]))])
async def get_assignments(current_user: dict = Depends(require_role(["teacher"]))):
    response = supabase.table("assignments").select("*").eq("created_by", str(current_user["id"])).execute()
    return response.data


@router.get("/assignments/{assignment_id}", response_model=AssignmentResponse, dependencies=[Depends(require_role(["teacher"]))])
async def get_assignment(assignment_id: UUID, current_user: dict = Depends(require_role(["teacher"]))):
    response = supabase.table("assignments").select("*").eq("id", str(assignment_id)).eq("created_by", str(current_user["id"])).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return response.data[0]


@router.put("/assignments/{assignment_id}", response_model=AssignmentResponse, dependencies=[Depends(require_role(["teacher"]))])
async def update_assignment(assignment_id: UUID, assignment: AssignmentUpdate, current_user: dict = Depends(require_role(["teacher"]))):
    update_data = {}
    if assignment.title is not None:
        update_data["title"] = assignment.title
    if assignment.description is not None:
        update_data["description"] = assignment.description
    if assignment.due_date is not None:
        update_data["due_date"] = assignment.due_date.isoformat()
    if assignment.meet_link is not None:
        update_data["meet_link"] = assignment.meet_link
    
    response = supabase.table("assignments").update(update_data).eq("id", str(assignment_id)).eq("created_by", str(current_user["id"])).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return response.data[0]


@router.delete("/assignments/{assignment_id}", dependencies=[Depends(require_role(["teacher"]))])
async def delete_assignment(assignment_id: UUID, current_user: dict = Depends(require_role(["teacher"]))):
    response = supabase.table("assignments").delete().eq("id", str(assignment_id)).eq("created_by", str(current_user["id"])).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {"message": "Assignment deleted successfully"}


@router.post("/attendance", dependencies=[Depends(require_role(["teacher"]))])
async def record_attendance(attendance: AttendanceCreate, current_user: dict = Depends(require_role(["teacher"]))):
    attendance_data = {
        "student_id": str(attendance.student_id),
        "subject": attendance.subject,
        "present_days": attendance.present_days,
        "total_days": attendance.total_days
    }
    
    # Check if record exists
    existing = supabase.table("attendance").select("*").eq("student_id", str(attendance.student_id)).eq("subject", attendance.subject).execute()
    
    if existing.data:
        # Update existing record
        response = supabase.table("attendance").update(attendance_data).eq("student_id", str(attendance.student_id)).eq("subject", attendance.subject).execute()
    else:
        # Create new record
        response = supabase.table("attendance").insert(attendance_data).execute()
    
    return {"message": "Attendance recorded successfully", "data": response.data[0]}


@router.post("/marks", dependencies=[Depends(require_role(["teacher"]))])
async def record_marks(marks: MarksCreate, current_user: dict = Depends(require_role(["teacher"]))):
    marks_data = {
        "student_id": str(marks.student_id),
        "subject": marks.subject,
        "marks_obtained": marks.marks_obtained,
        "total_marks": marks.total_marks
    }
    
    # Check if record exists
    existing = supabase.table("marks").select("*").eq("student_id", str(marks.student_id)).eq("subject", marks.subject).execute()
    
    if existing.data:
        # Update existing record
        response = supabase.table("marks").update(marks_data).eq("student_id", str(marks.student_id)).eq("subject", marks.subject).execute()
    else:
        # Create new record
        response = supabase.table("marks").insert(marks_data).execute()
    
    return {"message": "Marks recorded successfully", "data": response.data[0]}
