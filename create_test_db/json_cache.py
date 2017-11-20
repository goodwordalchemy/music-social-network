import json

from gwa_spotify_api import SpotifyAuthAPI
from gwa_spotify_api.exceptions import SpotifyException


"""A file with one uuid per line must exist in the following directory"""
SPOTIFY_UUIDS_FILENAME = 'data/spotify_uuids.txt'

EXAMPLE_SPOTIFY_USER_OBJECTS_FILENAME = 'data/example_spotify_user_objects.json'
EXAMPLE_SPOTIFY_TRACK_OBJECTS_FILENAME = 'data/example_spotify_track_ojects.json'

EXAMPLE_USER_TRACK_LINKS_FILENAME = 'data/example_spotify_track_links.txt'


def get_spotify_uuids_list(n_uuids=5):
    with open(SPOTIFY_UUIDS_FILENAME, 'r') as handle:
        spotify_uuids = handle.readlines()

    # Discarding first line because it is a vestigial (a column name)
    spotify_uuids = spotify_uuids[1:]

    # remove newline characters
    spotify_uuids = [x.strip() for x in spotify_uuids]

    spotify_uuids = spotify_uuids[:n_uuids]

    return spotify_uuids


def get_user_objects_from_spotify_api(api, spotify_uuids):
    print('getting_user_objects...')

    user_objects = []

    for uuid in spotify_uuids:
        try:
            user_object = api.get('users/{}'.format(uuid))
        except SpotifyException as e:
            print(e)
            continue

        user_objects.append(user_object)

    return user_objects


def save_example_user_objects_to_json_file():

    api = SpotifyAuthAPI()
    spotify_uuids = get_spotify_uuids_list()

    user_objects = get_user_objects_from_spotify_api(api, spotify_uuids)

    with open(EXAMPLE_SPOTIFY_USER_OBJECTS_FILENAME, 'w') as handle:
        json.dump(user_objects, handle)


def load_example_user_objects_json_file():
    with open(EXAMPLE_SPOTIFY_USER_OBJECTS_FILENAME, 'r') as handle:
        data = json.load(handle)

    return data


def save_example_track_objects_and_likes_to_files():
    spotify_user_objects = load_example_user_objects_json_file()

    api = SpotifyAuthAPI()

    likes = []
    track_objects = []

    for user_object in spotify_user_objects:
        uuid = user_object['id']

        playlists = api.get('users/{}/playlists'.format(uuid))

        for idx in range(len(playlists)):
            num_tracks = playlists[idx]['tracks']['total']
            if num_tracks < 100 and num_tracks > 1:
                break

        first_playlist_id = playlists[idx]['id']
        first_playlist_owner_id = playlists[idx]['owner']['id']

        playlist_url = 'users/{}/playlists/{}/tracks'.format(
            first_playlist_owner_id, first_playlist_id
        )

        playlist_tracks = api.get(playlist_url)
        playlist_tracks = [t['track'] for t in playlist_tracks]

        track_objects.extend(playlist_tracks)

        likes.extend([(uuid, track['id']) for track in track_objects])

        break

    with open(EXAMPLE_SPOTIFY_TRACK_OBJECTS_FILENAME, 'w') as handle:
        json.dump(track_objects, handle)

    with open(EXAMPLE_USER_TRACK_LINKS_FILENAME, 'w') as handle:
        likes_str = '\n'.join(['{},{}'.format(l[0], l[1]) for l in likes])
        handle.write(likes_str)


def load_example_track_objcts_json_file():
    with open(EXAMPLE_SPOTIFY_TRACK_OBJECTS_FILENAME, 'r') as handle:
        data = json.load(handle)

    return data


def load_example_user_track_links_file():
    with open(EXAMPLE_USER_TRACK_LINKS_FILENAME, 'r') as handle:
        data = handle.readlines()

    data = [d.strip('\n') for d in data]

    return data

def write_test_data_files():
    save_example_user_objects_to_json_file()
    save_example_track_objects_and_likes_to_files()


def main():
    write_test_data_files()
