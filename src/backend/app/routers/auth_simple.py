from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserLogin, Token, UserResponse
from app.database import supabase
from app.config import settings
from jose import jwt
from datetime import datetime, timedelta
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication"])


def create_token(user_id: str) -> str:
    expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode = {"sub": user_id, "exp": expire}
    return jwt.encode(to_encode, settings.JWT_SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    # Check if user exists
    existing = supabase.table("users").select("*").eq("email", user.email).execute()
    if existing.data:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Store with plaintext password for demo
    user_data = {
        "email": user.email,
        "password": user.password,  # Plaintext for demo
        "role": user.role,
        "name": user.name,
        "department": user.department
    }
    
    response = supabase.table("users").insert(user_data).execute()
    if not response.data:
        raise HTTPException(status_code=500, detail="Failed to create user")
    
    created_user = response.data[0]
    access_token = create_token(str(created_user["id"]))
    
    user_response = UserResponse(
        id=UUID(created_user["id"]),
        email=created_user["email"],
        role=created_user["role"],
        name=created_user["name"],
        department=created_user.get("department")
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    # Find user
    response = supabase.table("users").select("*").eq("email", credentials.email).execute()
    
    if not response.data:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    user = response.data[0]
    
    # Simple password check for demo
    if user["password"] != credentials.password:
        raise HTTPException(status_code=401, detail="Incorrect email or password")
    
    access_token = create_token(str(user["id"]))
    
    user_response = UserResponse(
        id=UUID(user["id"]),
        email=user["email"],
        role=user["role"],
        name=user["name"],
        department=user.get("department")
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)
