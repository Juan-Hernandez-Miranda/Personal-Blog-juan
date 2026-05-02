"""Pydantic schemas for User resources and authentication."""

from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    """Base schema for user data."""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """Schema for creating a user (includes password)."""
    password: str


class UserLogin(BaseModel):
    """Schema for login request."""
    username: str
    password: str


class UserRead(UserBase):
    """Schema for reading user data (response)."""
    id: int
    is_active: bool
    is_admin: bool
    fecha_creacion: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    """Schema for JWT token response."""
    access_token: str
    token_type: str = "bearer"
    user: UserRead


class TokenData(BaseModel):
    """Schema for token payload data."""
    user_id: Optional[int] = None
    username: Optional[str] = None
