FREE_TAGS = [
    'rating',
    'status',
    'is',
    'age',
    'date',
    'id',
    'limit',
    'score',
    'downvotes',
    'favcount',
    'width',
    'height',
    'ratio',
    'mpixels',
    'filesize',
    'filetype',
    'duration',
    'md5',
    'pixiv_id',
    'pixiv',
    'parent',
    'child',
    'upvote',
    'embedded',
    'tagcount'
]

BASIC_TAGS = ['is:sfw']  # Tags that will be applied to every request
ALLOWED_FILE_TYPES = ['png', 'jpg', 'webm']

# Default settings for new users
USER_DEFAULT_TAGS: list = []
USER_DEFAULT_COUNT: int = 1

# Limit for posts at one time
MAX_USER_POST_COUNT = 10
MAX_ADMIN_POST_COUNT = 100
