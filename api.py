from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query
import json
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from pydantic import BaseModel

from rest_api import router as api_router

from typing import List
import models, schemas
from database import SessionLocal

templates = Jinja2Templates(directory="templates/")

# Define los orígenes permitidos (puedes usar ["*"] para permitir todo, 
# pero no es recomendable en producción)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173", # Puerto común de Vue/Vite
]

def create_rooms():
    db = SessionLocal()
    try:
        for name in ["room 1", "room 2"]:
            if not db.query(models.Room).filter(models.Room.name == name).first():
                db.add(models.Room(name=name))
        db.commit()
    finally:
        db.close()

@asynccontextmanager
async def lifespan(app: FastAPI):
    print('****START')
    create_rooms()
    yield
    print('****END')

app = FastAPI(lifespan=lifespan)
router = APIRouter()

app.include_router(api_router, prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# uvicorn api_multiple:app --reload
# 

@app.get('/')
def form(request: Request):
    return templates.TemplateResponse(request=request, name='ws/chat.html')

# class LoginRequest(BaseModel):
#     username: str
#     password: str

# @app.post("/api/login")
# async def login(data: LoginRequest):
#     # Validación simple local (hardcoded)
#     if data.username == "admin" and data.password == "admin":
#         return {"token": "token-secreto"}
    
#     raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Credenciales inválidas")

class ConnectionManager:
    def __init__(self):
        # Lista para almacenar las conexiones activas
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    # async def send_personal_message(self, message: str, websocket: WebSocket):
    #     await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

manager = ConnectionManager()

# async def get_token(token: str = Query(...)): # ... REQUERIDO
#     # Validación simple de token
#     if token != "token-secreto":
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail="Token inválido"
#         )
#     return token

async def get_user_by_token(token: str = Query(...)):
    db = SessionLocal()
    try:
        # El token viene como "Token_abc123..."
        if "_" not in token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Formato de token inválido")
        
        _, key = token.split("_")
        db_token = db.query(models.Token).filter(models.Token.key == key).first()
        
        if not db_token:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token inválido")
        
        return db_token.user
    finally:
        db.close()


# para conectar al WebSocket, el cliente 
# deberá incluir el parámetro token: ws://localhost:8000/ws/123?token=token-secreto

@app.websocket("/ws/alert/room/{room_id}")
async def websocket_endpoint(websocket: WebSocket, room_id: int, user: models.User = Depends(get_user_by_token)):
    db = SessionLocal()
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        
        await websocket.accept()
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        db.close()
        return

    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            data_json = json.loads(data)
            message = data_json.get("message", "")
            if message:
                alert = models.Alert(content=message, user_id=user.id, room_id=room_id)
                db.add(alert)
                db.commit()
                # db.refresh(alert)
                # await manager.broadcast(f"Cliente #{room_id} dice: {data}")
                # Convertir el objeto SQLAlchemy a un esquema Pydantic y luego a dict/json
                alert_data = schemas.Alert.model_validate(alert).model_dump()
                # Convertir datetime a string para que sea serializable por json
                alert_data["created_at"] = alert_data["created_at"].isoformat()
                
                await manager.broadcast(json.dumps(alert_data))
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Cliente #{room_id} se ha desconectado")
        
# @app.websocket("/ws/{client_id}")
# async def websocket_endpoint(websocket: WebSocket, client_id: int, token: str = Depends(get_token)):
#     await manager.connect(websocket)
#     try:
#         while True:
#             data = await websocket.receive_text()
#             await manager.broadcast(f"Cliente #{client_id} dice: {data}")
#     except WebSocketDisconnect:
#         manager.disconnect(websocket)
#         await manager.broadcast(f"Cliente #{client_id} se ha desconectado")