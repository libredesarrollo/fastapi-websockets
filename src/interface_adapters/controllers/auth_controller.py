"""Auth controller - HTTP routes for authentication."""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from src.interface_adapters.presenters.schemas import LoginRequest, RegisterRequest, LogoutRequest
from src.use_cases.auth.login import LoginUseCase
from src.use_cases.auth.register import RegisterUseCase
from src.use_cases.auth.logout import LogoutUseCase
from src.frameworks_drivers.http.dependencies import (
    get_user_repository,
    get_token_repository
)

router = APIRouter()


@router.post("/login")
def login(
    request: LoginRequest,
    user_repo=Depends(get_user_repository),
    token_repo=Depends(get_token_repository)
):
    """Login endpoint."""
    use_case = LoginUseCase(user_repo, token_repo)
    token_key = use_case.execute(request.username, request.password)
    
    if not token_key:
        return JSONResponse(
            "Invalid credentials",
            status_code=status.HTTP_401_UNAUTHORIZED
        )
    
    return {"token": f"Token_{token_key}"}


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(
    request: RegisterRequest,
    user_repo=Depends(get_user_repository)
):
    """Register endpoint."""
    use_case = RegisterUseCase(user_repo)
    success = use_case.execute(request.username, request.password)
    
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    return {"message": "User created successfully"}


@router.post("/logout")
def logout(
    request: LogoutRequest,
    token_repo=Depends(get_token_repository)
):
    """Logout endpoint."""
    use_case = LogoutUseCase(token_repo)
    use_case.execute(request.token)
    return {"message": "ok"}
