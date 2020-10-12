from auth import AuthError, requires_auth
from authlib.integrations.flask_client import OAuth
from flask import (
    Flask,
    request,
    abort,
    jsonify,
    redirect,
    session,
    render_template,
    url_for
)
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from models import setup_db, Actor, Movie
from six.moves.urllib.parse import urlencode
import os
import sys
import json


def create_app(test_config=None):
    app = Flask(__name__)
    app.secret_key = os.getenv("FLASK_SECRET_KEY")
    setup_db(app)
    CORS(app)
    return app


APP = create_app()
oauth = OAuth(APP)

auth0_url = 'https://' + os.getenv('AUTH0_DOMAIN')

auth0 = oauth.register(
    'auth0',
    client_id=os.getenv("CLIENT_ID"),
    client_secret=os.getenv('AUTH0_SECRET'),
    api_base_url=auth0_url,
    access_token_url=auth0_url + '/oauth/token',
    authorize_url=auth0_url + '/authorize',
    client_kwargs={
        'scope': 'openid profile email',
    },
)


@APP.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers',
                         'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods',
                         'GET,PATCH,POST,PUT,DELETE,OPTIONS')
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response


@APP.route('/')
def home():
    return render_template('home.html')


@APP.route('/actors')
@requires_auth('read:actor')
def get_actors():
    try:
        actors = Actor.query.all()
        actors = list(map(lambda e: e.json(), actors))
        return jsonify({
            'success': True,
            'actors': actors
        }), 200
    except BaseException:
        print(sys.exc_info())
        abort(422)


@APP.route('/movies')
@requires_auth('read:movie')
def get_movies():
    try:
        movies = Movie.query.all()
        movies = list(map(lambda e: e.json(), movies))
        return jsonify({
            'success': True,
            'movies': movies
        }), 200
    except BaseException:
        print(sys.exc_info())
        abort(422)


@APP.route('/actors', methods=['POST'])
@requires_auth('add:actor')
def create_actor():
    data = request.get_json()
    if data is None:
        abort(400)
    try:
        actor = Actor(data.get('name'), data.get('age'), data.get('gender'))
        actor.create()
        return jsonify({
            'success': True,
            'created': actor.id
        }), 201
    except BaseException:
        print(sys.exc_info())
        abort(422)


@APP.route('/movies', methods=['POST'])
@requires_auth('add:movie')
def create_movie():
    data = request.get_json()
    if data is None:
        abort(400)
    try:
        movie = Movie(data.get('title'), data.get('release_date'))
        movie.create()
        return jsonify({
            'success': True,
            'created': movie.id
        }), 201
    except BaseException:
        print(sys.exc_info())
        abort(422)


@APP.route('/actors', methods=['PATCH'])
@requires_auth('modify:actor')
def patch_actor():
    data = request.get_json()
    id = data.get('id', None)
    if id is None or data is None:
        abort(400)
    try:
        actor = Actor.query.get(id)
        if data.get('name'):
            actor.name = data.get('name')
        if data.get('age'):
            actor.age = data.get('age')
        if data.get('gender'):
            actor.gender = data.get('gender')
        actor.patch()
        return jsonify({
            'success': True,
            'patched': actor.json()
        }), 200
    except BaseException:
        print(sys.exc_info())
        abort(422)


@APP.route('/movies', methods=['PATCH'])
@requires_auth('modify:movie')
def patch_movie():
    try:
        data = request.get_json()
        id = data.get('id', None)
        if id is None:
            abort(400)
        movie = Movie.query.get(id)
        if data.get('title'):
            movie.title = data.get('title')
        if data.get('release_date'):
            movie.release_date = data.get('release_date')
        movie.patch()
        return jsonify({
            'success': True,
            'movie': movie.json()
        }), 200
    except BaseException:
        print(sys.exc_info())
        abort(422)


@APP.route('/actors/<int:id>', methods=['DELETE'])
@requires_auth('delete:actor')
def delete_actor(id):
    try:
        actor = Actor.query.get(id)
        actor.delete()
        return jsonify({
            'success': True,
            'deleted': actor.json()
        })
    except BaseException:
        if actor is None:
            abort(404)
        print(sys.exc_info())
        abort(422)


@APP.route('/movies/<int:id>', methods=['DELETE'])
@requires_auth('delete:movie')
def delete_movie(id):
    try:
        movie = Movie.query.get(id)
        movie.delete()
        return jsonify({
            'success': True,
            'deleted': movie.json()
        })
    except BaseException:
        if movie is None:
            abort(404)
        print(sys.exc_info())
        abort(422)


@APP.route('/login')
def login():
    login_route = auth0_url + '/authorize'
    audience = os.getenv("API_AUDIENCE")
    response_type = "token"
    client_id = os.getenv("CLIENT_ID")
    redirect_uri = request.url_root[:-1] + url_for('callback_handling')
    return redirect(
        "{}?audience={}&response_type={}&client_id={}&redirect_uri={}".format(
            login_route,
            audience,
            response_type,
            client_id,
            redirect_uri))


@APP.route('/logout')
def logout():
    session.clear()
    params = {
        'returnTo': url_for(
            'home',
            _external=True),
        'client_id': os.getenv("CLIENT_ID")}
    return redirect(auth0.api_base_url + '/v2/logout?' + urlencode(params))


@APP.route('/callback')
def callback_handling():
    return render_template('dashboard.html')


@APP.errorhandler(400)
def error_400(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "Error in request format"
    }), 400


@APP.errorhandler(401)
def error_401(error):
    return jsonify({
        "success": False,
        "error": error,
        "message": "Unauthorized"
    }), error


@APP.errorhandler(403)
def error_403(error):
    return jsonify({
        "success": False,
        "error": error,
        "message": "Forbidden"
    }), error


@APP.errorhandler(404)
def error_404(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "resource not found"
    }), 404


@APP.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@APP.errorhandler(AuthError)
def authError(error):
    return jsonify({
        'success': False,
        'error': error.status_code,
        'message': error.error.get('description')

    }), error.status_code


if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
