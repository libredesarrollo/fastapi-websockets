"""WebSocket Controller - Handles WebSocket lifecycle and communication."""
import json
from typing import List, Dict
from fastapi import WebSocket, WebSocketDisconnect
from src.entities.user import User
from src.interface_adapters.repositories.repository_interfaces import (
    RoomRepositoryInterface,
    AlertRepositoryInterface
)
from src.use_cases.alerts.create_alert import CreateAlertUseCase
from src.interface_adapters.presenters.schemas import Alert as AlertSchema


class ConnectionManager:
    """Manages active WebSocket connections."""
    
    def __init__(self):
        # In a real app with rooms, this should be Dict[int, List[WebSocket]]
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """Accept connection and add to registry."""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """Remove connection from registry."""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        """Send message to all active connections."""
        for connection in self.active_connections:
            try:
                await connection.send_text(message)
            except Exception:
                # Connection might be dead
                pass


# Global manager instance
manager = ConnectionManager()


async def websocket_handler(
    websocket: WebSocket,
    room_id: int,
    user: User,
    room_repo: RoomRepositoryInterface,
    alert_repo: AlertRepositoryInterface
):
    """
    Handles WebSocket communication for a specific room.
    """
    # Verify room exists
    room = room_repo.get_by_id(room_id)
    if not room:
        await websocket.accept()
        # Using 1008 Policy Violation for "Room not found"
        await websocket.close(code=1008)
        return

    await manager.connect(websocket)
    
    create_alert_use_case = CreateAlertUseCase(alert_repo)
    
    try:
        while True:
            data = await websocket.receive_text()
            try:
                data_json = json.loads(data)
                message_content = data_json.get("message", "")
                
                if message_content:
                    # Execute use case to save alert
                    alert_entity = create_alert_use_case.execute(
                        content=message_content,
                        user_id=user.id,
                        room_id=room_id
                    )
                    
                    # Prepare response using schema
                    alert_data = {
                        "id": alert_entity.id,
                        "content": alert_entity.content,
                        "created_at": alert_entity.created_at.isoformat() if alert_entity.created_at else None,
                        "user_id": alert_entity.user_id
                    }
                    
                    # Broadcast to all
                    await manager.broadcast(json.dumps(alert_data))
            except json.JSONDecodeError:
                # Ignore invalid JSON
                pass
                
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(json.dumps({"info": f"User {user.username} disconnected"}))
    except Exception as e:
        manager.disconnect(websocket)
        print(f"WS Error: {e}")
