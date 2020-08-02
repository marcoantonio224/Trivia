import os
import re
from sqlalchemy import Column, String, Integer, create_engine
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import validates

import json

database_name = "trivia"
database_path = "postgres://{}/{}".format('localhost:5432', database_name)

db = SQLAlchemy()

'''
setup_db(app)
    binds a flask application and a SQLAlchemy service
'''
def setup_db(app, database_path=database_path):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)
    db.create_all()
    migrate = Migrate(app, db)

'''
Category

'''
class Category(db.Model):
  __tablename__ = 'categories'

  id = Column(Integer, primary_key=True)
  type = Column(String, nullable=False, unique=True)
  question = db.relationship('Question', backref='parent_category', cascade='all, delete-orphan',  lazy=True)

  def __init__(self, type):
    self.type = type

  def format(self):
    return {
      'id': self.id,
      'type': self.type
    }

'''
Question

'''
class Question(db.Model):
  __tablename__ = 'questions'

  id = Column(Integer, primary_key=True)
  question = Column(String, nullable=False)
  answer = Column(String, nullable=False)
  difficulty = Column(Integer, nullable=False)
  rating = Column(Integer, nullable=False, default=0)
  category = Column(String, db.ForeignKey('categories.type'))

  @validates('question','answer')
  def validate_question(self, keys, values):
    # Create a regular expression to search for special characters
    specialChars = re.compile('[@_!#$%^&*()<>/\|}{~:]')
    # Check to see if values are empty
    if values == '':
      raise AssertionError('Cannot contain empty fields')
    # Then validate to see if the string contains any special characters
    elif specialChars.search(values) is not None:
      raise AssertionError('Cannot contain special characters')

    return values


  def __init__(self, question, answer, category, difficulty):
    self.question = question
    self.answer = answer
    self.category = category
    self.difficulty = difficulty

  def insert(self):
    db.session.add(self)
    db.session.commit()

  def update(self):
    db.session.commit()

  def delete(self):
    db.session.delete(self)
    db.session.commit()

  def format(self):
    return {
      'id': self.id,
      'question': self.question,
      'answer': self.answer,
      'category': self.category,
      'difficulty': self.difficulty,
      'rating': self.rating
    }

