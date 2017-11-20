from models import reset, get_session, get_or_create, Track, TrackLike, User, UserFollow, Album, Artist

from .json_cache import (
    load_example_track_objcts_json_file,
    load_example_user_objects_json_file,
    load_example_user_track_links_file
)

def populate_music_entity_data():
    session = get_session()

    s_tracks = load_example_track_objcts_json_file()

    obs_to_save = []

    for s_track in s_tracks:

        track_obj = get_or_create(session, Track,
            sid=s_track['id'],
            name=s_track['name'],
            popularity=s_track['popularity'],
            uri=s_track['uri'],
            href=s_track['href']
        )
        obs_to_save.append(track_obj)

        s_album = s_track['album']

        album_obj = get_or_create(session, Album,
            sid=s_album['id'],
            name=s_album['name'],
            uri=s_album['uri']
        )
        obs_to_save.append(album_obj)

        track_obj.album = album_obj

        s_artists = s_track['artists']

        for s_artist in s_artists:
            artist_obj = get_or_create(session, Artist,
                sid=s_artist['id'],
                name=s_artist['name'],
                uri=s_artist['uri']
            )
            obs_to_save.append(artist_obj)

            track_obj.artists.append(artist_obj)

        session.add_all(obs_to_save)
        session.commit()

    session.close()


def populate_user_data():
    session = get_session()

    s_users = load_example_user_objects_json_file()

    for s_user in s_users:
        user_object = get_or_create(session, User,
            sid=s_user['id'],
            sdisplay_name=s_user['display_name'],
        )

        session.add(user_object)

    session.commit()
    session.close()


def populate_track_like_data():
    session = get_session()

    link_tups = load_example_user_track_links_file()

    for lt in link_tups:
        user_sid, track_sid = lt

        user = session.query(User).filter_by(sid=user_sid).first()
        track = session.query(Track).filter_by(sid=track_sid).first()

        like = TrackLike(user=user, track=track)

        session.add(like)

    session.commit()
    session.close()


def populate_user_follow_data():
    session = get_session()

    users = session.query(User).all()

    src = users[0]

    for dest in users[1:]:
        src.follows_users.append(dest)

    session.add(src)

    session.commit()
    session.close()


def main():
    reset()

    populate_music_entity_data()
    populate_user_data()
    populate_track_like_data()
    populate_user_follow_data()


if __name__ == '__main__':
    main()
