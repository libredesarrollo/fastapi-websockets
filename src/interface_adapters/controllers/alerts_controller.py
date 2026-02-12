"""Alerts controller - HTTP routes for alerts."""
from fastapi import APIRouter, Depends
from typing import List, Optional
from src.entities.user import User
from src.interface_adapters.presenters.schemas import Alert
from src.use_cases.alerts.get_alerts import GetAlertsUseCase
from src.frameworks_drivers.http.dependencies import (
    get_alert_repository,
    get_current_user
)

router = APIRouter()


@router.get("/alerts", response_model=List[Alert])
def get_alerts(
    room_id: Optional[int] = None,
    user: User = Depends(get_current_user),
    alert_repo=Depends(get_alert_repository)
):
    """Get alerts endpoint with optional room filtering."""
    use_case = GetAlertsUseCase(alert_repo)
    alerts = use_case.execute(room_id=room_id)
    
    # Convert entities to ORM-compatible format for Pydantic
    return [
        {
            "id": alert.id,
            "content": alert.content,
            "created_at": alert.created_at,
            "user_id": alert.user_id
        }
        for alert in alerts
    ]
