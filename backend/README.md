# FULL STACK TRIVIA API BACKEND

## DESCRIPTION
  Welcome to Trivia! This game gives the user trivia questions and they have the option to get, delete, rate, and add questions to the database system (PostgreSQL). It allows them to choose different categories in questions, and gives them the ability to study and answer the quesions to gain points.

## CODING STYLE
  This project was configured by react (frontend) and RESTful API patterns with Flask development. It uses the format of MVC, where the models are the database schema and routes are the controllers between the server and client.

## TECHNOLOGIES
  Frontend: [JavaScript], [Jquery], [React]
  Backend: [Python], [Flask], [SQLAlchemy], [PostgreSQL]

## GETTING STARTED:

  ### CREATE LOCAL ENVIRONMENT
  If not done so, please install virtual environment. This keeps your dependencies for each project separate and organized.
  `pip install virtualenv`

  Then create the environment:
  1. virtualenv trivia_env
  2. cd trivia_env
  3. source bin/activate
  To **deactivate** environment, type: `deactivate`

  ### INSTALL PREREQUISITES
    Please install first all the modules for the project to get it started if you haven't done so already. Make sure you are in the parent directory of requirements.txt.
    Command:
    `pip install -r requirements.txt`

  ### DATABASE SETUP
    In order to install data in this trivia application, please make sure
    PostgreSQL is running and has created a trivia database on your local
    machine. Then from the terminal of the parent folder of `trivia.psql`,
    type the following command in the terminal:
    `psql trivia < trivia.psql`


  ### DATABASE ACCESS
    In order to access the database, you must have
    Postgres up and running. From the backend folder, in the command line type:
    `psql triva`

  ### SERVER SIDE DEVELOPMENT
    To run a Flask application, make sure you set up the proper environmental variables within the command line and run the application for the backend.

  ### Commands:
    `export FLASK_APP=flaskr`  (Sets the application)
    `export FLASK_ENV=development` (Sets the project in development mode)
    `flask run` (Runs the application)

  ### APPLICATION PROGRAMMING INTERFACE
      Here are the endpoints of our API application.
      Base URL: [http://127.0.0.1:3000/questions]
      API Keys: This version of the application does not require authentication or API Keys.

## API ENDPOINTS
  GET `/questions`
  - Fetch a list of questions in a paginated format. They are a total of 10 questions each page.
  - Request Arguments: None
  - Returns dictionaries and a response list of categories and questions.
  - INPUT: `curl http://127.0.0.1:3000/questions`
  - OUTPUT:
    {
      "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
      ],
      "current_category": null,
      "questions": [
        {
          "answer": "Apollo 13",
          "category": 5,
          "difficulty": 4,
          "id": 2,
          "question": "What movie earned Tom Hanks his third straight Oscar nomination, in 1996?",
          "rating": 4
        },
        ( ......... 9 More Questions )
        ],
        "success": true,
        "total_questions": 13
      }


  GET  `/categories`
  - Fetches a list of categories.
  - Request Arguments: None
  - Returns a dictionary of a response list of categories
  - INPUT: `curl http://127.0.0.1:3000/categories`
  - OUTPUT:
      {
        "categories": [
          "Science",
          "Art",
          "Geography",
          "History",
          "Entertainment",
          "Sports"
        ],
        "success": true
      }

  PATCH `/questions/<int:question_id>`
  - Update a question by inserting a rating
  - Request Argument: <int:question_id> (question's id)
  - Returns a response of the id and success
  - INPUT: `curl http://127.0.0.1:3000/questions/5 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
  - Output:
    {
      "id": 5,
      "success": true
    }

  DELETE `/questions/<int:question_id>`
  - Delete a question by id
  - Request Arguments: <int:question_id> (question's id)
  - Returns a response of the id and success
  - INPUT: `curl http://127.0.0.1:3000/questions/19 -X DELETE`
  - OUTPUT:
    {
      "deleted": 19,
      "success": true
    }

  POST `/questions`
  - Add a question
  - Request Arguments: None
  - Returns a response of a list of questions
  - INPUT: `curl http://127.0.0.1:3000/questions -X POST -H "Content-Type: application/json" -d '{"question":"In what state was Barack Obama born in?", "answer":"Hawaii", "category": 4, "difficulty": 2}'`
  - OUTPUT:
    {
      "created": 51,
      "questions": [
        {
          "answer": "Hawaii",
          "category": 4,
          "difficulty": 2,
          "id": 51,
          "question": "In what state was Barack Obama born in?",
          "rating": 0
        },
        (... 9 other questions)
      ],
      "success": true,
      "total_questions": 10
    }


  GET `/categories/<category>/questions`
  - Fetches questions according to category
  - Request Arguments: <category>
  - Returns a list of questions according to category
  - INPUT: `curl http://127.0.0.1:3000/categories/1/questions`
  - OUTPUT:
    {
      "categories": [
        "Science",
        "Art",
        "Geography",
        "History",
        "Entertainment",
        "Sports"
      ],
      "current_category": "1",
      "questions": [
        {
          "answer": "Escher",
          "category": 2,
          "difficulty": 1,
          "id": 16,
          "question": "Which Dutch graphic artist\u2013initials M C was a creator of optical illusions?",
          "rating": 0
        },
        (... 3 other Art questions)
      ],
      "success": true,
      "total_questions": 4
    }
  POST `/quizzes`
  - Call Quiz to start and play trivia
  - Request Arguments: None
  - Returns an object of a random question
  - INPUT: `curl http://127.0.0.1:3000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Art", "id": "1"}}'`
  - OUTPUT:
  {
    "question": {
      "answer": "Jackson Pollock",
      "category": 2,
      "difficulty": 2,
      "id": 19,
      "question": "Which American artist was a pioneer of Abstract Expressionism, and a leading exponent of action painting?",
      "rating": 0
    },
    "questions_per_play": 4,
    "success": true
  }
## TEST API
  In order to test this application, create a database specifically for testing and install data in it. Make sure you are in the appropriate folder of these files. You can accomplish this by typing the following in the terminal:
  1.  `dropdb trivia_test`
  2. `createdb trivia_test`
  3. `psql trivia_test < trivia.psql`
  4. `python test_flaskr.py`

## DEPLOYMENT
  `N/A`

## AUTHORS
  - Marco A. Canchola (Full Stack Developer)
  - Abe Feinberg (Udacity Instructor/Full Stack Developer)

## ACKNOWLEDGEMENTS
  - Udacity
  - Python Docs (https://docs.python.org/3/tutorial/venv.html)
  - https://www.postgresqltutorial.com/postgresql-alter-table/
