from cheetahapi.api.responses.base_response import BaseResponse


class Success(BaseResponse):
    status = 200
    name = 'Success'
