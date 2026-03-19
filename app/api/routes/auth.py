from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from datetime import datetime, timedelta
import secrets
import logging

from app.core.database import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, ForgotPasswordRequest, ResetPasswordRequest, ChangePasswordRequest, ProfileUpdateRequest
from app.schemas.user import UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.api.deps import get_current_user

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/register")
async def register(user: UserCreate, db: AsyncSession = Depends(get_db)):
    logger.info(f"Registration request received: {user}")
    
    result = await db.execute(select(User).where(User.email == user.email))
    existing = result.scalar_one_or_none()

    if existing:
        logger.error(f"Email already exists: {user.email}")
        raise HTTPException(status_code=400, detail="Email already exists")

    new_user = User(
        email=user.email,
        password=hash_password(user.password),
        name=user.name
    )

    db.add(new_user)
    await db.commit()

    logger.info(f"User registered successfully: {user.email}")
    return {"success": True}

@router.post("/login")
async def login(user: UserLogin, db: AsyncSession = Depends(get_db)):
    logger.info(f"Login request received: {user}")
    
    result = await db.execute(select(User).where(User.email == user.email))
    db_user = result.scalar_one_or_none()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    token = create_access_token({"sub": str(db_user.id)})

    return {
        "success": True,
        "data": {
            "token": token
        }
    }

@router.post("/forgot-password")
async def forgot_password(request: ForgotPasswordRequest, db: AsyncSession = Depends(get_db)):
    logger.info(f"Forgot password request received: {request.email}")
    
    result = await db.execute(select(User).where(User.email == request.email))
    user = result.scalar_one_or_none()
    
    if user:
        token = secrets.token_urlsafe(32)
        user.password_reset_token = token
        user.password_reset_expires = datetime.utcnow() + timedelta(hours=1)
        await db.commit()
        logger.info(f"Password reset token generated for: {request.email}")
    
    return {"success": True, "message": "If the email exists, a reset link has been sent"}

@router.post("/reset-password")
async def reset_password(request: ResetPasswordRequest, db: AsyncSession = Depends(get_db)):
    logger.info("Password reset request received")
    
    result = await db.execute(
        select(User).where(
            User.password_reset_token == request.token,
            User.password_reset_expires > datetime.utcnow()
        )
    )
    user = result.scalar_one_or_none()
    
    if not user:
        raise HTTPException(status_code=400, detail="Invalid or expired token")
    
    user.password = hash_password(request.password)
    user.password_reset_token = None
    user.password_reset_expires = None
    await db.commit()
    
    logger.info(f"Password reset successful for: {user.email}")
    return {"success": True, "message": "Password reset successful"}

@router.post("/change-password")
async def change_password(
    request: ChangePasswordRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Change password request for: {current_user.email}")
    
    if not verify_password(request.current_password, current_user.password):
        raise HTTPException(status_code=400, detail="Current password is incorrect")
    
    current_user.password = hash_password(request.new_password)
    await db.commit()
    
    logger.info(f"Password changed successfully for: {current_user.email}")
    return {"success": True, "message": "Password changed successfully"}

@router.get("/profile")
async def get_profile(
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Get profile request for: {current_user.email}")
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "name": current_user.name,
            "phone": current_user.phone,
            "age": current_user.age,
            "weight": current_user.weight,
            "height": current_user.height,
            "goal": current_user.goal
        }
    }

@router.put("/profile")
async def update_profile(
    request: ProfileUpdateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    logger.info(f"Update profile request for: {current_user.email}")
    
    if request.name is not None:
        current_user.name = request.name
    if request.phone is not None:
        current_user.phone = request.phone
    if request.age is not None:
        current_user.age = request.age
    if request.weight is not None:
        current_user.weight = request.weight
    if request.height is not None:
        current_user.height = request.height
    if request.goal is not None:
        current_user.goal = request.goal
    
    await db.commit()
    
    return {
        "success": True,
        "data": {
            "id": str(current_user.id),
            "email": current_user.email,
            "name": current_user.name,
            "phone": current_user.phone,
            "age": current_user.age,
            "weight": current_user.weight,
            "height": current_user.height,
            "goal": current_user.goal
        }
    }