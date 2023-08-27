import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer, Date, String, create_engine
from dotenv import load_dotenv
from flask_migrate import Migrate

database_path = os.getenv('DATABASE_URL')

db = SQLAlchemy()


def setup_db(app, database_path = database_path):
    app.config['SQLALCHEMY_DATABASE_URI'] = database_path
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.app = app
    db.init_app(app)
    migrate = Migrate(app, db)
    # db.create_all()


class Movies(db.Model):
    __tablename__ = 'Movies'

    id = Column(Integer, primary_key=True)
    title = Column(String, nullable=False, unique=True)
    release_date = Column(Date, nullable=False)
    actor = db.relationship('Actors', backref ='artist',lazy = True)   

    def __init__(self, title, release_date):
        self.title = title
        self.release_date = release_date


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            }
    

class Actors(db.Model):
    __tablename__ = 'Actors'

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False,unique=True)
    age = Column(Integer, nullable=False)
    gender = Column(String, nullable=False)
    movie_id = db.Column(db.Integer, db.ForeignKey('Movies.id'))
    def __init__(self, name, gender, age, movie_id):
        self.name = name
        self.gender = gender
        self.age = age
        self.movie_id = movie_id


    def insert(self):
        db.session.add(self)
        db.session.commit()

    def update(self):
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()

    def format(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'movie_id':self.movie_id
            }
