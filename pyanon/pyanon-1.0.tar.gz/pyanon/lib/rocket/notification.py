from .rocketevent import RocketEvent
from .notificationpayload import NotificationPayload

class Notification(RocketEvent):
    def __init__(self,
                msg: str,
                collection: str,
                id: str,
                title: str,
                text: str,
                payload: NotificationPayload) -> None:
        self.msg: str = msg
        self.collection: str = collection
        self.id: str = id
        self.title: str = title
        self.text: str = text
        self.payload: NotificationPayload = payload