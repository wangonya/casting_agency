import os

from flask import Flask, jsonify, render_template, request, abort
from auth import AuthError
from models import setup_db, db_drop_and_create_all, Actor, Movie

app = Flask(__name__)
setup_db(app)
app.secret_key = os.getenv('SECRET')
# db_drop_and_create_all()


@app.route('/movies')
def movies():
    return render_template('movies.html')


@app.route('/actors')
def get_all_actors():
    try:
        actors = Actor.query.all()
        actors = [actor.format() for actor in actors]
        # return jsonify({
        #     'success': True,
        #     'actors': actors
        # }), 200
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
