import os
from sqlalchemy import Column, String, Integer
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "capstone"
database_username = "postgres"
database_password = "postgres"
database_path = "postgres://{}:{}@{}/{}".format(
    database_username,
    database_password,
    'localhost:5432',
    database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''

def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    Migrate(app, db)

class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)

    def __init__(self, t, rd):
        self.title = t
        self.release_date = rd

    def create(self):
        db.session.add(self)
        db.session.commit()

    def patch(self):
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()
    
    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date
        }
    
    def __repr__(self):
        return json.dumps(self.json())

class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)

    def __init__(self, name, age, gender):
        self.name = name
        self.age = age
        self.gender = gender

    def create(self):
        db.session.add(self)
        db.session.commit()

    def patch(self):
        db.session.commit()

    def delete(self):
        db.session.remove(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender
        }
    
    def __repr__(self):
        return json.dumps(self.json())