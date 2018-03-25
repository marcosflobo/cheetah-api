from cheetahapi.core.db.db_factory import DbFactory
from cheetahapi.core.db.model import Token

from sqlalchemy.orm import sessionmaker


class DbAuthenticate(object):

    """Database configuration"""
    db_config_dict = {}

    """Database sqlalchemy session"""
    session = None

    def __init__(self, db_config_dict):
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

    def load_db_session(self):
        """
        Loads the sqlalchemy session with the database
        :return:
        """
        engine = DbFactory().get_engine(self.get_db_config_dict())
        session_maker = sessionmaker(bind = engine)
        self.set_session(session_maker())

    def get_db_config_dict(self):
        return self.db_config_dict

    def set_db_config_dict(self, db_config_dict):
        self.db_config_dict = db_config_dict

    def set_session(self, session):
        self.session = session