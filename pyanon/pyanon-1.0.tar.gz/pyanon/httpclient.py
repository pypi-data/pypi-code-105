from httpx import AsyncClient, Response, Timeout
from ujson import dumps
from .pkg.utils.headers import HeadersUtils
from .pkg.objects.response import APIResponse
from .pkg.objects.rocketresponse import RocketResponse

class HttpClient(HeadersUtils):
    def __init__(self) -> None:
        super().__init__()
        self.api: str = "https://18.159.2.59/"
        self.rocket: str = "https://3.70.82.211/api/v1/"
        self.timeout: Timeout = Timeout(150, connect = 150)

    async def get(self, endpoint: str) -> APIResponse:
        async with AsyncClient(base_url = self.api, verify = False, timeout = self.timeout) as http:
            response: Response = await http.get(endpoint, headers = self.getHeaders())
        return APIResponse(response.status_code, response.text)

    async def post(self, endpoint: str, data: object) -> APIResponse:
        if isinstance(data, dict):
            data = dumps(data)
        async with AsyncClient(base_url = self.api, verify = False, timeout = self.timeout) as http:
            response: Response = await http.post(endpoint, headers = self.getHeaders(), data = data)
        return APIResponse(response.status_code, response.text)
    
    async def rocketGet(self, endpoint: str) -> RocketResponse:
        async with AsyncClient(base_url = self.rocket, verify = False, timeout = self.timeout) as http:
            response: Response = await http.get(endpoint, headers = self.getRocketHeaders())
        return RocketResponse(response.status_code, response.text)
    
    async def rocketPost(self, endpoint: str, data: object) -> RocketResponse:
        if isinstance(data, dict):
            data = dumps(data)
        async with AsyncClient(base_url = self.rocket, verify = False, timeout = self.timeout) as http:
            response: Response = await http.post(endpoint, headers = self.getRocketHeaders(), data = data)
        return RocketResponse(response.status_code, response.text)