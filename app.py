import os

from flask import Flask, jsonify, render_template, request, abort
from auth import AuthError
from models import setup_db, db_drop_and_create_all, Actor, Movie

app = Flask(__name__)
setup_db(app)
app.secret_key = os.getenv('SECRET')
# db_drop_and_create_all()


@app.route('/movies')
def get_all_movies():
    try:
        movies = Movie.query.all()
        movies = [movie.format() for movie in movies]
        return render_template('movies.html', movies=movies)
    except:
        abort(422)


@app.route('/movies', methods=['POST'])
def add_movie():
    title = request.form.get('title')
    release_date = request.form.get('release_date')
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
def edit_movie(movie_id):
    title = request.form.get('title')
    release_date = request.form.get('release_date')

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


@app.route('/actors')
def get_all_actors():
    try:
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        return render_template('actors.html', actors=actors)
    except:
        abort(422)


@app.route('/actors', methods=['POST'])
def add_actor():
    name = request.form.get('name')
    gender = request.form.get('gender')
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
def edit_actor(actor_id):
    name = request.form.get('name')
    gender = request.form.get('gender')

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
