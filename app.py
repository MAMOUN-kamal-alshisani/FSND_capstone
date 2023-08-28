import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from models import setup_db, Actors, Movies
from auth.auth import AuthError, requires_auth

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  # CORS(app)
  CORS(app, resources={r"/*": {"origins": ['*']}})
  @app.after_request
  def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers','Content-Type')
        response.headers.add('Access-Control-Allow-Methods', 'GET, POST, DELETE, PUT, PATCH, OPTIONS')
        return response


  @app.route('/')
  def helloWorld():
        return 'Hello World'
  

  @app.route('/movies', methods=['GET'])
  @requires_auth('get:movies')
  def handle_fetch_movies(payload):
        
      try:
        movies = Movies.query.all()
        obj_movies = [{'id': movie.id,'title': movie.title, 'release_date': movie.release_date} for movie in movies]
        return jsonify({
        'success': True,
        'movies': obj_movies
        }),200
      
      except Exception  as e:
          print('error occurred!', e)
          abort(404)

  @app.route('/movie', methods = ['POST'])
  @requires_auth('post:movie')
  def handle_create_movie(payload):
      try:
          req = request.get_json()
          title = req['title']
          release_date = req['release_date']

          movie = Movies(title, release_date)

          if not all([title, release_date]):
                return jsonify({
                "success": False,
                "message": "Missing required fields!'."
            }), 400
          
          movie.insert()

          return jsonify({
                'success': True,
                'title': title,
                'release_date': release_date
            }), 201
      
      except Exception  as e:
          print('error occurred!', e)
          abort(404)

  @app.route('/movie/<int:id>', methods = ['GET'])
  @requires_auth('get:movies')

  def handle_fetch_one_movie(payload, id):
        try:
          movie = Movies.query.get(id)
          # print(movie)
          if movie is None:
            abort(404)
            
          return jsonify({
              "success": True, 
              "id":movie.id,
              "title":movie.title,
              "release_date":movie.release_date,
          }), 201

        except Exception as error:
          print(error)
          abort(404)

          
  @app.route('/movie/<int:id>', methods = ['PATCH'])
  @requires_auth('patch:movie')

  def handle_update_movie(payload, id):
        try:
          req = request.json
          title = req.get('title')
          release_date = req.get('release_date')
          
          movie = Movies.query.get(id)

          if movie is None:
            abort(404)

          if title:
              movie.title = title
          if release_date:
              movie.release_date = release_date

          Movies.update(movie) 

          return jsonify({"success": True, "message": 'the movie has been updated!'}), 201

        except Exception as error:
          print(error)
          abort(404)


  @app.route('/movie/<int:id>', methods = ['DELETE'])
  @requires_auth('delete:movie')
  def handle_delete_movie(payload, id):
    try:

        movie = Movies.query.get(id)
        if movie is None:
            abort(404)

        if movie is not None:
              Movies.delete(movie)
              return jsonify({"success": True, "message": 'specified movie has been deleted successfully '}), 201

    except Exception as error:

        print(error)
        abort(404)



#################


  @app.route('/actors', methods=['GET'])
  @requires_auth('get:actors')
  def handle_fetch_actor(payload):
        
      try:
        actors = Actors.query.all()
        obj_actor = [{'id': actor.id,'name': actor.name, 'gender': actor.gender, 'age': actor.age, 'movie_id':actor.movie_id} for actor in actors]
        return jsonify({
        'success': True,
        'actors': obj_actor
        })
      
      except Exception  as e:
          print('error occurred!', e)
          abort(404)


  @app.route('/actor/<int:id>', methods = ['GET'])
  @requires_auth('get:actors')
  def handle_fetch_one_actor(payload, id):
        try:
          actor = Actors.query.get(id)
          if actor is None:
            abort(404)

          return jsonify({
              "success": True, 
              "id":actor.id,
              "name":actor.name,
              "age":actor.age,
              "gender":actor.gender,
              "movie_id":actor.movie_id
          }), 200

        except Exception as error:
          print(error)
          abort(404)


  @app.route('/actor', methods = ['POST'])
  @requires_auth('post:actor')
  def handle_create_actor(payload):
      try:
          req = request.get_json()
          name = req.get('name')
          gender = req.get('gender')
          age = req.get('age')
          movie_id = req.get('movie_id')
          
          actor = Actors(name, gender, age, movie_id)

          if not all([name, gender, age, movie_id]):
                return jsonify({
                "success": False,
                "message": "Missing required fields!'."
            }), 400
          
          actor.insert()

          return jsonify({
                'success': True,
                'name': name,
                'gender': gender,
                'age': age,
                'movie_id': movie_id,
            }), 201
      
      except Exception  as e:
          print('error occurred!', e)
          abort(404)


  @app.route('/actor/<int:id>', methods = ['PATCH'])
  @requires_auth('patch:actor')
  def handle_update_actor(payload, id):
        try:
          req = request.json
          name = req.get('name')
          gender = req.get('gender')
          age = req.get('age')
          movie_id = req.get('movie_id')

          
          actor = Actors.query.get(id)

          if actor is None:
            abort(404)

          if name:
              actor.name = name

          if gender:
              actor.gender = gender

          if age:
              actor.age = age

          if movie_id:
              actor.movie_id = movie_id

          Actors.update(actor) 

          return jsonify({"success": True, "message": 'actor has been updated'}), 201

        except Exception as error:
          print(error)
          abort(404)


  @app.route('/author/<int:id>', methods = ['DELETE'])
  @requires_auth('delete:actor')
  def handle_delete_actor(payload, id):
    try:

        actor = Actors.query.get(id)
        if actor is None:
            abort(404)

        if actor is not None:
              Actors.delete(actor)
              return jsonify({"success": True, "message": 'specified actor has been deleted successfully '}), 201

    except Exception as error:

        print(error)
        abort(404)


  # error handlers

  @app.errorhandler(400)
  def badRequest(error):
      return jsonify({
        'success': False,
        'error': 400,
        'message': 'Bad Request'
    }), 400

  @app.errorhandler(404)
  def notFound(error):
      return jsonify({
        'success': False,
        'error': 404,
        'message': 'Resource not found'
    }), 404

  @app.errorhandler(422)
  def UnprocessableContent(error):
      return jsonify({
        'success': False,
        'error': 422,
        'message': 'Unprocessable Content'
    }), 422

  @app.errorhandler(500)
  def InternalServerError(error):
       return jsonify({
        'success': False,
        'error': 500,
        'message': 'Internal Server Error'
    }), 500

  return app

app = create_app()



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)