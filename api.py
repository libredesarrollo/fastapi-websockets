from fastapi import FastAPI, APIRouter, Request, WebSocket

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
    while True:
        print('Hola')
        data = await websocket.receive_text()
        await websocket.send_text(f"Message text was: {data}")