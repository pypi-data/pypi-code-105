"""Functions for quickly sending Markdown emails without manually using BaseEmail or its subclasses."""

from pathlib import Path
from smtplib import SMTP

from earendil.markdown_email import MarkdownEmail


def send_markdown_email(server: SMTP, sender: str, recipient: str, subject: str, body: str):
    """Sends a Markdown-formatted email message with the given parameters.

    Before calling, server must be ready for a send_message method invocation.

    Args:
        server: The SMTP server to send the email on.
        sender: The email address of the message's author.
        recipient: The intended recipient of the email.
        subject: The subject header of the email.
        body: The body of the email, written in Markdown.
    """
    email = MarkdownEmail(sender, subject, body)
    message = email.get_message(recipient)

    server.send_message(message)


def send_markdown_email_from_file(server: SMTP, sender: str, recipient: str, subject: str, file_name: Path):
    """Sends a Markdown-formatted email message loaded from a file with the given parameters.

    Before calling, server must be ready for a send_message method invocation.

    Args:
        server: The SMTP server to send the email on.
        sender: The email address of the message's author.
        recipient: The intended recipient of the email.
        subject: The subject header of the email.
        file_name: The path to the file containing the message to send.
    """
    with file_name.open() as file:
        body = file.read()
    send_markdown_email(server, sender, recipient, subject, body)
