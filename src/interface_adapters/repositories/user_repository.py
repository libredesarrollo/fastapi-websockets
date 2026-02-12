"""User Repository implementation with SQLAlchemy."""
from typing import Optional
from sqlalchemy.orm import Session
from src.entities.user import User
from src.interface_adapters.repositories.repository_interfaces import UserRepositoryInterface
from src.frameworks_drivers.db.orm_models import UserORM


class SQLUserRepository(UserRepositoryInterface):
    """SQLAlchemy implementation of UserRepositoryInterface."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        user_orm = self.db.query(UserORM).filter(UserORM.id == user_id).first()
        if not user_orm:
            return None
        return self._to_entity(user_orm)
    
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        user_orm = self.db.query(UserORM).filter(UserORM.username == username).first()
        if not user_orm:
            return None
        return self._to_entity(user_orm)
    
    def create(self, user: User) -> User:
        """Create a new user."""
        user_orm = UserORM(
            username=user.username,
            password=user.password
        )
        self.db.add(user_orm)
        self.db.commit()
        self.db.refresh(user_orm)
        return self._to_entity(user_orm)
    
    def update(self, user: User) -> User:
        """Update an existing user."""
        user_orm = self.db.query(UserORM).filter(UserORM.id == user.id).first()
        if user_orm:
            user_orm.username = user.username
            user_orm.password = user.password
            self.db.commit()
            self.db.refresh(user_orm)
        return self._to_entity(user_orm)
    
    @staticmethod
    def _to_entity(user_orm: UserORM) -> User:
        """Convert ORM model to entity."""
        return User(
            id=user_orm.id,
            username=user_orm.username,
            password=user_orm.password
        )
