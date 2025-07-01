from flask import Flask, request, abort, jsonify, redirect
from models import *
from flask_cors import CORS
from auth import AuthError, requires_auth


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__)
    setup_db(app)
    CORS(app)

    @app.route('/')
    def goto_signin():
        # excited = os.environ['EXCITED']
        Domain = "dev-ht2o42qwj0gy43i8.us.auth0.com"
        Client_ID = "CLJJSxZslRDQNLgHjZOBefrX8iX9YrDQ"
        url_goback = 'http://localhost:5000/movies'
        audience = 'Capstone'

        url = f'https://{Domain}/authorize?audience={audience}&response_type=token&client_id={Client_ID}&redirect_uri={url_goback}'

        return redirect(url)

    @app.route("/movies", methods=['GET'])
    @requires_auth('get:movies')
    def get_movies(payload):
        print("movies")

        movies = Movies.query.all()

        if len(movies) == 0:
            abort(404)

        movies = [movie.format() for movie in movies]
        print(movies)
        return jsonify(
            {
                "success": True,
                "movies": movies
            }
        )

    @app.route("/movies-details", methods=['GET'])
    @requires_auth('get:movies-details')
    def get_movies_details(payload):
        movies = Movies.query.all()
        if len(movies) == 0:
            abort(404)

        try:

            list_movies = [movie.format() for movie in movies]
            list_actors = [movie.actors for movie in movies]

            for itemM, itemA in zip(list_movies, list_actors):
                list_Moives_Actors = []
                for i in range(len(itemA)):
                    actor = Actors.query.get(itemA[i].actor_id)
                    list_Moives_Actors.append(actor.format())
                itemM.update({"list Actors": list_Moives_Actors})
        except:
            abort(404)

        return jsonify(
            {
                "success": True,
                "movies": list_movies
            }
        )

    @app.route("/actors", methods=['GET'])
    @requires_auth('get:actors')
    def get_actors(payload):
        actors = Actors.query.all()
        if len(actors) == 0:
            abort(404)

        actors = [actor.format() for actor in actors]

        return jsonify(
            {
                "success": True,
                "actors": actors
            }
        )

    @app.route("/actors-details", methods=['GET'])
    @requires_auth('get:actors-details')
    def get_actors_details(payload):
        actors = Actors.query.all()
        if len(actors) == 0:
            abort(404)

        try:
            list_actors = [actor.format() for actor in actors]
            list_movies = [actor.movies for actor in actors]

            for itemA, itemM in zip(list_actors, list_movies):
                list_Actors_Moives = []
                for i in range(len(itemM)):
                    movie = Movies.query.get(itemM[i].movie_id)
                    list_Actors_Moives.append(movie.format())
                itemA.update({"list_movies": list_Actors_Moives})

            return jsonify(
                {
                    "success": True,
                    "actors": list_actors
                }
            )
        except:
            abort(404)

    @app.route("/movies", methods=['POST'])
    @requires_auth('post:movies')
    def add_movie(payload):
        body = request.get_json()

        title = body.get("title", None)
        release_date = body.get("release_date", None)
        # print(title)
        # print(release_date)
        try:
            movie = Movies(title=title, release_date=release_date)
            movie.insert()

            data = movie.format()
            return jsonify(
                {
                    "success": True,
                    "data": data

                }
            )

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/actors", methods=['POST'])
    @requires_auth('post:actors')
    def add_actor(payload):
        body = request.get_json()

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)

        try:
            actor = Actors(name=name, age=age, gender=gender)
            actor.insert()
            data = actor.format()
            return jsonify(
                {
                    "success": True,
                    "data": data

                }
            )

        except:
            abort(422)

    @app.route("/movies-actors", methods=['POST'])
    @requires_auth('post:movies-actors')
    def add_relationship_movies_actors(payload):
        body = request.get_json()

        movie_id = body.get("movie_id", None)
        actor_id = body.get("actor_id", None)

        if actor_id is None or movie_id is None:
            abort(422)

        try:

            movie_actor = Movies_actors()

            movie_actor.movie_id = movie_id
            print(movie_id, actor_id)
            movie_actor.actor_id = actor_id

            db.session.add(movie_actor)
            db.session.commit()

            return jsonify(
                {
                    "success": True

                }
            )

        except Exception as e:
            print(e)
            abort(422)

    @app.route("/movies/<int:id>", methods=["PATCH"])
    @requires_auth('patch:movies')
    def update_movie(payload, id):
        if id is None:
            abort(404)

        current_Movie = Movies.query.filter(Movies.id == id).one_or_none()

        body = request.get_json()

        title = body.get("title", None)
        release_date = body.get("release_date", None)

        if current_Movie is None:
            abort(404)

        try:
            if title is not None:
                current_Movie.title = title

            if release_date is not None:
                current_Movie.release_date = release_date
            print(title, release_date)
            current_Movie.update()

            return jsonify(
                {
                    "success": True,
                    "Movie": current_Movie.format()
                }
            )
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/actors/<int:id>", methods=["PATCH"])
    @requires_auth('patch:actors')
    def update_actor(payload, id):
        if id is None:
            abort(404)
        current_Actor = Actors.query.filter(Actors.id == id).one_or_none()

        body = request.get_json()

        name = body.get("name", None)
        age = body.get("age", None)
        gender = body.get("gender", None)

        if current_Actor is None:
            abort(404)

        try:
            if name is not None:
                current_Actor.name = name
            if age is not None:
                current_Actor.age = age
            if gender is not None:
                current_Actor.gender = gender

            current_Actor.update()

            return jsonify(
                {
                    "success": True,
                    "Actor": current_Actor.format()
                }
            )
        except:
            abort(422)

    @app.route("/movies/<int:id>", methods=["DELETE"])
    @requires_auth('delete:movies')
    def delete_movie(payload, id):
        if id is None:
            abort(404)
        current_Movie = Movies.query.filter(Movies.id == id).one_or_none()

        realationship_item = Movies_actors.query.filter(Movies_actors.movie_id == id).one_or_none()

        print(realationship_item)
        print(current_Movie)

        try:
            for item in realationship_item:
                db.session.delete(item)
                db.session.commit()
        except:
            db.session.delete(realationship_item)
            db.session.commit()

        if current_Movie is None:
            abort(404)

        try:

            current_Movie.delete()

            return jsonify(
                {
                    "success": True,
                    "delete": id
                }
            )
        except Exception as e:
            print(e)
            abort(422)

    @app.route("/actors/<int:id>", methods=["DELETE"])
    @requires_auth('delete:actors')
    def delete_actor(payload, id):
        if id is None:
            abort(404)
        current_Actor = Actors.query.filter(Actors.id == id).one_or_none()



        try:
            realationship_item = Movies_actors.query.filter(Movies_actors.actor_id == id).one_or_none()
            try:
                for item in realationship_item:
                    db.session.delete(item)
                    db.session.commit()
            except:
                db.session.delete(realationship_item)
                db.session.commit()
        except:
            print("We don't find ID")


        if current_Actor is None:
            abort(404)

        try:

            current_Actor.delete()

            return jsonify(
                {
                    "success": True,
                    "delete": id
                }
            )
        except Exception as e:
            print(e)
            abort(422)

    '''
    Example error handling for unprocessable entity
    '''

    @app.errorhandler(422)
    def unprocessable(error):
        return jsonify({
            "success": False,
            "error": 422,
            "message": "unprocessable"
        }), 422

    '''
    @TODO implement error handlers using the @app.errorhandler(error) decorator
        each error handler should return (with approprate messages):
                 jsonify({
                        "success": False,
                        "error": 404,
                        "message": "resource not found"
                        }), 404

    '''

    @app.errorhandler(404)
    def resource_not_found(error):
        return jsonify({
            "success": False,
            "error": 404,
            "message": "resource not found"
        }), 404

    '''
    @TODO implement error handler for 404
        error handler should conform to general task above
    '''

    @app.errorhandler(405)
    def not_found(error):
        return (
            jsonify({"success": False, "error": 405, "message": "method not allowed"}),
            405,
        )

    '''
    @TODO implement error handler for AuthError
        error handler should conform to general task above
    '''

    @app.errorhandler(AuthError)
    def auth_error(error):
        return jsonify({
            "success": False,
            "error": error.status_code,
            "message": error.error['description']
        }), error.status_code

    return app


APP = create_app()

if __name__ == '__main__':
    APP.run(host='0.0.0.0', port=8080, debug=True)
