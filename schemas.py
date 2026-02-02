from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: int
    class Config:
        orm_mode = True

class AlertBase(BaseModel):
    content: str

class Alert(AlertBase):
    id: int
    created_at: datetime
    user_id: int
    class Config:
        orm_mode = True

class RoomBase(BaseModel):
    name: str

class Room(RoomBase):
    id: int
    users: List[User] = []
    class Config:
        orm_mode = True

# Schemas para Request Body
class LoginRequest(BaseModel):
    username: str
    password: str

class LogoutRequest(BaseModel):
    token: str