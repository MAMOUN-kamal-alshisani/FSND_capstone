import os
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column,Integer, Date, String, create_engine
from dotenv import load_dotenv
load_dotenv()
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

    # actor = Actors(id=3000, name='mamoun', age=30, gender='Male')
    # db.session.add(actor)
    # db.session.commit()

    #     # Create a movie
    # movie = Movies(id=3000,title='Movie 1', release_date='2021-01-01')
    # db.session.add(movie)
    # db.session.commit()

    # def create_movie(id, title, release_date ):
    #     movie = Movies(id=id, title=title, release_date = release_date)
    #     db.session.add(movie)
    #     db.session.commit()
    # @app.before_first_request
    # def initialize_database():
    #     db.create_all()
    #     create_movie(1, 'first_movie', '2023/9/1')

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
