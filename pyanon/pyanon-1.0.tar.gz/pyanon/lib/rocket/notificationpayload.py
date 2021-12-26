from .notificationsender import NotificationSender
from .notificationmessage import NotificationMessage

class NotificationPayload:
    def __init__(self, 
                id: str,
                roomId: str,
                sender: NotificationSender,
                type: str,
                message: NotificationMessage) -> None:
        self.id: str = id
        self.roomId: str = roomId
        self.sender: NotificationSender = sender
        self.type: str = type
        self.message: NotificationMessage = message