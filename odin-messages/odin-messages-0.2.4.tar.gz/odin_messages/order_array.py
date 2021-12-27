from typing import List

from odin_messages.base import BaseEventMessageAssay
from odin_messages.orders import NewLimitOrderMessage, UpdateLimitOrderMessage


class NewLimitOrdersArray(BaseEventMessageAssay):
    messages: List[NewLimitOrderMessage]

class UpdateLimitOrdersArray(BaseEventMessageAssay):
    messages: List[UpdateLimitOrderMessage]
