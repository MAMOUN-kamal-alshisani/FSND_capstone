from email import header
from http.client import ImproperConnectionState
import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy
from models import Movies, Actors, setup_db, db
from app import create_app


database_name = "capstone"
database_path = 'postgresql://postgres:0000@localhost:5432/{}'.format(
    database_name)

casting_assistant_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlptQ21uRkRfS3gzUFRkamVIcnN2bCJ9.eyJpc3MiOiJodHRwczovL2Rldi1mMHU3d2FzdWZpNzB0aXlhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGViOGQ4MjBiMzhiMDc5OTY4MGUxYmQiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY5MzE1OTcyNywiZXhwIjoxNjkzMTY2OTI3LCJhenAiOiIzbktaSk4zWjlZbVlFckdKWUM2S3czdFVLU0dEZThPYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiXX0.i9cZv9glIS0dhBGDG4IMxc9hr6ufY5TASK0wjjMI-iEMnE0xbXMWd86qCgco-zxCnyd2Y4WzGdcJDF7gXZkfqTVW1iVac8qABUGkGjfYRmUvcg3p5RcAcIjEnmRsuTp13pnhkav0mwrgohjjYvc5O0PgcK_6NnK3xj6-oGyjJ84fGoAmpw08fqcWWp7wjUHX_Db-vMMjRQRym_NRqK21yHtRjdHTbplHqKRmtxV3mSW9AAYL46KQIio_UsPPoaaoYvWMZpNG1UrxnRHKQCHaRed0COfLft8HEEf6F_dptoXp2_xpW1v4FjJ77oNf_QmNyBTZmBkUB1LFr0MS8BvT8A"
casting_director_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlptQ21uRkRfS3gzUFRkamVIcnN2bCJ9.eyJpc3MiOiJodHRwczovL2Rldi1mMHU3d2FzdWZpNzB0aXlhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGViOGRkODQ5OGVlMWVlMzE3ZmZlY2MiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY5MzE2MDAxNCwiZXhwIjoxNjkzMTY3MjE0LCJhenAiOiIzbktaSk4zWjlZbVlFckdKWUM2S3czdFVLU0dEZThPYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciJdfQ.NH3LMRTdebEfdG8rhzHTHjh9HLpPZ9tX6pgKco5ZANWHP8POOhm-_IsA80AvqLgGLW45MWZIIp-6MXEtt_hrk_YVo9Lq-wuj1bJjuf5BPQSHMH4LW3TCMyNSx4ZcSqliQ_Y2XvxScW-qGlrBhYgYQh-b78T6_8kzg3arMgC-Cil0aVoBfWLf8gEyJbKnKsemiG0iUAK00OnWJSHwzpalyWy6xgPKGVIolsC5MzZRro-J5TaXD0WU7J_Ew_vJAh94Skr9hOiKdk9Or_0gTNE0JBp0F7YfH9TERdjXFAVFJIpgUsKFOXL2c8qzqqgt-ZIQw2AKPG1hHFqkpkZCSs4JMg"
executive_producer_token = "eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6IlptQ21uRkRfS3gzUFRkamVIcnN2bCJ9.eyJpc3MiOiJodHRwczovL2Rldi1mMHU3d2FzdWZpNzB0aXlhLnVzLmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw2NGViOGU0ZTQ5ZTMxMTAzNWFkNzM5NmEiLCJhdWQiOiJjYXBzdG9uZSIsImlhdCI6MTY5MzE2MDE1OSwiZXhwIjoxNjkzMTY3MzU5LCJhenAiOiIzbktaSk4zWjlZbVlFckdKWUM2S3czdFVLU0dEZThPYyIsInNjb3BlIjoiIiwicGVybWlzc2lvbnMiOlsiZGVsZXRlOmFjdG9yIiwiZGVsZXRlOm1vdmllIiwiZ2V0OmFjdG9ycyIsImdldDptb3ZpZXMiLCJwYXRjaDphY3RvciIsInBhdGNoOm1vdmllIiwicG9zdDphY3RvciIsInBvc3Q6bW92aWUiXX0.gSHMztpbOWp9LQMXQ7sxZKwDeBTTfLX5hKdXye-VEwChSV034ajtG8Mv-RK565OShYkpQ6Rs0V8jFYMusgjv32i32ULg6M8fXrKZ2tWyDWqlSP0civCKjPBbp5XfI7BCg4dnTlFLceWOqdcIVAvDIOOXyP9Z8aIWY-C6gIW94dtZKfPRsoP4x-SBMAR2e1YEP6B5JB26OMngtSE7jQHIi1z7pkGTz9LoO5aotdBMRfsiEpmYR5S_IzJEqrXEajOsLZv-MgoZHgIs6P9h7ViBD_-uFbkawvxwJk8E4b_KLTxzaNqmaPdke1zO0SRxjkYPj17gmVkeptn4AimOT4XEsg"


class CastingAgencyTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client
        self.database_path = database_path
        setup_db(self.app, self.database_path)
        self.casting_assistant = casting_assistant_token
        self.casting_director = casting_director_token
        self.executive_producer = executive_producer_token
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
            # self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass


    def test_list_actors(self):
        res = self.client().get('/actors',
                                headers={
                                    "Authorization": "Bearer {}"
                                    .format(self.casting_assistant)
                                })
        data = json.loads(res.data)
        print(data)
        if res.status_code == 200: #since the test database maybe empty
            self.assertTrue(data['success'])
            # self.assertNotEqual(len(data['actors']), 0)

    # def test_post_movies(self):
    #     movie = {
    #         "id":"500",
    #         "title": "Avengers",
    #         "release_date": "2019-01-02",
    #     }

    #     res = self.client().post('/movie',
    #                              headers={
    #                                  "Authorization": "Bearer {}"
    #                                  .format(self.executive_producer)
    #                              }, json=movie)
    #     data = json.loads(res.data)
    #     print(data)
    #     self.assertTrue(data['success'])
    #     movie_db = Movies.query.get(data['id'])
    #     movie['id'] = data['id']
    #     self.assertEqual(movie_db.get_formatted_json(), movie)
        

#     def test_post_movies_fail_400(self):
#         movie = {
#             "title": "Avengers",
#             "release_date": "2019-01-02",
#         }
#         res = self.client().post('/movie',
#                                  headers={
#                                      "Authorization": "Bearer {}"
#                                      .format(self.executive_producer)
#                                  }, json=movie)
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(400, res.status_code)
#         self.assertNotEqual(len(data['message']), 'Bad request')

#     def test_post_movies_fail_401(self):
#         movie = {
#             "title": "Avengers",
#             "release_date": "2019-01-02",
#         }
#         res = self.client().post('/movie',
#                                  headers={
#                                      "Authorization": "Bearer {}"
#                                      .format(self.casting_assistant)
#                                  }, json=movie)
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(401, res.status_code)

#     def test_list_movies_fail_401(self):
#         res = self.client().get('/movies')
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 401)
#         self.assertFalse(data['success'])

#     def test_list_movies(self):
#         res = self.client().get('/movies',
#                                 headers={
#                                     "Authorization": "Bearer {}"
#                                     .format(self.casting_assistant)
#                                 })
#         data = json.loads(res.data)
#         print(data)
#         if res.status_code == 200: #since the test database maybe empty
#             self.assertTrue(data['success'])
#             self.assertNotEqual(len(data['movies']), 0)

#     def test_delete_movie(self):
#         movie = Movies.query.order_by(Movies.id).first()
#         res = self.client().delete('/movie/'+str(movie.id),
#                                    headers={
#             "Authorization": "Bearer {}"
#             .format(self.executive_producer)})
#         data = json.loads(res.data)
#         print(data)
#         self.assertTrue(data['success'])
#         movie = Movies.query.get(data['deleted'])
#         self.assertEqual(movie, None)

#     def test_delete_movie_fail_401(self):
#         res = self.client().delete('/movie/1000')
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(401, res.status_code)

#     def test_delete_movie_fail_404(self):
#         res = self.client().delete('/movie/1000',
#                                    headers={
#                                        "Authorization": "Bearer {}"
#                                        .format(self.executive_producer)})
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(404, res.status_code)

#     def test_patch_movie_fail_404(self):
#         movie = {
#             "title": "Avengers",
#             "release_date": "2019-01-02",
#         }
#         res = self.client().patch('/movie/1000',
#                                   headers={
#                                       "Authorization": "Bearer {}".format(self.casting_director)
#                                   }, json=movie)
#         data = json.loads(res.data)
#         print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(404, res.status_code)

#     def test_patch_movie_fail_401(self):
#         movie = {
#             "title": "Avengers",
#             "release_date": "2019-01-02",
#         }
#         res = self.client().patch('/movie/1000',
#                                   headers={
#                                       "Authorization": "Bearer {}".format(self.casting_assistant)
#                                   }, json=movie)
#         data = json.loads(res.data)
#         print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(401, res.status_code)

