import os
from sqlalchemy import Column, String, Integer, ForeignKey, Table
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
import json

database_name = "capstone"
database_username = "postgres"
database_password = "postgres"
local_db_path = "postgresql://{}:{}@{}/{}".format(
    database_username,
    database_password,
    'localhost:5432',
    database_name)
database_path = os.getenv('DATABASE_URL', local_db_path)

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


association_table = Table('Association', db.Model.metadata,
                          Column('movie_id', Integer, ForeignKey('movie.id')),
                          Column('actor_id', Integer, ForeignKey('actor.id'))
                          )


class Movie(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    release_date = db.Column(db.DateTime, nullable=False)
    actors = db.relationship(
        'Actor',
        secondary=association_table,
        back_populates="movies")

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date

    def create(self):
        db.session.add(self)
        db.session.commit()

    def patch(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    """ JSON representation of an object """

    def json(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
            'actors': [actor.shortJson() for actor in self.actors]
        }

    """ Shorter JSON representation of an object
        Does not include information about the linked actors
    """

    def shortJson(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date.strftime("%Y-%m-%d %H:%M:%S.%f"),
        }

    def __repr__(self):
        return json.dumps(self.json())


class Actor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    age = db.Column(db.Integer, nullable=True)
    gender = db.Column(db.String, nullable=True)
    movies = db.relationship(
        'Movie',
        secondary=association_table,
        back_populates="actors")

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
        db.session.delete(self)
        db.session.commit()

    """ JSON representation of an object """

    def json(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movies': [movie.shortJson() for movie in self.movies]
        }

    """ Shorter JSON representation of an object
        Does not include information about the linked movies
    """

    def shortJson(self):
        return {
            'id': self.id,
            'title': self.name,
            'age': self.age,
            'gender': self.gender,
        }

    def __repr__(self):
        return json.dumps(self.json())
