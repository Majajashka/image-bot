from app.core.constants.danbooru import ALLOWED_FILE_TYPES
from app.core.models.dto.api.danbooru import DanbooruPost
from app.core.utils.expections import InvalidDanbooruPostData


def validate_danbooru_post(post: DanbooruPost) -> DanbooruPost:
    if post.file.ext not in ALLOWED_FILE_TYPES:
        raise InvalidDanbooruPostData(f'Unallowed file ext. File ext: {post.file.ext}')
    if not post.file.url:
        raise InvalidDanbooruPostData(f'{post.__class__.__name__} missing file url. ID: {post.id}')
    return post
