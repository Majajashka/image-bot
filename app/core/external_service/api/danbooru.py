from typing import Optional, Collection
from aiohttp import ClientResponse

from app.core.external_service.api.base import BaseRequests
from app.core.models.dto.api.danbooru import DanbooruPost, DanbooruTags
from app.core.utils.expections import DanbooruApiError


class DanbooruAPI(BaseRequests):
    def __init__(self):
        super().__init__(url="https://danbooru.donmai.us", error=DanbooruApiError)

    async def _handle_error(self, response: ClientResponse, description: str = None) -> None:
        data: dict = await response.json()
        description = data.get('message')
        await super()._handle_error(response, description)

    async def random_image(self, tags: Optional[Collection[str]] = None):
        params = {
            'tags': ','.join(tags or [])
        }
        data = await self._get(
            endpoint='posts/random.json',
            params=params
        )
        return DanbooruPost.from_dict(data=data)

    async def search_tags(
            self,
            tag: Optional[str],
            regex: str = '.*{}.*',
            order: str = 'count',
            hide_empty: bool = True
    ) -> list[DanbooruTags]:
        params = {
            'search[name_regex]': regex.format(tag or ''),
            'search[hide_empty]': hide_empty,
            'search[order]': order
        }
        data = await self._get(
            endpoint='tags.json',
            params=params
        )
        return [DanbooruTags.from_dict(tags) for tags in data]
