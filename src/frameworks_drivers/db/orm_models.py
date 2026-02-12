"""SQLAlchemy ORM models."""
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from src.frameworks_drivers.db.connection import Base
import secrets

# Tabla intermedia para la relación ManyToMany entre Room y User
room_users = Table('room_users', Base.metadata,
    Column('room_id', Integer, ForeignKey('rooms.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)


class UserORM(Base):
    """SQLAlchemy ORM model for User."""
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)
    
    alerts = relationship("AlertORM", back_populates="user")
    rooms_joined = relationship("RoomORM", secondary=room_users, back_populates="users")
    auth_token = relationship("TokenORM", back_populates="user", uselist=False)


class AlertORM(Base):
    """SQLAlchemy ORM model for Alert."""
    __tablename__ = "alerts"
    id = Column(Integer, primary_key=True, index=True)
    content = Column(String(200))
    user_id = Column(Integer, ForeignKey("users.id"))
    room_id = Column(Integer, ForeignKey("rooms.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    user = relationship("UserORM", back_populates="alerts")
    room = relationship("RoomORM", back_populates="alerts")


class RoomORM(Base):
    """SQLAlchemy ORM model for Room."""
    __tablename__ = "rooms"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(60), unique=True)
    
    alerts = relationship("AlertORM", back_populates="room")
    users = relationship("UserORM", secondary=room_users, back_populates="rooms_joined")


class TokenORM(Base):
    """SQLAlchemy ORM model for Token."""
    __tablename__ = "tokens"
    # Generamos una key similar a DRF
    key = Column(String, primary_key=True, index=True, default=lambda: secrets.token_hex(20))
    user_id = Column(Integer, ForeignKey("users.id"))
    
    user = relationship("UserORM", back_populates="auth_token")
