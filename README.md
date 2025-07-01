# Capstone-Project-Fullstack

The Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies. You are an Executive Producer within the company and are creating a system to simplify and streamline your process.

## Create Models

* Movies with attributes title and release date
* Actors with attributes name, age and gender
* Realatioship between Movies & Actors

## Add Endpoints:
* GET /actors and /movies
* DELETE /actors/ and /movies/
* POST /actors and /movies and
* PATCH /actors/ and /movies/

## Add Roles:
* Casting Assistant
    * Can view actors and movies
* Casting Director
    * All permissions a Casting Assistant has and…
    * Add or delete an actor from the database
    * Modify actors or movies
* Executive Producer
    * All permissions a Casting Director has and…
    * Add or delete a movie from the database

## Create Test Python File

* One test for success behavior of each endpoint
* One test for error behavior of each endpoint
* At least two tests of RBAC for each role

## Run Localy

### Install Python Dependencies

```bash
pip install requirements.txt
```

### Insert Your Postgres Database Details in models file
* database_name
* database_user
* database_password
* database_host

### Insert Your Auth0 Details in auth file

* AUTH0_DOMAIN
* ALGORITHMS
* API_AUDIENCE

### Set Up Url of Auth0
* Domain
* Client_ID
* url_goback
* audience


### Set up the environment

```bash
export FLASK_APP=app
export FLASK_DEBUG=1
```

In Windows 
```bash
set FLASK_APP=app
set FLASK_DEBUG=1
```

### Run Python file

```bash
flask run
```

### @app.route('/')

We need to retrun the url of auth0 for take the access token after sign in from new url

### We will use postman for send the request with 

### POST Request

### @app.route("/movies", methods=['POST'])

* Here only Executive Producer can post the data as json file
* Add New movie to database

```json
{
    "title":"insert the title here",
    "release_date":"Insert the release_date here"
}
```

* Retrun
  
```json
{
    "data": {
        "id": 5,
        "release_date": "01/02/2025",
        "title": "test"
    },
    "success": true
}
```

### @app.route("/actors", methods=['POST'])

* Here only Executive Producer and Casting Director can post the data as json file
* Add New actor to database
```json
{
    "name":"insert the Name here",
    "age":"Insert the age here",
    "gender":"Insert the gender here",
}
```

* Retrun
  
```json
{
    "data": {
        "id": 5,
        "name": "name",
        "age": "age",
        "gender": "gender"
    },
    "success": true
}
```

### @app.route("/movies-actors", methods=['POST'])

* Here only Executive Producer and Casting Director can post the data as json file
* Add New realationship to database
* Insert actual id of movie and actor already added to database
```json
{
    "movie_id":1,
    "actor_id":2
}
```

* Retrun
  
```json
{
    "success": true
}
```

### GET Request

### @app.route("/movies", methods=['GET'])

* Here all user can get the data as json file
* Return The Movies Data
```json
{
    "movies": [
        {
            "id": 2,
            "release_date": "20/12/2000",
            "title": "Film 2"
        },
        {
            "id": 4,
            "release_date": "10/05/2005",
            "title": "Film 4"
        },
        {
            "id": 1,
            "release_date": "20/10/2010",
            "title": "Film 1"
        },
        {
            "id": 3,
            "release_date": "20/12/2015",
            "title": "Film 3"
        }
    ],
    "success": true
}
```

### @app.route("/actors", methods=['GET'])
* Here all user can get the data as json file
* Return The Actors Data
* 
```json
{
    "actors": [
        {
            "age": "35",
            "gender": "male",
            "id": 2,
            "name": "John"
        },
        {
            "age": "20",
            "gender": "female",
            "id": 4,
            "name": "Karmen"
        },
        {
            "age": "29",
            "gender": "male",
            "id": 1,
            "name": "Jamal"
        },
        {
            "age": "40",
            "gender": "male",
            "id": 3,
            "name": "Mark"
        }
    ],
    "success": true
}
```

### @app.route("/movies-details", methods=['GET'])

* Here all user can get the data as json file
* Return each movie with their actors

```json
{
    "movies": [
        {
            "id": 1,
            "list Actors": [
                {
                    "age": "29",
                    "gender": "male",
                    "id": 1,
                    "name": "Jamal"
                }
            ],
            "release_date": "20/10/2010",
            "title": "Film 1"
        },
        {
            "id": 2,
            "list Actors": [
                {
                    "age": "40",
                    "gender": "male",
                    "id": 3,
                    "name": "Mark"
                }
            ],
            "release_date": "20/12/2000",
            "title": "Film 2"
        },
        {
            "id": 3,
            "list Actors": [
                {
                    "age": "35",
                    "gender": "male",
                    "id": 2,
                    "name": "John"
                }
            ],
            "release_date": "20/12/2015",
            "title": "Film 3"
        },
        {
            "id": 5,
            "list Actors": [],
            "release_date": "01/02/2025",
            "title": "test"
        },
        {
            "id": 4,
            "list Actors": [],
            "release_date": "10/05/2005",
            "title": "Film 4"
        }
    ],
    "success": true
}
```

### @app.route("/actors-details", methods=['GET'])

* Here all user can get the data as json file
* Return each actor with their movies

```json
{
    "actors": [
        {
            "age": "29",
            "gender": "male",
            "id": 1,
            "list_movies": [
                {
                    "id": 1,
                    "release_date": "20/10/2010",
                    "title": "Film 1"
                }
            ],
            "name": "Jamal"
        },
        {
            "age": "40",
            "gender": "male",
            "id": 3,
            "list_movies": [
                {
                    "id": 2,
                    "release_date": "20/12/2000",
                    "title": "Film 2"
                }
            ],
            "name": "Mark"
        },
        {
            "age": "35",
            "gender": "male",
            "id": 2,
            "list_movies": [
                {
                    "id": 3,
                    "release_date": "20/12/2015",
                    "title": "Film 3"
                }
            ],
            "name": "John"
        },
        {
            "age": "20",
            "gender": "female",
            "id": 4,
            "list_movies": [],
            "name": "Karmen"
        }
    ],
    "success": true
}
```

###  @app.route("/movies/<int:id>", methods=["PATCH"])

* Here only Executive Producer and Casting Director can patch the data as json file

###  @app.route("/actors/<int:id>", methods=["PATCH"])

* Here only Executive Producer and Casting Director can patch the data as json file

###  @app.route("/movies/<int:id>", methods=["DELETE"])

* Here only Executive Producer can delete the data 

###  @app.route("/actors/<int:id>", methods=["DELETE"])

* Here only Executive Producer and Casting Director can delete the data

## Test file

you will find in `test_flaskr.py` all the cmd of test

## Upload The File To Github For Connect with Render For Deploy 

1. Create file setup.sh
2. Create file runtime.txt
3. Create file Procfile

* Connect The github account with render
* Create database then add deteils in model
* Create Project web serve and connect github repository
* Deploy The Project

### And This is my Url 

```
https://capstone-project-fullstack-83pg.onrender.com
```










