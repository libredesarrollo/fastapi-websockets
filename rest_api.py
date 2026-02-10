from fastapi import APIRouter, Depends, HTTPException, status, Header
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from typing import List, Optional
# from passlib.context import CryptContext

import models
import schemas
from database import SessionLocal, engine

# Crear tablas en la BD (para propósitos de este ejemplo)
models.Base.metadata.create_all(bind=engine)

router = APIRouter()

# Configuración de hashing de contraseñas
# pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto", bcrypt__ident="2b")

# def verify_password(plain_password, hashed_password):
#     return pwd_context.verify(plain_password, hashed_password)

# def get_password_hash(password):
#     return pwd_context.hash(password)

import bcrypt

def get_password_hash(password: str) -> str:
    # Convertimos la contraseña a bytes
    pwd_bytes = password.encode('utf-8')
    # Generamos el salt y el hash
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt)
    # Retornamos como string para guardar en la BD
    return hashed_password.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    password_byte_enc = plain_password.encode('utf-8')
    hashed_password_enc = hashed_password.encode('utf-8')
    return bcrypt.checkpw(password_byte_enc, hashed_password_enc)

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
        
    return {"token": f"Token_{token.key}"}

@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: schemas.RegisterRequest, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.username == request.username).first()
    if user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    
    hashed_password = get_password_hash(request.password)
    new_user = models.User(username=request.username, password=hashed_password)
    db.add(new_user)
    db.commit()
    return {"message": "User created successfully"}

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
def alerts(room_id: Optional[int] = None, user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    query = db.query(models.Alert)
    if room_id:
        query = query.filter(models.Alert.room_id == room_id)
    return query.order_by(models.Alert.created_at).all()

@router.get("/rooms", response_model=List[schemas.Room])
def rooms(db: Session = Depends(get_db)):
    return db.query(models.Room).all()