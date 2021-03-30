import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from app import create_app
from models import setup_db, Movies, Actors


class AgencyTestCase(unittest.TestCase):
    """This class represents the Casting Agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "agency"
        self.database_path = "postgres://{}/{}".format(
            'localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        self.assistant = {'Authorization': 'Bearer ' +
                          os.environ.get('ASSISTANT_TOKEN')}
        self.director = {'Authorization': 'Bearer ' +
                         os.environ.get('DIRECTOR_TOKEN')}
        self.producer = {'Authorization': 'Bearer ' +
                         os.environ.get('PRODUCER_TOKEN')}
        self.new_movie = {
            'title': 'My Movie',
            'release_date': '2021-11-12'
        }

        self.new_actor = {
            'name': 'Actor',
            'age': '25',
            'gender': 'Female'
        }

        self.update_movie = {
            'title': 'My movie updated',
            'release_date': '2020-04-01'
        }

        self.update_actor = {
            'name': 'Actor updated ',
            'age': '20',
            'gender': 'Male'
        }
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    # Test Assistant
    def test_get_movies(self):
        res = self.client().get('/movies', headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_get_actors(self):
        res = self.client().get('/actors', headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_delete_movie_not_authorized(self):
        res = self.client().delete('/movies/1', headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_post_actor_not_authorized(self):
        res = self.client().post('/actors', headers=self.assistant, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_delete_actor_not_athurized(self):
        res = self.client().delete('/actors/3', headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    def test_patch_actor_not_authorized(self):
        res = self.client().patch('/actors/1', headers=self.assistant, json=self.update_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

        # Test Director

    def test_post_actor(self):
        res = self.client().post('/actors', headers=self.director, json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])

    def test_post_movie_not_authorized(self):
        res = self.client().post('/movies', headers=self.director, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Permission not found.')

    # TEST Producer
    def test_patch_movie(self):
        res = self.client().patch('/movies/1', headers=self.producer, json=self.update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_delete_movie(self):
        res = self.client().delete('/movies/2', headers=self.producer)
        data = json.loads(res.data)
        movie = Movies.query.get(2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        self.assertEqual(movie, None)

    def test_delete_actor(self):
        res = self.client().delete('/actors/2', headers=self.producer)
        data = json.loads(res.data)
        actor = Actors.query.get(2)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['delete'], 2)
        self.assertEqual(actor, None)

    def test_post_movie(self):
        res = self.client().post('/movies', headers=self.producer, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])

    def test_patch_movie_resource_not_found(self):
        res = self.client().patch('/movies/100', headers=self.producer, json=self.update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Movie #100 not found.')


if __name__ == "__main__":
    unittest.main()
