from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base
import secrets

# Tabla intermedia para la relación ManyToMany entre Room y User
room_users = Table('room_users', Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
    alerts = relationship("Alert", back_populates="user")
    rooms_joined = relationship("Room", secondary=room_users, back_populates="users")
    auth_token = relationship("Token", back_populates="user", uselist=False)

class Alert(Base):
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"))
    create_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("User", back_populates="alerts")

class Room(Base):
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), unique=True)
    
    users = relationship("User", secondary=room_users, back_populates="rooms_joined")

class Token(Base):
    __tablename__ = "tokens"
    # Generamos una key similar a DRF
    key = Column(String, primary_key=True, index=True, default=lambda: secrets.token_hex(20))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("User", back_populates="auth_token")