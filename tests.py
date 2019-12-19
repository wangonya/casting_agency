import unittest
import os
from app import app
from models import db, Movie, Actor

database_filename = 'test.db'
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

assistant_token = os.getenv('ASSISTANT_TOKEN')
director_token = os.getenv('DIRECTOR_TOKEN')
producer_token = os.getenv('PRODUCER_TOKEN')


def set_auth_header(role):
    if role == 'assistant':
        return {'Authorization': 'Bearer {}'.format(assistant_token)}
    elif role == 'director':
        return {'Authorization': 'Bearer {}'.format(director_token)}
    elif role == 'producer':
        return {'Authorization': 'Bearer {}'.format(producer_token)}


class MainTestCase(unittest.TestCase):

    # executed prior to each test
    def setUp(self):
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['DEBUG'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = database_path
        self.app = app.test_client()
        db.drop_all()
        db.create_all()

    # movies endpoint tests

    def test_get_movies(self):
        res = self.app.get(
            '/movies', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_movies_unauthorized(self):
        res = self.app.get(
            '/movies', headers=set_auth_header(''))
        self.assertEqual(res.status_code, 401)

    def test_add_movie(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        res = self.app.post(
            '/movies', json=data, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_add_movie_fail(self):
        res = self.app.post(
            '/movies', json={}, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)

    def test_add_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        res = self.app.post(
            '/movies', json=data, headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_movie(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post('/movies', json=data,
                      headers=set_auth_header('producer'))

        movie_id = Movie.query.first().id
        res = self.app.patch(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_edit_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post('/movies', json=data,
                      headers=set_auth_header('producer'))

        movie_id = Movie.query.first().id
        res = self.app.patch(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_movie_fail(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post('/movies', json=data,
                      headers=set_auth_header('producer'))

        movie_id = Movie.query.first().id

        data = {
            "title": '',
            "release_date": ''
        }
        res = self.app.patch(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 400)

    def test_delete_movie(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post(
            '/movies', json=data, headers=set_auth_header('producer'))

        movie_id = Movie.query.first().id
        res = self.app.delete(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_delete_movie_unauthorized(self):
        data = {
            "title": "title",
            "release_date": "release_date"
        }
        self.app.post(
            '/movies', json=data, headers=set_auth_header('producer'))

        movie_id = Movie.query.first().id
        res = self.app.delete(
            f'/movies/{movie_id}', json=data,
            headers=set_auth_header('director'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    # actors endpoint tests

    def test_get_actors(self):
        res = self.app.get(
            '/actors', headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 200)

    def test_get_actors_unauthorized(self):
        res = self.app.get(
            '/actors', headers=set_auth_header(''))
        self.assertEqual(res.status_code, 401)

    def test_add_actor(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        res = self.app.post(
            '/actors', json=data, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()['success'], True)

    def test_add_actor_fail(self):
        res = self.app.post(
            '/actors', json={}, headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 400)
        self.assertEqual(res.get_json()['success'], False)

    def test_add_actor_unauthorized(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        res = self.app.post(
            '/actors', json=data, headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_actor(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actor.query.first().id
        res = self.app.patch(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_edit_actor_unauthorized(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actor.query.first().id
        res = self.app.patch(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_edit_actor_fail(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actor.query.first().id
        res = self.app.patch(
            f'/actors/{actor_id}', data={},
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)
        self.assertEqual(res.get_json()['message'], 'unauthorized')

    def test_delete_actor(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actor.query.first().id
        res = self.app.delete(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('producer'))
        self.assertEqual(res.status_code, 200)
        self.assertEqual(res.get_json()['success'], True)

    def test_delete_actor_unauthorized(self):
        data = {
            "name": "name",
            "gender": "M"
        }
        self.app.post('/actors', json=data,
                      headers=set_auth_header('producer'))

        actor_id = Actor.query.first().id
        res = self.app.delete(
            f'/actors/{actor_id}', json=data,
            headers=set_auth_header('assistant'))
        self.assertEqual(res.status_code, 403)


if __name__ == '__main__':
    unittest.main()
