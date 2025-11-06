from fastapi import APIRouter, Depends, HTTPException
from app.models import ResourceCreate, ResourceResponse, GrantAccess
from app.database import supabase
from app.auth import require_role
from uuid import UUID
from typing import List

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/resources", response_model=ResourceResponse, dependencies=[Depends(require_role(["admin"]))])
async def create_resource(resource: ResourceCreate, current_user: dict = Depends(require_role(["admin"]))):
    resource_data = {
        "title": resource.title,
        "resource_type": resource.resource_type,
        "link": resource.link,
        "uploaded_by": str(current_user["id"])
    }
    
    response = supabase.table("resources").insert(resource_data).execute()
    
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create resource")
    
    return response.data[0]


@router.get("/resources", response_model=List[ResourceResponse], dependencies=[Depends(require_role(["admin"]))])
async def get_resources(current_user: dict = Depends(require_role(["admin"]))):
    response = supabase.table("resources").select("*").execute()
    return response.data


@router.put("/resources/{resource_id}", response_model=ResourceResponse, dependencies=[Depends(require_role(["admin"]))])
async def update_resource(resource_id: UUID, resource: ResourceCreate, current_user: dict = Depends(require_role(["admin"]))):
    resource_data = {
        "title": resource.title,
        "resource_type": resource.resource_type,
        "link": resource.link
    }
    
    response = supabase.table("resources").update(resource_data).eq("id", str(resource_id)).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return response.data[0]


@router.delete("/resources/{resource_id}", dependencies=[Depends(require_role(["admin"]))])
async def delete_resource(resource_id: UUID, current_user: dict = Depends(require_role(["admin"]))):
    response = supabase.table("resources").delete().eq("id", str(resource_id)).execute()
    
    if not response.data:
        raise HTTPException(status_code=404, detail="Resource not found")
    
    return {"message": "Resource deleted successfully"}


@router.post("/grant-access", dependencies=[Depends(require_role(["admin"]))])
async def grant_access(access: GrantAccess, current_user: dict = Depends(require_role(["admin"]))):
    # Verify class teacher exists
    teacher_response = supabase.table("users").select("*").eq("id", str(access.class_teacher_id)).eq("role", "class_teacher").execute()
    
    if not teacher_response.data:
        raise HTTPException(status_code=404, detail="Class teacher not found")
    
    # Create access record (you may need to create a separate table for this)
    access_data = {
        "class_teacher_id": str(access.class_teacher_id),
        "class_name": access.class_name,
        "granted_by": str(current_user["id"])
    }
    
    response = supabase.table("class_access").insert(access_data).execute()
    
    return {"message": "Access granted successfully", "data": response.data[0]}
