"""Token Repository implementation with SQLAlchemy."""
from typing import Optional
from sqlalchemy.orm import Session
from src.entities.token import Token
from src.interface_adapters.repositories.repository_interfaces import TokenRepositoryInterface
from src.frameworks_drivers.db.orm_models import TokenORM


class SQLTokenRepository(TokenRepositoryInterface):
    """SQLAlchemy implementation of TokenRepositoryInterface."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_by_key(self, key: str) -> Optional[Token]:
        """Get token by key."""
        token_orm = self.db.query(TokenORM).filter(TokenORM.key == key).first()
        if not token_orm:
            return None
        return self._to_entity(token_orm)
    
    def get_by_user_id(self, user_id: int) -> Optional[Token]:
        """Get token by user ID."""
        token_orm = self.db.query(TokenORM).filter(TokenORM.user_id == user_id).first()
        if not token_orm:
            return None
        return self._to_entity(token_orm)
    
    def create(self, token: Token) -> Token:
        """Create a new token."""
        token_orm = TokenORM(
            key=token.key,
            user_id=token.user_id
        )
        self.db.add(token_orm)
        self.db.commit()
        self.db.refresh(token_orm)
        return self._to_entity(token_orm)
    
    def delete(self, key: str) -> bool:
        """Delete a token by key."""
        token_orm = self.db.query(TokenORM).filter(TokenORM.key == key).first()
        if token_orm:
            self.db.delete(token_orm)
            self.db.commit()
            return True
        return False
    
    @staticmethod
    def _to_entity(token_orm: TokenORM) -> Token:
        """Convert ORM model to entity."""
        return Token(
            key=token_orm.key,
            user_id=token_orm.user_id
        )
