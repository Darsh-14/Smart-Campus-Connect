from fastapi import APIRouter, Depends, HTTPException
from app.models import AssignmentResponse, ResourceResponse, AttendanceResponse, MarksResponse
from app.database import supabase
from app.auth import require_role
from typing import List
from datetime import datetime, timedelta

router = APIRouter(prefix="/student", tags=["Student"])


@router.get("/assignments", response_model=List[AssignmentResponse], dependencies=[Depends(require_role(["student"]))])
async def get_student_assignments(current_user: dict = Depends(require_role(["student"]))):
    # Get all assignments for the student
    student_assignments = supabase.table("student_assignments").select("assignment_id").eq("student_id", str(current_user["id"])).execute()
    
    if not student_assignments.data:
        return []
    
    assignment_ids = [sa["assignment_id"] for sa in student_assignments.data]
    
    # Get assignment details
    assignments = supabase.table("assignments").select("*").in_("id", assignment_ids).execute()
    
    return assignments.data


@router.get("/assignments/upcoming", response_model=List[AssignmentResponse], dependencies=[Depends(require_role(["student"]))])
async def get_upcoming_assignments(current_user: dict = Depends(require_role(["student"]))):
    # Get assignments due in the next 2 days
    today = datetime.now().date()
    two_days_later = (datetime.now() + timedelta(days=2)).date()
    
    student_assignments = supabase.table("student_assignments").select("assignment_id").eq("student_id", str(current_user["id"])).eq("submitted", False).execute()
    
    if not student_assignments.data:
        return []
    
    assignment_ids = [sa["assignment_id"] for sa in student_assignments.data]
    
    assignments = supabase.table("assignments").select("*").in_("id", assignment_ids).gte("due_date", today.isoformat()).lte("due_date", two_days_later.isoformat()).execute()
    
    return assignments.data


@router.post("/assignments/{assignment_id}/submit", dependencies=[Depends(require_role(["student"]))])
async def submit_assignment(assignment_id: str, current_user: dict = Depends(require_role(["student"]))):
    update_data = {
        "submitted": True,
        "submitted_date": datetime.now().isoformat()
    }
    
    response = supabase.table("student_assignments").update(update_data).eq("assignment_id", assignment_id).eq("student_id", str(current_user["id"])).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Assignment not found")
    
    return {"message": "Assignment submitted successfully"}


@router.get("/resources", response_model=List[ResourceResponse], dependencies=[Depends(require_role(["student"]))])
async def get_resources(current_user: dict = Depends(require_role(["student"]))):
    response = supabase.table("resources").select("*").execute()
    return response.data


@router.get("/attendance", response_model=List[AttendanceResponse], dependencies=[Depends(require_role(["student"]))])
async def get_attendance(current_user: dict = Depends(require_role(["student"]))):
    response = supabase.table("attendance").select("*").eq("student_id", str(current_user["id"])).execute()
    return response.data


@router.get("/marks", response_model=List[MarksResponse], dependencies=[Depends(require_role(["student"]))])
async def get_marks(current_user: dict = Depends(require_role(["student"]))):
    response = supabase.table("marks").select("*").eq("student_id", str(current_user["id"])).execute()
    return response.data
