
from httpx import AsyncClient

from cenzopapa.mixins import ListMixin, RetrieveMixin, create_image


class ResourceClient:
    endpoint = None

    def __init__(self, api_url):
        self.api_url = api_url

    async def generate_url(self, pk=None, page=None, action=None):
        try:
            api_endpoint = "".join([self.api_url, self.endpoint])
            if pk and action:
                return "".join([api_endpoint, str(pk), "/", str(action), "/"])
            if pk:
                return "".join([api_endpoint, str(pk), "/"])
            if page:
                return f"{api_endpoint}?page={page}"
            if action:
                return "".join([api_endpoint, action, "/"])

            return api_endpoint
        except TypeError:
            print("Wystapil problem")

class ImageResource(
    ResourceClient,
    RetrieveMixin,
    ListMixin,

):
    endpoint = "/images/"

    async def random(self):
        async with AsyncClient() as client:
            url = await self.generate_url(action="random")
            response = await client.get(url)
            return await create_image(response)
