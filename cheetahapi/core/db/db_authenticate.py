import uuid

from cheetahapi.core.db.db_factory import DbFactory
from cheetahapi.core.db.model import Token, User

from sqlalchemy.orm import sessionmaker


class DbAuthenticate(object):

    """Database configuration"""
    db_config_dict = {}

    """Database sqlalchemy session"""
    session = None

    def __init__(self, db_config_dict={}):
        """
        Constructor. Loads database configuration and the sqlalchemy session
        :param db_config_dict: Database configuration as dictionary
        """
        self.set_db_config_dict(db_config_dict)
        self.load_db_session()

    def get_token(self, token_string):
        """
        Gets from database the information about a token from the token string
        :param token_string:
        :return: Token object
        """
        return self.session.query(Token).filter(Token.token == token_string).first()

    def get_user_from_db(self, username, password):
        """
        Gets from database the information about a user from username and password
        :param username:
        :param password:
        :return:
        """
        return self.session.query(User).filter(User.username == username, User.pw == password).first()

    def get_token_user_id(self, user_id):
        """
        Returns the token string for the user id
        :param user_id: Integer user identifier
        :return: String token. None in case there is no token for the user id
        """
        token_obj = self.session.query(Token).filter(Token.user_id == user_id).first()
        if token_obj:
            return token_obj.token
        return None

    def create_new_token(self, user_id):
        """
        Creates a new token in the database for the user id
        :param user_id: Integer user id
        :return: String token
        """
        token_string = uuid.uuid4().hex
        token = Token()
        token.user_id = user_id
        token.token = token_string
        self.session.add(token)
        self.session.commit()
        return token_string

    def load_db_session(self):
        """
        Loads the sqlalchemy session with the database
        :return:
        """
        engine = DbFactory().get_engine(self.get_db_config_dict())
        session_maker = sessionmaker(bind=engine)
        self.set_session(session_maker())

    def get_db_config_dict(self):
        return self.db_config_dict

    def set_db_config_dict(self, db_config_dict):
        self.db_config_dict = db_config_dict

    def set_session(self, session):
        self.session = session
