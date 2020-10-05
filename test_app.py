from flask import url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import upgrade, downgrade
import json
import os
import unittest
from app import create_app, APP
from models import setup_db, Actor, Movie

class TestCapstone(unittest.TestCase):
    def setUp(self):
        self.app = APP 
        #self.app.config["TESTING"] = True
        self.client = self.app.test_client
        database_name = "capstone_test"
        database_username = "postgres"
        database_password = "postgres"
        self.database_path = "postgres://{}:{}@{}/{}".format(
            database_username,
            database_password,
            'localhost:5432',
            database_name)
        setup_db(self.app, self.database_path)

        with self.app.app_context():
            upgrade()
            self.executive_token = os.getenv("EXECUTIVE_TOKEN")
            self.director_token = os.getenv("DIRECTOR_TOKEN")
            self.assistant_token = os.getenv("ASSISTANT_TOKEN")

    def tearDown(self):
        #with self.app.app_context():
            #downgrade()
        pass

    def test_assistant_should_get_all_actors(self):
        actor = Actor(name="Abls", age=123, gender="M")
        actor.create()
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_director_should_get_all_actors(self):
        actor = Actor(name="Abls", age=123, gender="M")
        actor.create()
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.director_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_executive_should_get_all_actors(self):
        actor = Actor(name="Abls", age=123, gender="M")
        actor.create()
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.executive_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

    def test_assistant_should_get_all_movies(self):
        movie = Movie(title="Test Title", release_date="2012-04-23 18:25:43.511")
        movie.create()
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_director_should_get_all_movies(self):
        movie = Movie(title="Test Title", release_date="2012-04-23 18:25:43.511")
        movie.create()
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.director_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_executive_should_get_all_movies(self):
        movie = Movie(title="Test Title", release_date="2012-04-23 18:25:43.511")
        movie.create()
        res = self.client().get('/movies', headers={"Authorization": "Bearer {}".format(self.executive_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        movies = Movie.query.all()
        self.assertEqual(len(data['movies']), len(movies))

    def test_assistant_cant_create_actor(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(self.assistant_token)}, json=dict(name="A", age=12, gender="M"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 401)
        self.assertFalse(data['success'])

    
    def test_director_should_create_actor(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(self.director_token)}, json=dict(name="A", age=12, gender="M"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])
    
    def test_executive_should_create_actor(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(self.executive_token)}, json=dict(name="A", age=12, gender="M"))
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 201)
        self.assertTrue(data['success'])

        createdId = data['created']
        actor = Actor.query.get(createdId)
        self.assertIsNotNone(actor)
        self.assertEqual(actor.id, createdId)

    def test_incorrect_create_actor(self):
        res = self.client().post('/actors', headers={"Authorization": "Bearer {}".format(self.executive_token)})
        self.assertEqual(res.status_code, 400)
        data = json.loads(res.data)
        self.assertFalse(data['success'])

if __name__ == "__main__":
    unittest.main()
