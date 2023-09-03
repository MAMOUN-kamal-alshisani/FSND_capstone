from app import create_app
from models import setup_db, Movies, Actors,db
import os
import random
import unittest
import json
import uuid
from dotenv import load_dotenv
load_dotenv()
class Capstone(unittest.TestCase):

    def setUp(self):

        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = 'capstone'
        self.database_path = 'postgresql://{}:{}@{}/{}'.format(
                                'postgres', '0000',
                                'localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        self.executive_producer = os.getenv('EXECUTIVE_PRODUCER')
        self.casting_director = os.getenv('CASTING_DIRECTOR')
        self.casting_assistant = os.getenv('CASTING_ASSISTANT')
        

        movie = Movies.query.all()[0]
        self.movie = {"id":random.randint(0, 100), "title":uuid.uuid4(), 'release_date':'2023/9/1'}
        self.actor = {"id":random.randint(0, 100), "name":uuid.uuid4(), 'age':40, 'gender':"male",'movie_id':movie.id}

    def tearDown(self):
        pass

    def test_success_get_movies(self):

        res = self.client().get("/movies", headers ={'Authorization':'Bearer {}'.format(self.casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["movies"])

    def test_failure_get_movies(self):

        res = self.client().get("/movies/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_success_create_movie(self):
        
        response = self.client().post(
                                    '/movie',
                                    headers ={'Authorization':'Bearer {}'.format(self.executive_producer)},
                                    json={"id": random.randint(0, 100), "title":uuid.uuid4(), 'release_date':'2023/9/1'})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_failure_create_movie(self):

        res = self.client().post("/movie", json='self.question')
        data = res.get_json()
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 401)

    def test_success_patch_movie(self):

        movie = Movies.query.all()[0]
        response = self.client().patch('/movie/{}'.format(movie.id),
                                                                            headers ={'Authorization':'Bearer {}'.format(self.casting_director)},
                                        json=self.movie)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_failure_patch_movie(self):
        
        res = self.client().delete("/movie/none")
        self.assertEqual(res.status_code, 404)

    def test_success_delete_movie(self):

        movie = Movies.query.all()[0]
        response = self.client().delete('/movie/{}'.format(movie.id),
                                    headers ={'Authorization':'Bearer {}'.format(self.executive_producer)})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failure_delete_movie(self):
        res = self.client().delete("/movie/sa")
        self.assertEqual(res.status_code, 404)

#######################################################
#######################################################

    def test_success_get_actors(self):
        res = self.client().get("/actors", headers ={'Authorization':'Bearer {}'.format(self.casting_assistant)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["actors"])

    def test_failure_get_actors(self):
        res = self.client().get("/actors/10000")
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)

    def test_success_create_actor(self):
        movie = Movies.query.all()[0]

        response = self.client().post(
                                    '/actor',
                                        headers ={'Authorization':'Bearer {}'.format(self.casting_director)},
                                    json= {"name":uuid.uuid4(), 'age':40, 'gender':"male", 'movie_id':movie.id})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_failure_create_actor(self):
        res = self.client().post("/actor", json='self.question')
        data = res.get_json()
        self.assertEqual(data["success"], False)
        self.assertEqual(res.status_code, 401)

    def test_success_patch_actor(self):

        actor = Actors.query.all()[0]
        print(actor)
        response = self.client().patch('/actor/{}'.format(actor.id),
                                        headers ={'Authorization':'Bearer {}'.format(self.casting_director)},
                                        json=self.actor)
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertEqual(data['success'], True)

    def test_failure_patch_actor(self):
        res = self.client().delete("/actor/none")
        self.assertEqual(res.status_code, 404)

    def test_success_delete_actor(self):
        actor = Actors.query.all()[0]
        response = self.client().delete('/actor/{}'.format(actor.id),
                                        headers ={'Authorization':'Bearer {}'.format(self.casting_director)})
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    def test_failure_delete_actor(self):
        res = self.client().delete("/actor/sa")
        self.assertEqual(res.status_code, 404)
        
if __name__ == "__main__":
    unittest.main()
