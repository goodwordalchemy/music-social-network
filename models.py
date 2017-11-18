from sqlalchemy import Column, Integer, ForeignKey, create_engine
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# Database and Models
Base = declarative_base()

# Nodes
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    follows_tracks = relationship('TrackFollow', back_populates='user')

    # relationships
    follows_users = relationship('UserFollow', back_populates='follower')
    followed_by_users = relationship('UserFollow', back_populates='followed')


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)

    # relationships
    followed_by_users = relationship('TrackFollow', back_populates='track')



# Relationships and Events
class TrackFollow(Base):
    __tablename__ = 'track_follow'

    # foreign keys
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    track_id = Column(Integer, ForeignKey('track.id'), primary_key=True)

    # relationships
    user = relationship('User', back_populates='follows_tracks')
    track = relationship('Track', back_populates='followed_by_users')



class UserFollow(Base):
    __tablename__ = 'user_follow'

    id = Column(Integer, primary_key=True)

    # foreign keys
    follower_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # relationships
    follower = relationship('User', back_populates='follows_users')
    followed = relationship('User', back_populates='followed_by_user')
