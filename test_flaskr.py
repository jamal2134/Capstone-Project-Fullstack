import unittest
import json
from app import create_app
from models import db
import os

ASSISTANT_TOKEN = os.environ['ASSISTANT_TOKEN']
DIRECTOR_TOKEN = os.environ['DIRECTOR_TOKEN']
PRODUCER_TOKEN = os.environ['Producer']


class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        # self.database_name = DB_NAME_TEST
        # self.database_user = DB_USER
        # self.database_password = DB_PASSWORD
        self.database_name = 'postgres_test'
        self.database_user = 'postgres'
        self.database_password = 123
        self.database_host = "localhost:5432"
        self.database_path = f"postgresql://{self.database_user}:{self.database_password}@{self.database_host}/{self.database_name}"

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        self.new_movie = {"title": "Eternal Sunshine of the Spotless Mind", "release_date": "March 19, 2004"}
        self.new_actor = {"name": "Jim Carrey", "age": "63", "gender": 'male'}
        self.new_movie_actor = {"movies_id": 1, "actors_id": 1}

        # Bind the app to the current context and create all tables
        with self.app.app_context():
            db.create_all()

    def tearDown(self):
        """Executed after each test"""
        with self.app.app_context():
            pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """

    # test index page success
    def test_index_page(self):
        res = self.client.get("/")  # No Authorization header
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['greeting'], "Hello You are now in Project Full Stack Capstone.")

    # test get movies success
    def test_get_movies(self):
        res = self.client.get("/movies", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'}) # ASSISTANT_TOKEN has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    # test get movies failure
    def test_get_movies_failure(self):
        res = self.client.get("/movies")  # Without Authorization header
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    # test get movies success
    def test_get_movies_details(self):
        res = self.client.get("/movies-details", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'}) # ASSISTANT_TOKEN has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    # test get movies success
    def test_get_actors(self):
        res = self.client.get("/actors", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'})  # ASSISTANT_TOKEN has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    # test get actors failure
    def test_get_actors_failure(self):
        res = self.client.get("/actors")  # Without Authorization header
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    # test get movies success
    def test_get_actors_details(self):
        res = self.client.get("/actors-details", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'})  # ASSISTANT_TOKEN has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_add_new_movie(self):
        res = self.client.post("/movies", headers={
            'Authorization': f'Bearer {PRODUCER_TOKEN}'}, json=self.new_movie)  # PRODUCER_TOKEN has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # test get actors failure

    def test_add_movie_failure(self):
        res = self.client.post("/movies", headers={
            'Authorization': f'Bearer {PRODUCER_TOKEN}'}, json={})  # PRODUCER_TOKEN has authorized but without data
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_cannot_add_movie_failure(self):
        res = self.client.post("/movies", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json=self.new_movie)  # DIRECTOR_TOKEN doesn't has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    def test_add_new_actor(self):
        res = self.client.post("/actors", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json=self.new_actor)  # DIRECTOR_TOKEN  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_actor_failure(self):
        res = self.client.post("/actors", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json={})  # DIRECTOR_TOKEN has authorized but without data
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_cannot_add_actor_failure(self):
        res = self.client.post("/actors", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'},
                               json=self.new_movie)  # ASSISTANT_TOKEN doesn't has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    def test_add_new_relationship(self):
        res = self.client.post("/movies-actors", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json=self.new_movie_actor)# DIRECTOR_TOKEN  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    # test_add_new_relationship failure
    def test_add_new_relationship_failure(self):
        res = self.client.post("/movies-actors", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json={})# DIRECTOR_TOKEN  has authorized  but without data
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_movie(self):
        res = self.client.patch("/movies/1", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json={"title": "YOYO2030"})# DIRECTOR_TOKEN  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_cannot_update_movie(self):
        res = self.client.patch("/movies/1", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'}, json={"title": "YOYO2030"})# ASSISTANT_TOKEN doesn't  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    def test_update_actor(self):
        res = self.client.patch("/actors/1", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'}, json={"age": "63"})# DIRECTOR_TOKEN  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_cannot_update_actor(self):
        res = self.client.patch("/actors/1", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'}, json={"title": "YOYO2030"})# ASSISTANT_TOKEN doesn't  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    def test_delete_movie(self):
        res = self.client.delete("/movies/1", headers={
            'Authorization': f'Bearer {PRODUCER_TOKEN}'})# PRODUCER_TOKEN  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_cannot_delete_movie(self):
        res = self.client.delete("/movies/1", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'})# DIRECTOR_TOKEN doesn't  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")

    def test_delete_actor(self):
        res = self.client.delete("/actors/1", headers={
            'Authorization': f'Bearer {DIRECTOR_TOKEN}'})# DIRECTOR_TOKEN  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_cannot_delete_actor(self):
        res = self.client.delete("/actors/1", headers={
            'Authorization': f'Bearer {ASSISTANT_TOKEN}'})# ASSISTANT_TOKEN doesn't  has authorized
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 401)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Unauthorized")


if __name__ == '__main__':
    unittest.main()
