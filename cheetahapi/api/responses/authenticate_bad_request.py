from cheetahapi.api.responses.base_response import BaseResponse


class AuthenticateBadRequest(BaseResponse):
    """
    Bad Request response
    """
    status = 500
    name = 'Bad Request'
