from cheetahapi.api.responses.base_response import BaseResponse


class Unauthorized(BaseResponse):
    """
    Unauthorized response
    """
    status = 401
    name = 'Unauthorized'
