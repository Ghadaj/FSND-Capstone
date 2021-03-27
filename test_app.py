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
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)
        
        self.assistant =  {'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZaXzB1Mzk5S0UzZTRGdG9wUG5fViJ9.eyJpc3MiOiJodHRwczovL2NzLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E1OTYyOTlkYmViMDA2OGI2NWZmNCIsImF1ZCI6ImNhc3RpbmdBZ2VuY3kiLCJpYXQiOjE2MTY4NjEwMDUsImV4cCI6MTYxNjg2ODIwNSwiYXpwIjoiUk5CU1ZaNDJpaTBPS01sT2FSWVNQYVg5TGJvWm9WMEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImdldDphY3RvcnMiLCJnZXQ6bW92aWVzIl19.DOhAIOoIHvALHuqbfHLCRPH9q374i01BqLDIxtai78df4uFAOjGcm6S8AiV3qg0DUElC8mC1HfU7LY6chYcrCmXUTYapVxaRpPpdySgdJ_pDBXsxi7ZWWAUT-NViBtxrjgTkBg6uHJQwTZTUBulkmmjs6JpJY_mIkav72e9wMMhHW4AXDzoofqlmQHgK4SUeW7QJdG2Q2vJ0wh_jrf3popQOOSBMY2_ZY52iTHMtZFEV92UMFQ_M8kHsHDlv2vlWog1v9I5A_dIDKeF-0Bcvl3ptPd6dwY_mzWGTDLDwmMtVdBHhi90uEFa1mLv7Qz-uW3z_Np0WK0Re1E_rbAK4Fw'}
        self.director =  {'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZaXzB1Mzk5S0UzZTRGdG9wUG5fViJ9.eyJpc3MiOiJodHRwczovL2NzLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E1OWExNTY5MjQzMDA3MGMwOTAwYSIsImF1ZCI6ImNhc3RpbmdBZ2VuY3kiLCJpYXQiOjE2MTY4NjEwOTMsImV4cCI6MTYxNjg2ODI5MywiYXpwIjoiUk5CU1ZaNDJpaTBPS01sT2FSWVNQYVg5TGJvWm9WMEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJnZXQ6YWN0b3JzIiwiZ2V0Om1vdmllcyIsInBhdGNoOmFjdG9ycyIsInBhdGNoOm1vdmllcyIsInBvc3Q6YWN0b3JzIl19.KCwhT_JhfWMlKY5qJl60bHExsQRmpnmPN7GaVbiRns2Lt9VULHuPsawgVZrU910velPCaoUwnEJiw2S4Nn80cDMVqVNqDLCfs-t8ue1V6R-n8O1jcT8FSleuTmg65t_azFNswQEIIv_QOOUPWuM1buflEjUMGHCXsYTevLNvNkx3lnFezRIfR-5vpzfwJJRh9zyhPIK9qB1y3nBsp_QSgaPl_R0myiWpnfsIo5c0y-kXI90cftSZXb1ElBAMxCTEJyWee9mYeCxOkiwKsnnAmNY_KQLQ96g-bfANmrR1i6Ilcnc0KcacGdIpSJ8O14RC0A-HjSSX7m84qeqAK0oTgA'}
        self.producer = {'Authorization': 'Bearer ' + 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IkZaXzB1Mzk5S0UzZTRGdG9wUG5fViJ9.eyJpc3MiOiJodHRwczovL2NzLWZzbmQudXMuYXV0aDAuY29tLyIsInN1YiI6ImF1dGgwfDYwM2E1OWNiYjhjZGY2MDA3MDg4MDE0NyIsImF1ZCI6ImNhc3RpbmdBZ2VuY3kiLCJpYXQiOjE2MTY4NjExODksImV4cCI6MTYxNjg2ODM4OSwiYXpwIjoiUk5CU1ZaNDJpaTBPS01sT2FSWVNQYVg5TGJvWm9WMEYiLCJzY29wZSI6IiIsInBlcm1pc3Npb25zIjpbImRlbGV0ZTphY3RvcnMiLCJkZWxldGU6bW92aWVzIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvcnMiLCJwYXRjaDptb3ZpZXMiLCJwb3N0OmFjdG9ycyIsInBvc3Q6bW92aWVzIl19.IVE7MCibmzXJn9hZtazLfxAt7pS2MytshjuSM6RIHBsvDXqOCSe7h514c3d6VhVDbEIbTAFPC-zZveX76QHBBMpXW-J8txL9q6PV-ZMVGi-vY519AUio6dsGreI7Fme_kl3WSNo1MjTePf0_XWAvRe5rVXbllRAugy-rActkHwhHg1slweceUeZg3FaZyBvoEIWOTcjZarFEVMZvBVKqYJSdO8XCyhaRChdhZbh6gJsdmQ72A4b8ojjT7iy1mCq03iKtuJO0GTPBqjkFeaT3fPrqiLWHZbFW6e2qJV_6Gd19ZO0xtojChwds88NtT9qBe1YnE2UHj1fk9gEjSmRRGA'}

        #self.assistant = {'Authorization': 'Bearer ' + os.environ.get('ASSISTANT_TOKEN')}
        #self.director = {'Authorization': 'Bearer ' + os.environ.get('DIRECTOR_TOKEN')}
        #self.producer = {'Authorization': 'Bearer ' + os.environ.get('PRODUCER_TOKEN')}
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
        self.assertEqual(data['message'],'Permission not found.')

    def test_post_actor_not_authorized(self):
        res = self.client().post('/actors',headers=self.assistant,json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Permission not found.')


	
    def test_delete_actor_not_athurized(self):
        res = self.client().delete('/actors/3', headers=self.assistant)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Permission not found.')
		
    def test_patch_actor_not_authorized(self):
        res = self.client().patch('/actors/1',headers=self.assistant,json=self.update_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Permission not found.')
		
		
		
        # Test Director 
    def test_post_actor(self):
        res = self.client().post('/actors',headers=self.director,json=self.new_actor)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['actors'])
	
    def test_post_movie_not_authorized(self):
        res = self.client().post('/movies',headers=self.director, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Permission not found.')

    # TEST Producer
    def test_patch_movie(self):
        res = self.client().patch('/movies/1',headers=self.producer,json=self.update_movie)
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
        res = self.client().post('/movies',headers=self.producer, json=self.new_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['movies'])
    
    def test_patch_movie_resource_not_found(self):
        res = self.client().patch('/movies/100',headers=self.producer,json=self.update_movie)
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'],'Movie #100 not found.')	
			

if __name__ == "__main__":
    unittest.main()