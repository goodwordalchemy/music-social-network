from sqlalchemy import Column, Integer, ForeignKey, create_engine, Table, String
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

from sqlalchemy import create_engine
from sqlalchemy.orm import backref, sessionmaker

engine = create_engine('sqlite:///:memory:', echo=True)

Session = sessionmaker(bind=engine)


def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()

    if instance:
        return instance
    else:
        return model(**kwargs)


# Database and Models
Base = declarative_base()

# Association Tables
track_artist_association = Table('track_artist', Base.metadata,
    Column('track_sid', String, ForeignKey('track.sid')),
    Column('artist_sid', String, ForeignKey('artist.sid'))
)

album_artist_association = Table('album_artist', Base.metadata,
    Column('album_sid', String, ForeignKey('album.sid')),
    Column('artist_sid', String, ForeignKey('artist.sid'))
)


# Nodes
class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)

    follows_tracks = relationship('TrackFollow', back_populates='user')

    # relationships
    follows_users = relationship('UserFollow',
        primaryjoin=lambda : (id==UserFollow.follower_id),  # primaryjoin='id == user_follow.follower_id',
        backref='follower'
    )
    followed_by_users = relationship('UserFollow',
        primaryjoin=lambda : (id==UserFollow.followed_id),  # primaryjoin='id == user_follow.followed_id',
        backref='followed'
    )


class UserFollow(Base):
    __tablename__ = 'user_follow'

    id = Column(Integer, primary_key=True)

    # foreign keys
    follower_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # relationships
    # follower = relationship('User',
    #     primaryjoin=lambda : (follower_id == User.id),
    #     backref='follows_users'
    # )
    # followed = relationship('User',
    #     primaryjoin= lambda : (followed_id == User.id),
    #     backref='followed_by_user'
    # )


class Track(Base):
    __tablename__ = 'track'

    id = Column(Integer, primary_key=True)

    sid = Column(String)
    name = Column(String)
    popularity = Column(Integer)
    uri = Column(String)
    href = Column(String)

    # foreign keys
    album_sid = Column(String, ForeignKey('album.sid'))

    # relationships
    album = relationship('Album', back_populates='tracks')
    artists = relationship(
        'Artist',
        secondary=track_artist_association,
        back_populates='tracks'
    )
    followed_by_users = relationship('TrackFollow', back_populates='track')


class Album(Base):
    __tablename__ = 'album'

    id = Column(Integer, primary_key=True)

    sid = Column(String)
    name = Column(String)
    uri = Column(String)

    # relationships
    tracks = relationship('Track', back_populates='album')
    artists = relationship(
        'Artist',
        secondary=album_artist_association,
        back_populates='albums'
    )


class Artist(Base):
    __tablename__ = 'artist'

    id = Column(Integer, primary_key=True)

    sid = Column(String)
    name = Column(String)
    uri = Column(String)

    # relationships
    tracks = relationship(
        'Track',
        secondary=track_artist_association,
        back_populates='artists'
    )
    albums = relationship(
        'Album',
        secondary=album_artist_association,
        back_populates='artists'
    )


# Assocation Classes
class TrackFollow(Base):
    __tablename__ = 'track_follow'

    # foreign keys
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    track_id = Column(Integer, ForeignKey('track.id'), primary_key=True)

    # relationships
    user = relationship('User', back_populates='follows_tracks')
    track = relationship('Track', back_populates='followed_by_users')



