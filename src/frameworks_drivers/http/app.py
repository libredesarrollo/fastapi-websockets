"""FastAPI application initialization."""
from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from fastapi.templating import Jinja2Templates
from src.interface_adapters.controllers import auth_controller, alerts_controller, rooms_controller
from src.frameworks_drivers.db.connection import engine
from src.frameworks_drivers.db.orm_models import Base

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
