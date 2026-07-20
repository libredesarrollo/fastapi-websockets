from pydantic import BaseModel, ConfigDict
from typing import List, Optional
from datetime import datetime

class UserBase(BaseModel):
    username: str

class User(UserBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class AlertBase(BaseModel):
    content: str

class Alert(AlertBase):
    id: int
    created_at: datetime
    user_id: int
    model_config = ConfigDict(from_attributes=True)

class RoomBase(BaseModel):
    name: str

class Room(RoomBase):
    id: int
    users: List[User] = []
    model_config = ConfigDict(from_attributes=True)

# Schemas para Request Body
class LoginRequest(BaseModel):
    username: str
    password: str

class RegisterRequest(BaseModel):
    username: str
    password: str

class LogoutRequest(BaseModel):
    token: str