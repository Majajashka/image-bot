import json
from typing import Optional, Collection

from aiohttp import ClientResponse


class ApiError(Exception):
    def __init__(
            self,
            response: ClientResponse = None,
            api_name: str = None,
            url: str = None,
            description: str = None
    ):
        self.api_name = api_name
        self.response = response
        self.url = url
        self.description = description

    def __str__(self):
        return (f'API name: {self.api_name}\n'
                f'Code status: {self.response.status}\n'
                f'Description: {self.description}\n'
                f'Url: {self.url}')

    @property
    def response_status(self):
        return self.response.status

class DanbooruApiError(ApiError):
    def __init__(
            self,
            response_status: int = None,
            api_name: str = None,
            url: str = None,
            description: str = None
    ):
        super().__init__(response_status, api_name, url, description)


class UserArgumentError(ValueError):
    def __init__(self, message: str, user_args: str = None):
        super().__init__(message)
        self.user_args = user_args

    def __str__(self):
        return self.user_args

    def __repr__(self):
        return f'{self.__class__.__name__}({self})'


class InvalidRequestCount(UserArgumentError):
    def __init__(
            self,
            message: str,
            count: int,
            max_count: int,
            user_args: str = None
    ):
        super().__init__(message=message, user_args=user_args)
        self.count = count
        self.max_count = max_count

    def __str__(self):
        return f'{self.count=}. {self.max_count}'

class InvalidTagsCount(UserArgumentError):
    def __init__(
            self,
            message: str,
            count: int,
            tags: Optional[Collection[str]] = None,
            user_args: str = None
    ):
        super().__init__(message=message, user_args=user_args)
        self.count = count
        self.tags = tags

    def __str__(self):
        return f'{self.tags=}. {self.count}'