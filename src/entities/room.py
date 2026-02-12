"""Room entity - Core business model."""
from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Room:
    """Room entity representing a chat room."""
    id: Optional[int]
    name: str
    user_ids: List[int] = field(default_factory=list)
