import os

import sqlalchemy
from sqlalchemy import Column, Integer, ForeignKey, create_engine, Table, String
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import backref, sessionmaker, relationship


basedir = os.path.abspath(os.path.dirname(__file__))

db_url = 'sqlite:///{}/data/test_database.db'.format(basedir)

Base = declarative_base()


def row2dict(row):
    return dict((col, getattr(row, col)) for col in row.__table__.columns.keys())


def create_tables(engine):
    Base.metadata.create_all(engine)


def db_connect():
    return create_engine(db_url)


def get_session(engine=None):
    if engine is None:
        engine = db_connect()

    Session = sessionmaker(bind=engine)

    return Session()


def reset():
    engine = db_connect()
    meta = sqlalchemy.MetaData(engine)
    meta.reflect()
    meta.drop_all()
    create_tables(engine)



def get_or_create(session, model, **kwargs):
    instance = session.query(model).filter_by(**kwargs).first()

    if instance:
        return instance
    else:
        return model(**kwargs)


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

    sid = Column(String)
    sdisplay_name = Column(String)

    # relationships
    likes_tracks = association_proxy('outbound_likes', 'track', creator=lambda track: TrackLike(track=track))

    follows_users = association_proxy('outbound_follows', 'followed', creator=lambda followed: UserFollow(followed=followed))
    followed_by_users = association_proxy('inbound_follows', 'follower', creator=lambda follower: UserFollow(follower=follower))


class UserFollow(Base):
    __tablename__ = 'user_follow'

    # foreign keys
    follower_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    followed_id = Column(Integer, ForeignKey('user.id'), primary_key=True)

    # relationships
    follower = relationship('User',
        primaryjoin=(follower_id == User.id),
        backref='outbound_follows'
    )
    followed = relationship('User',
        primaryjoin=(followed_id == User.id),
        backref='inbound_follows'
    )


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
    liked_by_users = association_proxy('inbound_likes', 'user')


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
class TrackLike(Base):
    __tablename__ = 'track_like'

    # foreign keys
    user_id = Column(Integer, ForeignKey('user.id'), primary_key=True)
    track_id = Column(Integer, ForeignKey('track.id'), primary_key=True)

    # relationships
    user = relationship('User', backref='outbound_likes')
    track = relationship('Track', backref='inbound_likes')
