"""Logout Use Case - Handles user logout."""
from src.interface_adapters.repositories.repository_interfaces import TokenRepositoryInterface


class LogoutUseCase:
    """Use case for user logout."""
    
    def __init__(self, token_repository: TokenRepositoryInterface):
        self.token_repository = token_repository
    
    def execute(self, token_str: str) -> bool:
        """
        Execute logout use case.
        
        Args:
            token_str: Token string (format: "Token_<key>")
            
        Returns:
            True if token was deleted successfully
        """
        # Parse token string
        if '_' not in token_str:
            return False
        
        parts = token_str.split('_')
        if len(parts) != 2 or parts[0] != 'Token':
            return False
        
        token_key = parts[1]
        
        # Delete token
        return self.token_repository.delete(token_key)
