class ApiError(Exception):
    def __init__(
            self,
            response_status: int = None,
            api_name: str = None,
            url: str = None,
            description: str = None
    ):
        self.api_name = api_name
        self.response_status = response_status
        self.url = url
        self.description = description

    def __str__(self):
        return (f'\n  API name: {self.api_name}\n'
                f'  Code status: {self.response_status}\n'
                f'  Description: {self.description}'
                f'  Url: {self.url}')

