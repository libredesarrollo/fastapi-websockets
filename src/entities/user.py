"""User entity - Core business model."""
from dataclasses import dataclass
from typing import Optional


@dataclass
class User:
    """User entity representing a user in the system."""
    id: Optional[int]
    username: str
    password: str
