"""Functionality for generating Markdown-formatted emails with one recipient."""

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from markdown import markdown as markdown_to_html

from earendil.base_email import BaseEmail
from earendil.plaintext_renderer import markdown_to_plaintext


def render_plain(text: str) -> str:
    return markdown_to_plaintext(text)


def render_html(text: str) -> str:
    return markdown_to_html(text)


class MarkdownEmail(BaseEmail):
    """An email message that is generated from Markdown text."""

    def __init__(self, sender: str, subject: str, body: str):
        super().__init__(sender, subject)

        self.markdown_body = body
        self.plain_text = render_plain(body)
        self.plain_mime = MIMEText(self.plain_text, "plain")
        self.html_text = render_html(body)
        self.html_mime = MIMEText(self.html_text, "html")

    def get_message(self, recipient: str) -> MIMEMultipart:
        mime = MIMEMultipart("alternative")
        mime["From"] = self.sender
        mime["To"] = recipient
        mime["Subject"] = self.subject

        mime.attach(self.plain_mime)
        mime.attach(self.html_mime)

        return mime
