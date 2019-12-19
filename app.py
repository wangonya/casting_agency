import os

from flask import Flask, jsonify, render_template, request, abort
from auth import AuthError, requires_auth
from models import setup_db, db_drop_and_create_all, Actor, Movie

app = Flask(__name__)
setup_db(app)
app.secret_key = os.getenv('SECRET')
# db_drop_and_create_all()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/movies')
@requires_auth('read:movies')
def get_all_movies(payload):
    try:
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return jsonify({
            'success': True,
            'movies': movies
        })
    except:
        abort(422)


@app.route('/movies', methods=['POST'])
@requires_auth('write:movies')
def add_movie(payload):
    title = request.get_json().get('title')
    release_date = request.get_json().get('release_date')
    try:
        data = title and release_date
        if not data:
            abort(400)
    except (TypeError, KeyError):
        abort(400)

    try:
        Movie(title=title, release_date=release_date).insert()
        return jsonify({
            'success': True,
            'movie': title
        }), 201
    except:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('update:movies')
def edit_movie(payload, movie_id):
    title = request.get_json().get('title')
    release_date = request.get_json().get('release_date')

    # make sure some data was passed
    try:
        data = title or release_date
        if not data:
            abort(400)
    except (TypeError, KeyError):
        abort(400)

    # make sure movie exists
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        abort(404)

    # update
    try:
        if title:
            movie.title = title
        if release_date:
            movie.release_date = release_date
        movie.update()
        return jsonify({
            'success': True,
            'movie': movie.format()
        }), 200
    except Exception:
        abort(422)


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
    movie = Movie.query.filter_by(id=movie_id).first()
    if not movie:
        abort(404)

    try:
        movie.delete()
        return jsonify({
            'success': True,
            'delete': movie_id
        }), 200
    except Exception:
        abort(422)


@app.route('/actors')
@requires_auth('read:actors')
def get_all_actors(payload):
    try:
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        return jsonify({
            'success': True,
            'actors': actors
        })
    except:
        abort(422)


@app.route('/actors', methods=['POST'])
@requires_auth('write:actors')
def add_actor(payload):
    name = request.get_json().get('name')
    gender = request.get_json().get('gender')
    try:
        data = name and gender
        if not data:
            abort(400)
    except (TypeError, KeyError):
        abort(400)

    try:
        Actor(name=name, gender=gender).insert()
        return jsonify({
            'success': True,
            'actor': name
        }), 201
    except:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['PATCH'])
@requires_auth('update:actors')
def edit_actor(payload, actor_id):
    name = request.get_json().get('name')
    gender = request.get_json().get('gender')

    # make sure some data was passed
    try:
        data = name or gender
        if not data:
            abort(400)
    except (TypeError, KeyError):
        abort(400)

    # make sure actor exists
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        abort(404)

    # update
    try:
        if name:
            actor.name = name
        if gender:
            actor.gender = gender
        actor.update()
        return jsonify({
            'success': True,
            'actor': actor.format()
        }), 200
    except Exception:
        abort(422)


@app.route('/actors/<int:actor_id>', methods=['DELETE'])
@requires_auth('delete:actors')
def delete_actor(payload, actor_id):
    actor = Actor.query.filter_by(id=actor_id).first()
    if not actor:
        abort(404)

    try:
        actor.delete()
        return jsonify({
            'success': True,
            'delete': actor_id
        }), 200
    except Exception:
        abort(422)


@app.route('/login')
def login():
    return render_template('login.html')


# Error Handling

@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": "bad request"
    }), 400


@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "not found"
    }), 404


@app.errorhandler(409)
def duplicate(error):
    return jsonify({
        "success": False,
        "error": 409,
        "message": "duplicate"
    }), 409


@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(AuthError)
def auth_error(error):
    return jsonify({
        "success": False,
        "error": error.status_code,
        "message": error.error
    }), error.status_code


if __name__ == '__main__':
    app.run()
