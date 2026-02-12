"""HTTP layer dependencies - Dependency injection for controllers."""
from typing import Optional
from fastapi import Depends, HTTPException, status, Header
from sqlalchemy.orm import Session
from src.frameworks_drivers.db.connection import SessionLocal
from src.frameworks_drivers.db.orm_models import TokenORM
from src.entities.user import User
from src.interface_adapters.repositories.user_repository import SQLUserRepository
from src.interface_adapters.repositories.alert_repository import SQLAlertRepository
from src.interface_adapters.repositories.room_repository import SQLRoomRepository
from src.interface_adapters.repositories.token_repository import SQLTokenRepository


def get_db():
    """Database dependency."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_repository(db: Session = Depends(get_db)):
    """Get user repository instance."""
    return SQLUserRepository(db)


def get_alert_repository(db: Session = Depends(get_db)):
    """Get alert repository instance."""
    return SQLAlertRepository(db)


def get_room_repository(db: Session = Depends(get_db)):
    """Get room repository instance."""
    return SQLRoomRepository(db)


def get_token_repository(db: Session = Depends(get_db)):
    """Get token repository instance."""
    return SQLTokenRepository(db)


def get_current_user(
    authorization: Optional[str] = Header(None),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency for authentication - extracts current user from token.
    
    Args:
        authorization: Authorization header (format: "Token_<key>" or "Token <key>")
        db: Database session
        
    Returns:
        Current authenticated user
        
    Raises:
        HTTPException: If authentication fails
    """
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credentials missing"
        )
    
    # Parse token from header
    try:
        if "_" in authorization:
            _, key = authorization.split("_")
        else:
            _, key = authorization.split(" ")
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token format"
        )
    
    # Validate token
    token_orm = db.query(TokenORM).filter(TokenORM.key == key).first()
    if not token_orm:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid token"
        )
    
    # Return user entity
    user_orm = token_orm.user
    return User(
        id=user_orm.id,
        username=user_orm.username,
        password=user_orm.password
    )
