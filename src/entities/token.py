"""Token entity - Core business model."""
from dataclasses import dataclass


@dataclass
class Token:
    """Token entity representing an authentication token."""
    key: str
    user_id: int
