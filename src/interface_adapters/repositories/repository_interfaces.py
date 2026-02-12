"""Repository interfaces - Abstract contracts for data access."""
from abc import ABC, abstractmethod
from typing import Optional, List
from src.entities.user import User
from src.entities.alert import Alert
from src.entities.room import Room
from src.entities.token import Token


class UserRepositoryInterface(ABC):
    """Abstract interface for User repository."""
    
    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Get user by ID."""
        pass
    
    @abstractmethod
    def get_by_username(self, username: str) -> Optional[User]:
        """Get user by username."""
        pass
    
    @abstractmethod
    def create(self, user: User) -> User:
        """Create a new user."""
        pass
    
    @abstractmethod
    def update(self, user: User) -> User:
        """Update an existing user."""
        pass


class AlertRepositoryInterface(ABC):
    """Abstract interface for Alert repository."""
    
    @abstractmethod
    def get_all(self, room_id: Optional[int] = None) -> List[Alert]:
        """Get all alerts, optionally filtered by room_id."""
        pass
    
    @abstractmethod
    def create(self, alert: Alert) -> Alert:
        """Create a new alert."""
        pass


class RoomRepositoryInterface(ABC):
    """Abstract interface for Room repository."""
    
    @abstractmethod
    def get_all(self) -> List[Room]:
        """Get all rooms."""
        pass
    
    @abstractmethod
    def get_by_id(self, room_id: int) -> Optional[Room]:
        """Get room by ID."""
        pass
    
    @abstractmethod
    def create(self, room: Room) -> Room:
        """Create a new room."""
        pass


class TokenRepositoryInterface(ABC):
    """Abstract interface for Token repository."""
    
    @abstractmethod
    def get_by_key(self, key: str) -> Optional[Token]:
        """Get token by key."""
        pass
    
    @abstractmethod
    def get_by_user_id(self, user_id: int) -> Optional[Token]:
        """Get token by user ID."""
        pass
    
    @abstractmethod
    def create(self, token: Token) -> Token:
        """Create a new token."""
        pass
    
    @abstractmethod
    def delete(self, key: str) -> bool:
        """Delete a token by key."""
        pass
