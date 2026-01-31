from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from passlib.context import CryptContext

import models
import schemas
from database import SessionLocal, engine

# Crear tablas en la BD (para propósitos de este ejemplo)
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Configuración de hashing de contraseñas
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Dependencia de Base de Datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Dependencia de Autenticación (Simula IsAuthenticated)
def get_current_user(authorization: Optional[str] = Header(None), db: Session = Depends(get_db)):
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credentials missing")
    
    # Esperamos formato "Token_<key>" o "Token <key>"
    try:
        if "_" in authorization:
            _, key = authorization.split("_")
        else:
            _, key = authorization.split(" ")
    except ValueError:
         raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token format")

    token = db.query(models.Token).filter(models.Token.key == key).first()
    if not token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
    
    return token.user

@router.post("/login")
def login(request: schemas.LoginRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    
    if not user:
        return JSONResponse("User invalid", status_code=status.HTTP_401_UNAUTHORIZED)
    
    if not verify_password(request.password, user.password):
        return JSONResponse("Password invalid", status_code=status.HTTP_401_UNAUTHORIZED)
    
    # Get or Create Token
    token = db.query(models.Token).filter(models.Token.user_id == user.id).first()
    if not token:
        token = models.Token(user_id=user.id)
        db.add(token)
        db.commit()
        db.refresh(token)
        
    return f"Token_{token.key}"

@router.post("/logout")
def logout(request: schemas.LogoutRequest, db: Session = Depends(get_db)):
    token_str = request.token

    if len(token_str.split('_')) == 2:
        token_name, token_key = token_str.split('_')
        if token_name == 'Token':
            token = db.query(models.Token).filter(models.Token.key == token_key).first()
            if token:
                db.delete(token)
                db.commit()
    return "ok"

@router.get("/alerts", response_model=List[schemas.Alert])
def alerts(user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    print(user.id)
    alerts = db.query(models.Alert).order_by(models.Alert.create_at).all()
    return alerts

@router.get("/rooms", response_model=List[schemas.Room])
def rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()