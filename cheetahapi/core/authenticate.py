from datetime import datetime

from cheetahapi.core.db.db_authenticate import DbAuthenticate


class Authenticate(object):
    """
    Number of days that a token is valid. In the future, this value will come from config file
    """
    token_days_valid = 5

    db_manager = None

    db_config_dict = {}

    def __init__(self):
        self.load_db_manager()

    def authenticate(self, user, password):
        """
        Authenticates a user using username and password
        :param user: Username
        :param password: Password for the username
        :return: Token object with crated date and user_id
        """
        user = self.get_user_from_db(user, password)
        if user is None:
            raise Exception("User '{0}' not found using password".format(user))
        token = self.get_token_user_id(user["id"])
        if token is None or not self.is_valid_token(token["token"]):
            token = self.create_new_token(user["id"])
        return token

    def get_user_from_db(self, user, password):
        # TODO
        pass

    def create_new_token(self, param):
        # TODO
        pass

    def get_token_user_id(self, param):
        # TODO
        """

        :param param:
        :return:
        """
        pass

    def is_valid_token(self, token):
        """
        Checks if the token string is valid, which means the creation date does not exceed the amount of days allowed
        by configuration file
        :param token: Token string
        :return: True if the token string is valid, False in other case
        """
        token_obj = self.get_token_from_db(token)
        return self.token_date_not_expired(token_obj.created)

    def token_date_not_expired(self, token_date_creation):
        """
        Checks the token date creation does not exceed the number of days allowed
        :param token_date_creation: Date as string
        :return: True if the date does NOT exceed the number of days from today, False in other case
        """
        datetime_object = datetime.strptime(token_date_creation, "%Y-%m-%d")
        return (self.get_today_date() - datetime_object).days <= self.get_token_days_valid()

    def get_today_date(self):
        return datetime.today()

    def get_token_from_db(self, token):
        """
        Returns the token information for token string
        :param token: Token string
        :return: Token object from model.py
        """
        db_manager = DbAuthenticate(self.get_db_config_dict())
        return db_manager.get_token(token)

    def get_token_days_valid(self):
        return self.token_days_valid

    def set_token_days_valid(self, num_days):
        self.token_days_valid = num_days

    def load_db_manager(self):
        self.db_manager = DbAuthenticate(self.get_db_config_dict())

    def set_db_config_dict(self, db_config_dict):
        self.db_config_dict = db_config_dict

    def get_db_config_dict(self):
        return self.db_config_dict
