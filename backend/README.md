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
  - Return a list of categories in a paginated format. They are a total of 10.
    INPUT: `curl http://127.0.0.1:3000/questions`
    OUTPUT:
      {
        "categories": [
          "Science",
          "Art",
          "Geography",
          "History",
          "Entertainment",
          "Sports"
        ],
        "currentCategory": "not provided",
        "questions": [
          {
            "answer": "Oxygen",
            "category": "Science",
            "difficulty": 4,
            "id": 24,
            "question": "What element did Joseph Priestley discover in 1774?",
            "rating": 4
          },
          ( ......... 9 More Questions )
        ],
        "success": true,
        "total_questions": 13
      }


  GET  `/categories`
  - Return a list of categories.
    INPUT: `curl http://127.0.0.1:3000/categories`
    OUTPUT:
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
    INPUT: `curl http://127.0.0.1:3000/questions/25 -X PATCH -H "Content-Type: application/json" -d '{"rating":"1"}'`
    {
      "id": 25,
      "success": true
    }

  GET `/categories`
  - Return a list of categories.
    INPUT: `curl http://127.0.0.1:3000/categories`
    OUTPUT:
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

  DELETE `/questions/<int:question_id>`
  - Delete a question by id
    INPUT: `curl http://127.0.0.1:3000/questions/25 -X DELETE`
    {
      "deleted": 25,
      "success": true
    }

  POST `/questions`
  - Add a question
    INPUT: `curl http://127.0.0.1:3000/questions/25 -X POST -H "Content-Type: application/json" -d '{"question":"In what state was Barack Obama born in?", "answer":"Hawaii", "category":"History", "difficulty": 2}'`
    OUTPUT:
    {
      "created": 51,
      "questions": [
        {
          "answer": "Hawaii",
          "category": "History",
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
  - Grab questions according to category
    INPUT: `curl http://127.0.0.1:3000/categories/Science/questions`
    OUTPUT:
    {
      "questions": [
        {
          "answer": "Oxygen",
          "category": "Science",
          "difficulty": 4,
          "id": 24,
          "question": "What element did Joseph Priestley discover in 1774?",
          "rating": 4
        },
        {
          "answer": "Copper and Tin",
          "category": "Science",
          "difficulty": 3,
          "id": 26,
          "question": "Bronze is an alloy consisting primarily of what two elements?",
          "rating": 1
        }
      ],
      "success": true,
      "total_questions": 2
  }

  POST `/quizzes`
  - Call Quiz to start and play trivia.
    INPUT: `curl http://127.0.0.1:3000/quizzes -X POST -H "Content-Type: application/json" -d '{"previous_questions": [], "quiz_category": {"type": "Art", "id": "1"}}'`
  OUTPUT:
  {
    "question": {
      "answer": "Michelangelo",
      "category": "Art",
      "difficulty": 3,
      "id": 29,
      "question": "Who painted the Sistine Chapel's ceiling?",
      "rating": 0
    },
    "questions_per_play": 3,
    "success": true
}

## TEST API
  How to run unit test in python flask on command line.
  INPUT: `pyhton test_flaskr.py`

## DEPLOYMENT
  `N/A`

## AUTHORS
  - Marco A. Canchola (Full Stack Developer)
  - Abe Feinberg (Udacity Instructor/Full Stack Developer)

## ACKNOWLEDGEMENTS
  - Udacity
  - Python Docs (https://docs.python.org/3/tutorial/venv.html)
  - https://www.postgresqltutorial.com/postgresql-alter-table/
