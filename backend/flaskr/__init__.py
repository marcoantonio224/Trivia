import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category


def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  CORS(app)

  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET, PUT, POST, DELETE, OPTIONS')
    return response
  '''
  @TODO:
  Create an endpoint to handle GET requests
  for all available categories.
  '''
  @app.route('/categories')
  def get_categories():
    categories = Category.query.all()
    categories_serialized = [category.format()['type'] for category in categories]

    return jsonify({
      'success': True,
      'categories': categories_serialized
    })

  QUESTIONS_PER_PAGE = 10
  # Paginate the questions helper function
  def paginate_questions(request, questions):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE
    questions = [question.format() for question in questions]
    current_questions = questions[start:end]
    return current_questions

  '''
  @TODO:
  Create an endpoint to handle GET requests for questions,
  including pagination (every 10 questions).
  This endpoint should return a list of questions,
  number of total questions, current category, categories.

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions.
  '''
  # GET questions (paginated by 10 questions)
  @app.route('/questions')
  def get_questions():
    # Grab all questions from database
    questions = Question.query.order_by(Question.id).all()
    # Paginate the questions by helper function
    current_questions = paginate_questions(request, questions)
    # Grab all the categories from database and serialize them
    categories = Category.query.order_by(Category.id).all()
    categories_serialized = [category.format()['type'] for category in categories]

    if len(current_questions) == 0:
      # Questions not found
      abort(404)

    return jsonify({
      'success': True,
      'questions': current_questions,
      'total_questions': len(Question.query.all()),
      'categories': categories_serialized,
      'currentCategory': 'not provided'
    })

  # Update question rating
  @app.route('/questions/<int:question_id>', methods=['PATCH'])
  def update_question_rating(question_id):
    try:
      body = request.get_json()
      # Get question according to id
      question = Question.query.filter(Question.id == question_id).one_or_none()

      if question is None:
        abort(404) # Question is not found
      print(body)
      # Else, proceed with the update
      if 'rating' in body:
        question.rating = int(body.get('rating'))
        question.update()

      return jsonify({
        "success": True,
        "id": question_id
      })

    except:
      abort(400)

  '''
  @TODO:
  Create an endpoint to DELETE question using a question ID.

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page.
  '''
  # Delete a question by question's id
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    try:

      # Grab question id
      question = Question.query.filter(Question.id == question_id).one_or_none()
      # If question id does not exist
      if question is None:
        abort(404)

      # Delete question
      question.delete()

      return jsonify({
        'success': True,
        'deleted': question_id
      })
    except:
      abort(422)

  '''
  @TODO:
  Create an endpoint to POST a new question,
  which will require the question and answer text,
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab,
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.
  '''

  '''
  @TODO:
  Create a POST endpoint to get questions based on a search term.
  It should return any questions for whom the search term
  is a substring of the question.

  TEST: Search by any phrase. The questions list will update to include
  only question that include that string within their question.
  Try using the word "title" to start.
  '''

  # Save a new trivia question
  @app.route('/questions', methods=['POST'])
  def add_new_question():
    # Get json body
    body = request.get_json()
    answer = body.get('answer', None)
    category = body.get('category', None)
    difficulty = body.get('difficulty', None)
    question = body.get('question', None)
    # Search query
    search = body.get('searchTerm', None)
    try:
      # If a search request
      if search:
        # Search questions and get the questions where search query is found
        results = Question.query.order_by(Question.id).filter(Question.question.ilike('%{}%'.format(search))).all()
        current_questions = paginate_questions(request, results)

        return jsonify({
          'success': True,
          'questions': current_questions,
          'total_questions': len(current_questions)
        })
      # If not a search request
      else:
        # Create a new question instance
        question = Question(question=question, answer=answer,category=category, difficulty=difficulty)
        # Save question
        question.insert()
        # Grab all the questions
        questions = Question.query.all()
        # Paginate questions
        current_questions = paginate_questions(request, questions)

        return jsonify({
          'success': True,
          'created': question.id,
          'questions': current_questions,
          'total_questions': len(current_questions)
        })

    except:
      abort(422)

  '''
  @TODO:
  Create a GET endpoint to get questions based on category.

  TEST: In the "List" tab / main screen, clicking on one of the
  categories in the left column will cause only questions of that
  category to be shown.
  '''
  # Get questions based on category /categories/Entertainment/questions
  @app.route('/categories/<category>/questions')
  def get_category_questions(category):
    # Get questions according to categories provided in the url
    questions = Question.query.filter(Question.category == category).all()

    if questions != []:

      # Paginate the questions by helper function
      current_questions = paginate_questions(request, questions)
      # Grab all the categories from database and serialize them
      questions_serialized = [question.format() for question in questions]

      return jsonify({
        'success': True,
        'questions': questions_serialized,
        'total_questions': len(questions_serialized)
      })

    else:
      abort(404)

  '''
  @TODO:
  Create a POST endpoint to get questions to play the quiz.
  This endpoint should take category and previous question parameters
  and return a random questions within the given category,
  if provided, and that is not one of the previous questions.

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not.
  '''
  # A helper function to genereate a random question for the user to answer
  def generate_random_question(category, previous_questions):
    # Get the questions out of category
    questions = Question.query.filter(Question.category == category['type']).all()

    # If questions are empty, then initiate the "all" category (all questions)
    if questions == []:
      questions = Question.query.all()

    # Get length of questions
    len_of_questions = len(questions)
    # Genereate a random number
    random_number = random.randint(0, len_of_questions) - 1
    # Generate random question
    question = questions[random_number].format()
    # Check the question's id to see if they have already been asked
    # in a previous question
    if question['id'] in previous_questions:
      # Check to see if all the questions are in the previous_array
      if len(previous_questions) == len(questions):
        return { "question":'done', "questions_per_play": len_of_questions }
      else:
        # Recursive function
        return generate_random_question(category, previous_questions)
    else:
      return { "question":question, "questions_per_play": len_of_questions }

  # Play the trivia game
  @app.route('/quizzes', methods=['POST'])
  def play_quiz():
    try:
      # Get json body
      body = request.get_json()
      category = body.get('quiz_category', None)
      previous_questions = body.get('previous_questions', None)
      # Generate random question
      question_dictionary = generate_random_question(category, previous_questions)

      return jsonify({
        'success': True,
        'question': question_dictionary['question'],
        'questions_per_play': question_dictionary['questions_per_play']
      })

    except:
      abort(422)

  '''
  @TODO:
  Create error handlers for all expected errors
  including 404 and 422.
  '''
  # Not Found Error (404)
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      'success': False,
      'error': 404,
      'message': 'Questions not found'
    }), 404

  # Method Not Allowed (405)
  @app.errorhandler(405)
  def method_not_allowed(error):
    return jsonify({
      'success': False,
      'error': 405,
      'message': 'Method not allowed'
    }), 405

  # Request Unprocessable (422)
  @app.errorhandler(422)
  def unprocessable_request(error):
    return jsonify({
      'success': False,
      'error': 422,
      'message': 'Request unprocessable'
    }), 422

  # Internal Server (500)
  @app.errorhandler(500)
  def server_error(error):
    return jsonify({
      'success': False,
      'error': 500,
      'message': 'Internal server error'
    }), 500

  return app

