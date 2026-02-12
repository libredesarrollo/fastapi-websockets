"""Login Use Case - Handles user authentication."""
from typing import Optional
import bcrypt
from src.entities.user import User
from src.entities.token import Token
from src.interface_adapters.repositories.repository_interfaces import (
    UserRepositoryInterface,
    TokenRepositoryInterface
)


class LoginUseCase:
    """Use case for user login."""
    
    def __init__(
        self,
        user_repository: UserRepositoryInterface,
        token_repository: TokenRepositoryInterface
    ):
        self.user_repository = user_repository
        self.token_repository = token_repository
    
    def execute(self, username: str, password: str) -> Optional[str]:
        """
        Execute login use case.
        
        Args:
            username: User's username
            password: User's plain password
            
        Returns:
            Token key if successful, None otherwise
        """
        # Get user by username
        user = self.user_repository.get_by_username(username)
        if not user:
            return None
        
        # Verify password
        if not self._verify_password(password, user.password):
            return None
        
        # Get or create token
        token = self.token_repository.get_by_user_id(user.id)
        if not token:
            import secrets
            token = Token(
                key=secrets.token_hex(20),
                user_id=user.id
            )
            token = self.token_repository.create(token)
        
        return token.key
    
    @staticmethod
    def _verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify password against hash."""
        password_byte_enc = plain_password.encode('utf-8')
        hashed_password_enc = hashed_password.encode('utf-8')
        return bcrypt.checkpw(password_byte_enc, hashed_password_enc)
