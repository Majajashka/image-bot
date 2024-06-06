from typing import Collection, Optional

from app.core.models.dto.api.danbooru import DanbooruPost
from app.core.external_service.api.danbooru import DanbooruAPI


async def get_danbooru_post(tags: Optional[Collection[str]] = None) -> DanbooruPost:
    danbooru = DanbooruAPI()
    post = await danbooru.image(tags)
    await danbooru.session_close()
    return post
