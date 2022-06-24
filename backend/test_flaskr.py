import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category


class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.db_username = "kenory"
        self.db_host = "localhost:5432"
        self.db_password = 'kenory'
        self.database_path = "postgresql://{}:{}@{}/{}".format(self.db_username, self.db_password, self.db_host, self.database_name)

        #self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)

        setup_db(self.app, self.database_path)

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

        self.new_question = {
            "question": "What is your name?", 
            "answer": "Kenneth Afegbai", 
            "difficulty": "5",
            "category":"1"
            }
    
    
    def tearDown(self):
        """Executed after reach test"""
        pass

#test to confirm paginated questions - success(200)
    def test_200_get_paginated_questions(self):
        res = self.client().get("/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["total_questions"])
        self.assertTrue(len(data["questions"]))

#test to confirm invalid paginated - resource not found (404)
    def test_404_requesting_invalid_page(self):
        res = self.client().get("/questions?page=1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

#test to confirm submitted questions - success(200)
    def test_create_new_Question(self):
        res = self.client().post("/questions", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["added"])

#test to confirm failed submitted question - method not allowed(405)
    def test_405_submit_question_not_allowed(self):
        res = self.client().post("/questions/1", json=self.new_question)
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

#test to confirm successful deleted question - success(200)
    def test_200_delete_question(self):
        res = self.client().delete("/questions/6")
        data = json.loads(res.data)

        question = Question.query.filter(Question.id == 6).one_or_none()

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertEqual(data["deleted"], 6)
        self.assertTrue(data["message"], "delete successful")

#test to confirm delete question id does not exist - resource not found(404)
    def test_404_delete_question_not_existing(self):
        res = self.client().delete("/questions/1000")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertTrue(data["message"], "Resource not found")

#test to confirm search question was successful - success(200)
    def test_200_search_question_exist(self):
        res = self.client().post("/questions", json={"searchTerm":"title"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["totalQuestions"])
        self.assertTrue(len(data["questions"]))

#test to confirm search question was not successful - resource not found(404)
    def test_404_if_search_question_does_not_exist(self):
        res = self.client().post("/questions", json={"searchTerm":"wow"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 404)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Resource not found")

#test to confirm categories were retrieved successfully - success(200)
    def test_get_categories(self):
        res = self.client().get("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["categories"])


#test to confirm method not allowed in categories - method not allowed(405)
    def test_405_categories_method_not_allowed(self):
        res = self.client().post("/categories")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

#test to confirm questions by categories were retrieved successfully - success(200)
    def test_200_questions_by_category(self):
        res = self.client().get("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertEqual(data["success"], True)
        self.assertTrue(data["questions"])
        self.assertTrue(data["totalQuestions"])

#test to confirm method not allowed in questions by categories - method not allowed(405)
    def test_405_questions_by_category_method_not_allowed(self):
        res = self.client().post("/categories/4/questions")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")

#test to confirm randomly selected quiz is retrieved successfully - success(200)
    def test_200_quiz(self):
        res = self.client().post("/quizzes", json={"previous_questions":[1, 3, 4, 10], "quiz_category":"4"})
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 200)
        self.assertTrue(data["question"])

#test to confirm method not allowed in quizzes - method not allowed(405)
    def test_405_quiz_method_not_allowed(self):
        res = self.client().get("/quizzes")
        data = json.loads(res.data)

        self.assertEqual(res.status_code, 405)
        self.assertEqual(data["success"], False)
        self.assertEqual(data["message"], "Method not allowed")


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()