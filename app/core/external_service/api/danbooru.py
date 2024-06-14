from typing import Optional, Collection
from aiohttp import ClientResponse

from app.core.external_service.api.base import BaseExternalAPI
from app.core.models.dto.api.danbooru import DanbooruPost
from app.core.utils.expections import DanbooruApiError


class DanbooruAPI(BaseExternalAPI):
    def __init__(self):
        super().__init__(url="https://danbooru.donmai.us", error=DanbooruApiError)

    async def _handle_error(self, response: ClientResponse, description: str = None) -> None:
        data: dict = await response.json()
        description = data.get('message')
        await super()._handle_error(response, description)

    async def image(self, tags: Optional[Collection[str]] = None):
        params = {
            'tags': ','.join(tags or [])
        }
        data = await self.get(
            endpoint='posts/random.json',
            params=params
        )
        return DanbooruPost.from_dict(data=data)

