import os
from flask import Flask, request, jsonify, abort
from sqlalchemy import exc
import json
from flask_cors import CORS

from models import setup_db, Movies, Actors
from auth import AuthError, requires_auth

  

def create_app(test_config=None):
  # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.after_request 
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headets', 'Content-Type, Authorization')
        response.headers.add('Access-Control-Allow-Headets', 'GET, POST,PATCH, DELETE,OPTIONS')
        return response

    ## ROUTES
    ##Movies

    @app.route('/movies', methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(jwt):
        try:    
            movies = Movies.query.all()
            return jsonify({'success': True, 'movies': [movie.format() for movie in movies ]})
        except:
            abort(500)


    @app.route('/movies', methods=['POST'])
    @requires_auth('post:movies')
    def create_new_movie(jwt):

        data = request.get_json()
        title=data.get('title')
        release_date=data.get('release_date')
        try:
            title=data.get('title')
            release_date=data.get('release_date')
            newMovie = Movies(title=title,release_date=release_date)
            newMovie.insert()

            return jsonify({'success': True, 'movies': [newMovie.format()]}),200

        except Exception as e:
  
            abort(500)

    @app.route('/movies/<int:movie_id>', methods=['DELETE'])
    @requires_auth('delete:movies')
    def delete_movie(jwt, movie_id):
        movie = Movies.query.filter_by(id=movie_id).one_or_none()

        if movie is None:
            return (jsonify({'success': False, 'error': 404,
                    'message': 'Movie #{} not found.'.format(movie_id)}),
                    404)
        try:
            movie.delete()
        except exc.SQLAlchemyError:
            # return internal server error if couldn't delete record
            abort(500)

        return jsonify({'success': True, 'delete': movie_id})



    @app.route('/movies/<int:movie_id>', methods=['PATCH'])
    @requires_auth('patch:movies')
    def patch_movies(jwt, movie_id):
        movie = Movies.query.filter_by(id=movie_id).one_or_none()
        if movie is None:
            # Movie with ID is not found
            return (jsonify({'success': False, 'error': 404,
                    'message': 'Movie #{} not found.'.format(movie_id)}),
                    404)
        data = request.get_json()
        if data.get('title', '') != '':
            movie.title = data.get('title', '')

        if data.get('release_date', '') != '':
            movie.release_date = data.get('release_date', '')
        movie.update()
        return jsonify({'success': True, 'movies': [movie.format()]})


    ##Actors
    @app.route('/actors', methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(jwt):
        try:
            actors = Actors.query.all()
            return jsonify({'success': True, 'actors': [actor.format() for actor in actors]})
        except:
            abort(500)

            
    @app.route('/actors', methods=['POST'])
    @requires_auth('post:actors')
    def create_new_actor(jwt):

        data = request.get_json()
        newActor = Actors(name = data.get('name',''),
                        age=data.get('age', ''),
                        gender=data.get('gender', ''))

        try:
            newActor = Actors(name = data.get('name',''),
                        age=data.get('age', ''),
                        gender=data.get('gender', ''))

            newActor.insert()
            return jsonify({'success': True, 'actors': [newActor.format()]}),200

        except:
            abort(500)

    @app.route('/actors/<int:actor_id>', methods=['DELETE'])
    @requires_auth('delete:actors')
    def delete_actor(jwt, actor_id):
        actor = Actors.query.filter_by(id=actor_id).one_or_none()

        if actor is None:
            return (jsonify({'success': False, 'error': 404,
                    'message': 'Actor #{} not found.'.format(actor_id)}),
                    404)
        try:
            actor.delete()
        except exc.SQLAlchemyError:
            # return internal server error if couldn't delete record
            abort(500)

        return jsonify({'success': True, 'delete': actor_id})



    @app.route('/actors/<int:actor_id>', methods=['PATCH'])
    @requires_auth('patch:actors')
    def patch_actors(jwt, actor_id):

        actor = Actors.query.filter_by(id=actor_id).one_or_none()
        if actor is None:
            # actor with ID is not found
            return (jsonify({'success': False, 'error': 404,
                    'message': 'Actor #{} not found.'.format(actor_id)}),
                    404)
                
        data = request.get_json()
        if data.get('name', '') != '':
            actor.name = data.get('name', '')
        if data.get('age', '') != '':
            actor.age = data.get('age', '')
        if data.get('gender', '') != '':
            actor.gender = data.get('gender', '')
        try:

            actor.update()

            return jsonify({'success': True, 'actors': [actor.format()]})
        except:
            abort(500)


    ## Error Handling

    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unprocessable'}), 422)
    @app.errorhandler(422)
    def unprocessable(error):
        return (jsonify({'success': False, 'error': 422,
                'message': 'unprocessable'}), 422)


    @app.errorhandler(400)
    def error_400(e):
        return (jsonify({'success': False, 'error': 400,
                'message': 'Bad Request'}), 400)


    @app.errorhandler(404)
    def error_404(e):
        return (jsonify({'success': False, 'error': 404,
                'message': 'Resource not found'}), 404)


    @app.errorhandler(500)
    def error_500(e):
        return (jsonify({'success': False, 'error': 500,
                'message': 'internal server error'}), 500)


    @app.errorhandler(AuthError)
    def auth_error(error):
        return (jsonify({'success': False, 'error': error.status_code,
                'message': error.error.get('description', 'unknown error'
                )}), error.status_code)
    return app