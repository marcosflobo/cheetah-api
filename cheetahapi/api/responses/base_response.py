class BaseResponse(object):
    status = 0
    message = ''
    name = ''
    extra_fields_dict = {}

    def __init__(self, message=''):
        self.set_message(message)

    def to_json(self):
        ret = {
            'response': {
                'status': self.status,
                'message': self.message,
            }
        }
        ret = dict(ret['response'].items() + self.get_extra_fields().items())
        return ret

    def add_extra_fields(self, data_dict):
        self.extra_fields_dict = data_dict

    def get_extra_fields(self):
        return self.extra_fields_dict

    def set_status(self, status):
        self.status = status

    def set_message(self, message):
        self.message = self.name + ': ' + message
