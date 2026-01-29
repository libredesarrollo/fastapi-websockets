from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketDisconnect, Depends, HTTPException, status, Query

from fastapi.templating import Jinja2Templates

from fastapi.middleware.cors import CORSMiddleware

templates = Jinja2Templates(directory="templates/")

# Define los orígenes permitidos (puedes usar ["*"] para permitir todo, 
# pero no es recomendable en producción)
origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
    "http://localhost:5173", # Puerto común de Vue/Vite
]


app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# uvicorn api:app --reload
# 

router = APIRouter()

@app.get('/')
def form(request: Request):
    return templates.TemplateResponse(request=request, name='ws/chat.html')

from typing import List

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

async def get_token(token: str = Query(...)): # ... REQUERIDO
    # Validación simple de token
    if token != "token-secreto":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Token inválido"
        )
    return token

# para conectar al WebSocket, el cliente 
# deberá incluir el parámetro token: ws://localhost:8000/ws/123?token=token-secreto
@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: int, token: str = Depends(get_token)):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            await manager.broadcast(f"Cliente #{client_id} dice: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Cliente #{client_id} se ha desconectado")