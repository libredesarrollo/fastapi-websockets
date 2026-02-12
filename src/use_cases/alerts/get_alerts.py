"""Get Alerts Use Case - Retrieves alerts."""
from typing import List, Optional
from src.entities.alert import Alert
from src.interface_adapters.repositories.repository_interfaces import AlertRepositoryInterface


class GetAlertsUseCase:
    """Use case for retrieving alerts."""
    
    def __init__(self, alert_repository: AlertRepositoryInterface):
        self.alert_repository = alert_repository
    
    def execute(self, room_id: Optional[int] = None) -> List[Alert]:
        """
        Execute get alerts use case.
        
        Args:
            room_id: Optional room ID to filter alerts
            
        Returns:
            List of alerts
        """
        return self.alert_repository.get_all(room_id=room_id)
