"""Abstract base class for email composers."""

from abc import ABCMeta, abstractmethod
from email.message import EmailMessage


class BaseEmail(metaclass=ABCMeta):
    """Generic email object that can generate an EmailMessage based on its contents."""

    def __init__(self, sender: str, subject: str):
        self.sender = sender
        self.subject = subject

    @abstractmethod
    def get_message(self, recipient: str) -> EmailMessage:
        """Generate a message that can be sent using the SMTP.send_message method.

        Args:
            recipient: Address of the email's intended recipient.
        """
        pass
