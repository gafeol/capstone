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
            downgrade()
            upgrade()
            self.executive_token = os.getenv("EXECUTIVE_TOKEN")
            self.director_token = os.getenv("DIRECTOR_TOKEN")
            self.assistant_token = os.getenv("ASSISTANT_TOKEN")

    def tearDown(self):
        pass

    def test_should_return_all_actors(self):
        actor = Actor(name="Abls", age=123, gender="M")
        actor.create()
        res = self.client().get('/actors', headers={"Authorization": "Bearer {}".format(self.assistant_token)})
        data = json.loads(res.data)
        self.assertEqual(res.status_code, 200)
        self.assertTrue(data['success'])
        actors = Actor.query.all()
        self.assertEqual(len(data['actors']), len(actors))

if __name__ == "__main__":
    unittest.main()

