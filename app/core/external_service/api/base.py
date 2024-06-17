from typing import Type
from aiohttp import ClientSession, ClientResponse

from app.core.utils.expections import ApiError


class BaseExternalAPI:
    def __init__(self, url: str, error: Type[ApiError] = ApiError):
        self.base_url = url
        self.session = ClientSession()

        if not issubclass(error, ApiError):
            raise ValueError(f'{error} is not subclass of ApiError')
        self.error = error

    async def _handle_error(self, response: ClientResponse, description: str = None) -> None:
        """
         Handles API error responses.

         :param response: The HTTP response object.
         :type response: aiohttp.ClientResponse
         :param description: Error description from response
         :type description: str

         :raises ApiError: If an error occurs during the API request.
        """
        if not description:
            description = 'Unknown error'

        if response.status >= 400:
            raise self.error(
                api_name=self.__class__.__name__,
                response=response,
                url=response.url.__str__(),
                description=description
            )

    async def fetch(self, endpoint: str, method='GET', params=None, data=None) -> dict:
        url = f"{self.base_url}/{endpoint}"
        async with self.session.request(method, url, params=params, data=data) as response:
            data = await response.json()
            await self._handle_error(response)
            return data

    async def get(self, endpoint: str, params=None):
        return await self.fetch(endpoint, 'GET', params=params)

    async def post(self, endpoint: str, data=None):
        return await self.fetch(endpoint, 'POST', data=data)

    async def put(self, endpoint: str, data=None):
        return await self.fetch(endpoint, 'PUT', data=data)

    async def session_close(self) -> None:
        await self.session.close()
