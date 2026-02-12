"""Rooms controller - HTTP routes for rooms."""
from fastapi import APIRouter, Depends
from typing import List
from sqlalchemy.orm import Session
from src.interface_adapters.presenters.schemas import Room
from src.use_cases.rooms.get_rooms import GetRoomsUseCase
from src.frameworks_drivers.http.dependencies import (
    get_room_repository,
    get_db
)
from src.frameworks_drivers.db.orm_models import RoomORM

router = APIRouter()


@router.get("/rooms", response_model=List[Room])
def get_rooms(
    room_repo=Depends(get_room_repository),
    db: Session = Depends(get_db)
):
    """Get all rooms endpoint."""
    # Use ORM directly for this endpoint to maintain relationship loading
    # This is a pragmatic choice to avoid complex entity->schema mapping
    return db.query(RoomORM).all()
