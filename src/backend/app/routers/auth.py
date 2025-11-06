from fastapi import APIRouter, HTTPException, status
from app.models import UserCreate, UserLogin, Token, UserResponse
from app.database import supabase
from app.auth import get_password_hash, verify_password, create_access_token
from uuid import UUID

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/signup", response_model=Token)
async def signup(user: UserCreate):
    try:
        # Check if user already exists
        existing_user = supabase.table("users").select("*").eq("email", user.email).execute()
        if existing_user.data:
            raise HTTPException(status_code=400, detail="Email already registered")
        
        # Hash password
        hashed_password = get_password_hash(user.password)
        
        # Create user in Supabase
        user_data = {
            "email": user.email,
            "password": hashed_password,
            "role": user.role,
            "name": user.name,
            "department": user.department
        }
        
        response = supabase.table("users").insert(user_data).execute()
        
        if not response.data:
            raise HTTPException(status_code=500, detail="Failed to create user")
        
        created_user = response.data[0]
        
        # Create access token
        access_token = create_access_token(data={"sub": str(created_user["id"])})
        
        user_response = UserResponse(
            id=UUID(created_user["id"]),
            email=created_user["email"],
            role=created_user["role"],
            name=created_user["name"],
            department=created_user.get("department")
        )
        
        return Token(access_token=access_token, token_type="bearer", user=user_response)
    except HTTPException:
        raise
    except Exception as e:
        print(f"Signup error: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Signup failed: {str(e)}")


@router.post("/login", response_model=Token)
async def login(credentials: UserLogin):
    # Find user by email
    response = supabase.table("users").select("*").eq("email", credentials.email).execute()
    
    if not response.data:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    user = response.data[0]
    
    # Verify password
    if not verify_password(credentials.password, user["password"]):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )
    
    # Create access token
    access_token = create_access_token(data={"sub": str(user["id"])})
    
    user_response = UserResponse(
        id=UUID(user["id"]),
        email=user["email"],
        role=user["role"],
        name=user["name"],
        department=user.get("department")
    )
    
    return Token(access_token=access_token, token_type="bearer", user=user_response)
