import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from flaskr import create_app
from models import setup_db, Question, Category

"""
  Copy existing database from trivia database to create a testing database
  for developing purposes.
  Psql commands: CREATE DATABASE targetdb WITH TEMPLATE source;
"""

class TriviaTestCase(unittest.TestCase):
    """This class represents the trivia test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = create_app()
        self.client = self.app.test_client
        self.database_name = "trivia_test"
        self.database_path = "postgres://{}/{}".format('localhost:5432', self.database_name)
        setup_db(self.app, self.database_path)

        # Test new question success
        self.new_question_success= {
            'question':'In what state was Barack Obama born in?',
            'answer':'Hawaii',
            'category':'History',
            'difficulty': 2
        }
        # Test new question failure
        self.new_question_fail = {
            'quote':'Come with me if you want to live',
            'person': 'Arnold SwarSchwarzenegger',
            'movie':'Terminator'
        }

        # Test search query success
        self.search_query = {
            "searchTerm": "president"
        }

        # Test search query failure
        self.search_query_failure = {
            "Unprocessable": "Not required"
        }

        # Test play quiz with science category
        self.play_category = {
            "quiz_category": {
                "type": "Science",
                "id": 0
            },
            "previous_questions": []
        }

        # Test play quiz with category failure
        self.play_category_failure = {
            "quiz_category": {"type": "fail"},
            "previous_question": []
        }

        # Test rating question update success
        self.rating = {
            "id": 3,
            "rating": 3
        }

        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()

    def tearDown(self):
        """Executed after reach test"""
        pass

    """
    TODO
    Write at least one test for each test for successful operation and for expected errors.
    """
    #============== GET /questions?page=1 ===================
    #========================================================

    # Sucess
    def test_paginated_questions(self):
        response = self.client().get('/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['total_questions'])
        self.assertTrue(data['categories'])
        self.assertTrue(data['currentCategory'])

    # Failure
    def test_404_for_questions_not_found(self):
        response = self.client().get('/questions?page=300')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Questions not found')

    #======================================================
    #======================================================

    #========= DELETE /questions/<int:book_id> ==============
    #========================================================

    # Success
    def test_delete_question_success(self):
        response = self.client().delete('/questions/49')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)

    # Failure
    def test_delete_question_failure(self):
        response = self.client().delete('/questions/23233')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertEqual(data['message'], 'Request unprocessable')


    #======================================================
    #======================================================

    #=============== POST /questions ========================
    #========================================================

    # Success
    def test_new_question_success(self):
        response = self.client().post('/questions', json=self.new_question_success)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['created'])
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    # Failure
    def test_new_question_failure(self):
        response = self.client().post('/questions', json=self.new_question_fail)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Request unprocessable')

    #======================================================
    #======================================================

    #=============== SEARCH POST /questions ========================
    #========================================================

    # Success
    def test_search_query_success(self):
        response = self.client().post('/questions', json=self.search_query)
        data = json.loads(response.data)
        print(data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    # Failure
    def test_search_query_failure(self):
        response = self.client().post('/questions', json=self.search_query_failure)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Request unprocessable')

    #======================================================
    #======================================================

    #========= GET /category/<category>/questions ===========
    #========================================================

    # Success
    def test_get_category_questions_success(self):
        # Test a category in the database. In this case it's Science
        response = self.client().get('/categories/Science/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['questions'])
        self.assertTrue(data['total_questions'])

    # Failure
    def test_get_category_questions_failure(self):
        response = self.client().get('/category/Business/questions')
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not found')

    #======================================================
    #======================================================

    #========= POST /quizzes ===========
    #========================================================
    # Success
    def test_play_quiz_success(self):
        # Test a category in the database. In this case it's Science
        response = self.client().post('/quizzes', json=self.play_category)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertTrue(data['question'])
        self.assertTrue(data['questions_per_play'])

    # Failure
    def test_play_quiz_failure(self):
        response = self.client().post('/quizzes', json=self.play_category_failure)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 422)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Request unprocessable')

    #======================================================
    #======================================================

    #========= PATCH /questions/<int:question_id> ===========
    #========================================================
    # Success
    def test_question_update_rating_success(self):
        # Test a category in the database. In this case it's Science
        response = self.client().patch('/questions/55', json=self.rating)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(data['success'], True)
        self.assertEqual(data['id'], 55)

    # Failure
    def test_question_update_rating_failure(self):
        response = self.client().patch('/questions/5e5', json=self.rating)
        data = json.loads(response.data)

        self.assertEqual(response.status_code, 404)
        self.assertEqual(data['success'], False)
        self.assertTrue(data['message'], 'Not found')

    #======================================================
    #======================================================

# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()