import asyncio
from typing import Optional, Collection

from app.core.external_service.api.base import BaseExternalAPI
from app.core.models.dto.api.danbooru import DanbooruPost


class DanbooruAPI(BaseExternalAPI):
    def __init__(self):
        super().__init__(url="https://danbooru.donmai.us")

    async def image(self, tags: Optional[Collection[str]]):
        params = {
            'tags': ','.join(tags)
        }
        data = await self.get(
            endpoint='posts/random.json',
            params=params
        )
        return DanbooruPost.from_dict(data=data)



