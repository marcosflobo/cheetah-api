from cheetahapi.api.responses.authenticate_bad_request import AuthenticateBadRequest
from cheetahapi.api.responses.success import Success
from cheetahapi.api.responses.unauthorized import Unauthorized
from cheetahapi.core.authenticate import Authenticate


class Dispacher(object):

    config = None

    def __init__(self, config=None):
        self.set_config(config)

    def authenticate(self, data_json):
        if 'authenticate' not in data_json:
            return AuthenticateBadRequest('\'authenticate\' key is missing')
        if 'username' not in data_json['authenticate']:
            return AuthenticateBadRequest('\'username\' key is missing in \'authenticate\' dict')
        if 'password' not in data_json['authenticate']:
            return AuthenticateBadRequest('\'password\' key is missing in \'authenticate\' dict')

        try:
            auth_obj = Authenticate(self.get_config().read_database())
        except Exception as ex:
            return AuthenticateBadRequest(ex.message)
        try:
            token = auth_obj.authenticate(data_json['authenticate']['username'],
                                          data_json['authenticate']['password'])
            response = Success('Authenticated')
            response.add_extra_fields({'token': token})
            return response
        except Exception as ex:
            return Unauthorized(ex.message)

    def get_config(self):
        return self.config

    def set_config(self, config):
        self.config = config
