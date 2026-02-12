"""Alert Repository implementation with SQLAlchemy."""
from typing import List, Optional
from sqlalchemy.orm import Session
from src.entities.alert import Alert
from src.interface_adapters.repositories.repository_interfaces import AlertRepositoryInterface
from src.frameworks_drivers.db.orm_models import AlertORM


class SQLAlertRepository(AlertRepositoryInterface):
    """SQLAlchemy implementation of AlertRepositoryInterface."""
    
    def __init__(self, db: Session):
        self.db = db
    
    def get_all(self, room_id: Optional[int] = None) -> List[Alert]:
        """Get all alerts, optionally filtered by room_id."""
        query = self.db.query(AlertORM)
        if room_id:
            query = query.filter(AlertORM.room_id == room_id)
        alert_orms = query.order_by(AlertORM.created_at).all()
        return [self._to_entity(alert_orm) for alert_orm in alert_orms]
    
    def create(self, alert: Alert) -> Alert:
        """Create a new alert."""
        alert_orm = AlertORM(
            content=alert.content,
            user_id=alert.user_id,
            room_id=alert.room_id
        )
        self.db.add(alert_orm)
        self.db.commit()
        self.db.refresh(alert_orm)
        return self._to_entity(alert_orm)
    
    @staticmethod
    def _to_entity(alert_orm: AlertORM) -> Alert:
        """Convert ORM model to entity."""
        return Alert(
            id=alert_orm.id,
            content=alert_orm.content,
            user_id=alert_orm.user_id,
            room_id=alert_orm.room_id,
            created_at=alert_orm.created_at
        )
