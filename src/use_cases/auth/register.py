"""Register Use Case - Handles user registration."""
import bcrypt
from src.entities.user import User
from src.interface_adapters.repositories.repository_interfaces import UserRepositoryInterface


class RegisterUseCase:
    """Use case for user registration."""
    
    def __init__(self, user_repository: UserRepositoryInterface):
        self.user_repository = user_repository
    
    def execute(self, username: str, password: str) -> bool:
        """
        Execute registration use case.
        
        Args:
            username: Desired username
            password: User's plain password
            
        Returns:
            True if successful, False if username already exists
        """
        # Check if username already exists
        existing_user = self.user_repository.get_by_username(username)
        if existing_user:
            return False
        
        # Hash password
        hashed_password = self._hash_password(password)
        
        # Create user
        new_user = User(
            id=None,
            username=username,
            password=hashed_password
        )
        self.user_repository.create(new_user)
        
        return True
    
    @staticmethod
    def _hash_password(password: str) -> str:
        """Hash password using bcrypt."""
        pwd_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(pwd_bytes, salt)
        return hashed_password.decode('utf-8')
