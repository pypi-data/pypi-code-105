from fastack_cache.backends.base import BaseCache


class DummyCache(BaseCache):
    def __init__(self, serializer, **options):
        super().__init__(serializer, **options)

    def connect(self) -> "DummyCache":
        """
        Connect to the server.
        """

    def disconnect(self) -> None:
        """
        Disconnect from the server.
        """

    def get(self, key):
        pass

    def set(self, key, value, timeout=None):
        pass

    def delete(self, key):
        pass

    def clear(self):
        pass
