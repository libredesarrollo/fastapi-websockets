from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, Depends
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from src.interface_adapters.controllers import (
    auth_controller, 
    alerts_controller, 
    rooms_controller,
    websocket_controller
)
from src.frameworks_drivers.db.connection import engine
from src.frameworks_drivers.db.orm_models import Base
from src.frameworks_drivers.http.dependencies import (
    get_user_by_token_query,
    get_room_repository,
    get_alert_repository
)
from src.entities.user import User

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize FastAPI app
app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Setup templates
templates = Jinja2Templates(directory="templates/")

# Include routers with /api prefix
app.include_router(auth_controller.router, prefix="/api")
app.include_router(alerts_controller.router, prefix="/api")
app.include_router(rooms_controller.router, prefix="/api")


@app.get('/')
def form(request: Request):
    """Render WebSocket chat page."""
    return templates.TemplateResponse(request=request, name='ws/chat.html')


@app.websocket("/ws/alert/room/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket, 
    room_id: int, 
    user: User = Depends(get_user_by_token_query),
    room_repo=Depends(get_room_repository),
    alert_repo=Depends(get_alert_repository)
):
    """
    WebSocket endpoint refactored to Clean Architecture.
    Delegates logic to the interface adapter.
    """
    await websocket_controller.websocket_handler(
        websocket=websocket,
        room_id=room_id,
        user=user,
        room_repo=room_repo,
        alert_repo=alert_repo
    )
        
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication."""
    await websocket.accept()
    try:
        while True:
            print('connection open')
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        # --- EVENTO: AL DESCONECTARSE (Cierre limpio) ---
        print("El cliente cerró la conexión")
        
    except Exception as e:
        # Captura otros errores inesperados
        print(f"Error inesperado: {e}")
        
    finally:
        # --- LÓGICA FINAL ---
        # Este bloque se ejecuta siempre, ideal para limpieza de recursos
        print("Limpieza de conexión finalizada")