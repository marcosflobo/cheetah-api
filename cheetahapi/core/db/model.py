"""
Datamodel for sqlalchemy
"""
from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, backref

Base = declarative_base()


class Team(Base):
    """
    Represents team table
    """
    __tablename__ = 'team'
    id = Column(Integer, primary_key=True)
    users = relationship("User", secondary="userteam")
    name = Column(String(255), nullable=False, unique=True)
    created = Column(DateTime)
    modified = Column(DateTime)


class Token(Base):
    """
    Represents token table
    """
    __tablename__ = 'token'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    token = Column(String(64), nullable=False, unique=True)
    created = Column(DateTime)
    modified = Column(DateTime)


class User(Base):
    """
    Represents user table and its relationships
    """
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey('profile.id'), nullable=False)
    country_id = Column(Integer, ForeignKey('country.id'), nullable=False)
    teams = relationship("Team", secondary="userteam")
    tokens = relationship(Token, collection_class=set)
    name = Column(String(255), nullable=False)
    username = Column(String(255), nullable=False, unique=True)
    pw = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    created = Column(DateTime)
    modified = Column(DateTime)


class Country(Base):
    """
    Represents country table
    """
    __tablename__ = 'country'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False, unique=True)
    users = relationship(User, collection_class=set)
    created = Column(DateTime)
    modified = Column(DateTime)


class Profile(Base):
    """
    Represents country table
    """
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    users = relationship(User, collection_class=set)
    created = Column(DateTime)
    modified = Column(DateTime)


class Userteam(Base):
    """
    Represents the many-to-many relationship between users and teams
    """
    __tablename__ = 'userteam'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('user.id'), nullable=False)
    team_id = Column(Integer, ForeignKey('team.id'), nullable=False)

    user = relationship(User, backref=backref("userteam", cascade="all, delete-orphan"))
    team = relationship(Team, backref=backref("userteam", cascade="all, delete-orphan"))
