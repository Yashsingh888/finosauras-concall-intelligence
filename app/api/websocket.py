from fastapi import APIRouter, WebSocket, WebSocketDisconnect

websocket_router = APIRouter()


class ConnectionManager:

    def __init__(self):
        self.active_connections = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)
        print("New WebSocket client connected!")

    def disconnect(self, websocket: WebSocket):
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

        print("WebSocket client disconnected!")

    async def broadcast(self, message: dict):

        print("Broadcasting notification:", message)

        for connection in self.active_connections:
            try:
                await connection.send_json(message)
                print("Notification delivered successfully!")

            except Exception as error:
                print("Notification failed:", error)
                self.disconnect(connection)


manager = ConnectionManager()


@websocket_router.websocket("/ws/updates")
async def websocket_updates(websocket: WebSocket):

    await manager.connect(websocket)

    try:
        await websocket.send_json({
            "type": "connection",
            "status": "connected",
            "message": "Connected to Finosauras real-time updates!"
        })

        while True:
            await websocket.receive_text()

    except WebSocketDisconnect:
        manager.disconnect(websocket)