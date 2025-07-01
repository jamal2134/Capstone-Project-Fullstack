import unittest
import json
from app import create_app
from .database.models import db


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

        self.database_path = os.environ['DATABASE_URL']
        if self.database_path.startswith("postgres://"):
            self.database_path = database_path.replace("postgres://", "postgresql://", 1)

        # Create app with the test configuration
        self.app = create_app({
            "SQLALCHEMY_DATABASE_URI": self.database_path,
            "SQLALCHEMY_TRACK_MODIFICATIONS": False,
            "TESTING": True
        })
        self.client = self.app.test_client()

        self.new_movie = {"title": "Eternal Sunshine of the Spotless Mind", "release_date": "March 19, 2004"}
        self.new_actor = {"name": "Jim Carrey", "age":"63", "gender": 'male'}
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
    #test index page success
    def test_index_page(self):
        res = self.client.get("/")
        self.assertEqual(res.status_code, 200)
        data = json.loads(res.data)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['greeting'], "Hello You are now in Project Full Stack Capstone.")

    #test get movies success
    def test_get_movies(self):
        res = self.client.get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))
    #test get movies failure
    def test_get_movies_failure(self):
        res = self.client.get("/movies")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    #test get movies success
    def test_get_movies_details(self):
        res = self.client.get("/movies-details")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["movies"]))

    # test get movies success
    def test_get_actors(self):
        res = self.client.get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    #test get actors failure
    def test_get_actors_failure(self):
        res = self.client.get("/actors")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "resource not found")


    # test get movies success
    def test_get_actors_details(self):
        res = self.client.get("/actors-details")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        # self.assertEqual(data["success"], True)
        self.assertTrue(len(data["actors"]))

    def test_add_new_movie(self):
        res = self.client.post("/movies", json=self.new_movie)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        # test get actors failure

    def test_add_movie_failure(self):
        res = self.client.post("/movies", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_add_new_actor(self):
        res = self.client.post("/actors", json=self.new_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_add_actor_failure(self):
        res = self.client.post("/actors", json={})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_add_new_relationship(self):
        res = self.client.post("/movies-actors", json=self.new_movie_actor)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
    # test_add_new_relationship failure
    def test_add_new_relationship_failure(self):
        res = self.client.post("/movies-actors", json={"movies_id": 1})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 422)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "unprocessable")

    def test_update_movie(self):
        res = self.client.patch("/movies/1", json={"title":"YOYO2030"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_update_actor(self):
        res = self.client.patch("/actors/1", json={"age":"63"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)

    def test_delete_movie(self):
        res = self.client.delete("/movies/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)


    def test_delete_actor(self):
        res = self.client.delete("/actors/1")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)



if __name__ == '__main__':
    unittest.main()
