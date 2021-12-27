"""A Markdown-based HTML email API."""

from .base_email import BaseEmail
from .mailer import send_markdown_email, send_markdown_email_from_file
from .markdown_email import MarkdownEmail
