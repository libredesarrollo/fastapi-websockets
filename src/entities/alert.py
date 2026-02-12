"""Alert entity - Core business model."""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Alert:
    """Alert entity representing a message in a room."""
    id: Optional[int]
    content: str
    user_id: int
    room_id: int
    created_at: Optional[datetime] = None
