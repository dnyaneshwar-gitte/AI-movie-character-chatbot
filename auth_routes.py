# auth_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel,EmailStr
from auth import create_user, authenticate_user, create_access_token

router = APIRouter()

class UserRegister(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"

@router.post("/signup", status_code=201)
async def signup(user: UserRegister):
    created = create_user(user.name, user.email, user.password)
    if created is None:
        raise HTTPException(status_code=400, detail="Email already registered")
    return {"message": "User created successfully"}

@router.post("/login", response_model=TokenResponse)
async def login(user: UserLogin):
    auth_user = authenticate_user(user.email, user.password)
    if not auth_user:
        raise HTTPException(status_code=401, detail="Invalid email or password")
    access_token = create_access_token(data={"sub": auth_user["email"]})
    return {"access_token": access_token}