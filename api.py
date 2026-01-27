from fastapi import FastAPI, APIRouter, Request, WebSocket, WebSocketDisconnect

from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="templates/")


# uvicorn api:app --reload
# 

app = FastAPI()
router = APIRouter()

@app.get('/')
def form(request: Request):
    return templates.TemplateResponse(request=request, name='ws/chat.html')

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    try:
        while True:
            print('conection open')
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