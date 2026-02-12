"""Room Repository implementation with SQLAlchemy."""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.entities.room import Room
from src.interface_adapters.repositories.repository_interfaces import RoomRepositoryInterface
from src.frameworks_drivers.db.orm_models import RoomORM


class SQLRoomRepository(RoomRepositoryInterface):
    """SQLAlchemy implementation of RoomRepositoryInterface."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self) -> List[Room]:
        """Get all rooms."""
        room_orms = self.db.query(RoomORM).all()
        return [self._to_entity(room_orm) for room_orm in room_orms]
    
    def get_by_id(self, room_id: int) -> Optional[Room]:
        """Get room by ID."""
        room_orm = self.db.query(RoomORM).filter(RoomORM.id == room_id).first()
        if not room_orm:
            return None
        return self._to_entity(room_orm)
    
    def create(self, room: Room) -> Room:
        """Create a new room."""
        room_orm = RoomORM(name=room.name)
        self.db.add(room_orm)
        self.db.commit()
        self.db.refresh(room_orm)
        return self._to_entity(room_orm)
    
    @staticmethod
    def _to_entity(room_orm: RoomORM) -> Room:
        """Convert ORM model to entity."""
        user_ids = [user.id for user in room_orm.users]
        return Room(
            id=room_orm.id,
            name=room_orm.name,
            user_ids=user_ids
        )
