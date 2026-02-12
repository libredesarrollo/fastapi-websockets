"""Get Rooms Use Case - Retrieves all rooms."""
from typing import List
from src.entities.room import Room
from src.interface_adapters.repositories.repository_interfaces import RoomRepositoryInterface


class GetRoomsUseCase:
    """Use case for retrieving all rooms."""
    
    def __init__(self, room_repository: RoomRepositoryInterface):
        self.room_repository = room_repository
    
    def execute(self) -> List[Room]:
        """
        Execute get rooms use case.
        
        Returns:
            List of all rooms
        """
        return self.room_repository.get_all()
