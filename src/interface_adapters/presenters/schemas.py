"""Pydantic schemas for API request/response."""
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime


class UserBase(BaseModel):
    """Base user schema."""
    username: str


class User(UserBase):
    """User response schema."""
    id: int
    
    class Config:
        from_attributes = True


class AlertBase(BaseModel):
    """Base alert schema."""
    content: str


class Alert(AlertBase):
    """Alert response schema."""
    id: int
    created_at: datetime
    user_id: int
    
    class Config:
        from_attributes = True


class RoomBase(BaseModel):
    """Base room schema."""
    name: str


class Room(RoomBase):
    """Room response schema."""
    id: int
    users: List[User] = []
    
    class Config:
        from_attributes = True


# Schemas for Request Body
class LoginRequest(BaseModel):
    """Login request schema."""
    username: str
    password: str


class RegisterRequest(BaseModel):
    """Register request schema."""
    username: str
    password: str


class LogoutRequest(BaseModel):
    """Logout request schema."""
    token: str
