from main import db
from flask_login import UserMixin
from datetime import datetime

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(100), nullable=False)
    def __repr__(self):
        return f'{self.title}, author {self.author} created on {self.date} status: {self.status}'
#to finish
class FinishedBook(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(100), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    response = db.Column(db.String())
    date = db.Column(db.Date, nullable=False)
    def __repr__(self):
        return f'{self.title}, author {self.author} created on {self.date} status: {self.status}'


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)