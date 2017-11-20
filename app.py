from flask import Flask, jsonify, render_template

from models import get_session, Track, User

app = Flask(__name__)

@app.route('/')
def index():
    session = get_session()

    all_users = session.query(User).all()

    all_users_str = str([u.sid for u in all_users])

    session.close()

    return all_users_str


@app.route('/user/<user_id>')
def show_user_profile(user_id):
    session = get_session()

    user = session.query(User).get(user_id)

    likes_tracks = user.likes_tracks
    likes_tracks_str = str([t.sid for t in likes_tracks])

    follows_users = user.follows_users
    follows_users_str = str([u.sid for u in follows_users])

    followed_by_users = user.followed_by_users
    followed_by_users_str = str([u.sid for u in followed_by_users])

    session.close()

    return (
        '<div>likes: {}</div>'
        '<br />'
        '<div>follows: {}</div>'
        '<br />'
        '<div>followed by users: {}</div>'
    ).format(likes_tracks_str, follows_users_str, followed_by_users_str)

@app.route('/track/<track_id>')
def show_track_profile(track_id):
    session = get_session()

    track = session.query(Track).get(track_id)

    liked_by_users = track.liked_by_users
    liked_by_users_str = str([u.sid for u in liked_by_users])

    session.close()

    return '<div>liked by users: {}</div>'.format(liked_by_users_str)





if __name__ == '__main__':
    app.run(debug=True)
