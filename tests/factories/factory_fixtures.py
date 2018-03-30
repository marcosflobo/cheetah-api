import factory

from sqlalchemy import Integer, String, DateTime, Unicode, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker


engine = create_engine('sqlite://')
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()

# ATTENTION: This import must stay here, other wise Base class will not know about the classes that inherit from it in
# cheetahapi.core.db.model file
from cheetahapi.core.db.model import *

Base.metadata.create_all(engine)


class UserFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = User
        sqlalchemy_session = session   # the SQLAlchemy session object

    id = factory.Sequence(lambda n: n)
    profile_id = factory.Sequence(lambda n: n)
    country_id = factory.Sequence(lambda n: n)
    name = factory.Sequence(lambda n: u'John %d' % n)
    username = factory.Sequence(lambda n: u'john-%d' % n)
    pw = '1234'
    email = factory.Sequence(lambda n: u'john-%d@domain.com' % n)


class TokenFactory(factory.alchemy.SQLAlchemyModelFactory):
    class Meta:
        model = Token
        sqlalchemy_session = session   # the SQLAlchemy session object
    id = factory.Sequence(lambda n: n)
    user_id = factory.Sequence(lambda n: n)
    token = factory.Sequence(lambda n: u'token-%d' % n)