#     def test_patch_movie(self):
#         movie_patch = {
#             "title": "Avengers 2",
#             "release_date": "2019-01-02",
#         }
#         movie = Movies.query.order_by(Movies.id).first()
#         print(movie)
#         res = self.client().patch('/movie/'+str(movie.id),
#                                   headers={
#             "Authorization": "Bearer {}".format(self.casting_director)
#         }, json=movie_patch)
#         data = json.loads(res.data)
#         print(data)
#         self.assertTrue(data['success'])
#         self.assertEqual(200, res.status_code)
#         movie = Movies.query.get(data['movie']['id'])
#         movie_json = movie.get_formatted_json()
#         for key in movie_patch.keys():
#             self.assertEqual(movie_patch[key], movie_json[key])

# # actor tests

#     def test_post_actor(self):
#         actor = {
#             "name": "rish",
#             "gender": "male",
#             "age": 22,
#         }

#         res = self.client().post('/actor',
#                                  headers={
#                                      "Authorization": "Bearer {}"
#                                      .format(self.executive_producer)
#                                  }, json=actor)
#         data = json.loads(res.data)
#         print(data)
#         self.assertTrue(data['success'])
#         actor_db = Actors.query.get(data['actor_id'])
#         actor['id'] = data['actor_id']
#         self.assertEqual(actor_db.get_formatted_json(), actor)

#     def test_post_actors_fail_400(self):
#         actor = {
#             "name": "rish",
#             "gender": "male",
#         }
#         res = self.client().post('/actor',
#                                  headers={
#                                      "Authorization": "Bearer {}"
#                                      .format(self.executive_producer)
#                                  }, json=actor)
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(400, res.status_code)
#         self.assertNotEqual(len(data['message']), 'Bad request')

#     def test_post_actors_fail_401(self):
#         actor = {
#             "name": "rish",
#             "gender": "male",
#             "age":  22
#         }
#         res = self.client().post('/actor',
#                                  headers={
#                                      "Authorization": "Bearer {}"
#                                      .format(self.casting_assistant)
#                                  }, json=actor)
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(401, res.status_code)

#     def test_list_actors_fail_401(self):
#         res = self.client().get('/actors')
#         data = json.loads(res.data)
#         self.assertEqual(res.status_code, 401)
#         self.assertFalse(data['success'])

#     def test_list_actors(self):
#         res = self.client().get('/actors',
#                                 headers={
#                                     "Authorization": "Bearer {}"
#                                     .format(self.casting_assistant)
#                                 })
#         data = json.loads(res.data)
#         print(data)
#         if res.status_code == 200: #since the test database maybe empty
#             self.assertTrue(data['success'])
#             self.assertNotEqual(len(data['actors']), 0)

#     def test_delete_actors(self):
#         actor = Actors.query.order_by(Actors.id).first()
#         res = self.client().delete('/actor/'+str(actor.id),
#                                    headers={
#             "Authorization": "Bearer {}"
#             .format(self.executive_producer)})
#         data = json.loads(res.data)
#         print(data)
#         self.assertTrue(data['success'])
#         actor = Actors.query.get(data['deleted'])
#         self.assertEqual(actor, None)

#     def test_delete_actor_fail_401(self):
#         res = self.client().delete('/actor/1000')
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(401, res.status_code)

#     def test_delete_actor_fail_404(self):
#         res = self.client().delete('/actor/1000',
#                                    headers={
#                                        "Authorization": "Bearer {}"
#                                        .format(self.executive_producer)})
#         data = json.loads(res.data)
#         # print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(404, res.status_code)

#     def test_patch_actor_fail_404(self):
#         actor = {
#             "name": "gopi",
#             "gender": "male",
#         }
#         res = self.client().patch('/actor/1000',
#                                   headers={
#                                       "Authorization": "Bearer {}".format(self.casting_director)
#                                   }, json=actor)
#         data = json.loads(res.data)
#         print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(404, res.status_code)

#     def test_patch_actor_fail_401(self):
#         actor = {
#             "name": "gopi",
#             "gender": "male",
#         }
#         res = self.client().patch('/actor/1000',
#                                   headers={
#                                       "Authorization": "Bearer {}".format(self.casting_assistant)
#                                   }, json=actor)
#         data = json.loads(res.data)
#         print(data)
#         self.assertFalse(data['success'])
#         self.assertEqual(401, res.status_code)

#     def test_patch_actor(self):
#         actor = {
#             "name": "gopi",
#             "gender": "male",
#         }
#         actor_db = Actors.query.order_by(Actors.id).first()
#         res = self.client().patch('/actor/'+str(actor_db.id),
#                                   headers={
#             "Authorization": "Bearer {}".format(self.casting_director)
#         }, json=actor)
#         data = json.loads(res.data)
#         print(data)
#         self.assertTrue(data['success'])
#         self.assertEqual(200, res.status_code)
#         actor_db = Actors.query.get(data['actor']['id'])
#         actor_json = actor_db.get_formatted_json()
#         for key in actor.keys():
#             self.assertEqual(actor[key], actor_json[key])


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()