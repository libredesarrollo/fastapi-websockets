"""Create Alert Use Case - Handles saving a new alert via WebSocket."""
from src.entities.alert import Alert
from src.interface_adapters.repositories.repository_interfaces import AlertRepositoryInterface


class CreateAlertUseCase:
    """Use case for creating a new alert."""
    
    def __init__(self, alert_repository: AlertRepositoryInterface):
        self.alert_repository = alert_repository
    
    def execute(self, content: str, user_id: int, room_id: int) -> Alert:
        """
        Execute create alert use case.
        
        Args:
            content: Message content
            user_id: User ID who sent the message
            room_id: Room ID where message was sent
            
        Returns:
            The created Alert entity
        """
        alert = Alert(
            id=None,
            content=content,
            user_id=user_id,
            room_id=room_id
        )
        return self.alert_repository.create(alert)
