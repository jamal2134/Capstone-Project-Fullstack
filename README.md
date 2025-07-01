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

### @app.route("/movies", methods=['GET'])

* Here all user can get the data as json file
* Return The Movies Data

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



