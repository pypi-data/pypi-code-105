"""Declares standard exceptions."""
from unimatrix.ext.model import CanonicalException


class Backoff(CanonicalException):
    """Raised when a backoff is enforced to a request"""
    http_status_code = 429
    code = 'BACKOFF'

    def __init__(self, seconds: int):
        """Initialize a new :class:`Backoff` instance."""
        self.seconds = seconds
        super().__init__(
            message="Requests to this resource are being rate limited.",
            hint="Respect the Retry-After header.",
        )

    def get_http_headers(self) -> dict:
        return {
            **super().get_http_headers(),
            'Retry-After': str(self.seconds)
        }
