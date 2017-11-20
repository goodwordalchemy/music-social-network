from models import get_or_create, Session, Track, TrackFollow, User, UserFollow

from .json_cache import (
    load_example_track_objcts_json_file,
    load_example_user_objects_json_file,
    load_example_user_track_links_file
)

def populate_music_entity_data():
    session = Session()

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

        s_album = s_track=['album']

        album_obj = get_or_create(session, Album,
            sid=s_album['id'],
            name=s_album['name'],
            uri=s_album['uri']
        )
        obs_to_save.append(album_obj)

        track_obj.album = album_obj

        s_artists = s_track['arists']

        for s_artist in s_artists:
            artist_obj = Artist(
                sid=s_artist['sid'],
                name=s_artist['name'],
                uri=s_artist['uri']
            )
            obs_to_save.append(artist_obj)

            track_obj.artists.append(artist_obj)

        session.add_all(obs_to_save)
        session.commit()


def main():
    populate_music_entity_data()


if __name__ == '__main__':
    main()
