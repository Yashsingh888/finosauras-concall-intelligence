
from app.api.websocket import manager


async def send_notification(
    event_type: str,
    company_name: str,
    message: str
):
    notification = {
        "type": event_type,
        "company": company_name,
        "message": message
    }

    await manager.broadcast(notification)

    print("Notification sent:", notification)
