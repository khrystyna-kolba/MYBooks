from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, PasswordField, TextAreaField, DecimalRangeField
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from models import *
from main import bcrypt
class AddBookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    status = SelectField("Status",choices=[('want_to_read', 'want to read'),('reading_now', 'reading now')],validators=[DataRequired()])

    submit =SubmitField("submit")
class DeleteTaskForm(FlaskForm):
    submit = SubmitField('Delete')

class LoginForm(FlaskForm):
    username = StringField("username", validators=[DataRequired()])
    email = StringField("email", validators=[DataRequired()])
    password = PasswordField("password", validators=[DataRequired()])
    submit = SubmitField("login")
    def validate_username(self, username):
        existing = User.query.filter_by(username=username.data).first()
        print("validating login username", existing)
        if existing==None:
            raise ValidationError("username is not found. try again")
    def validate_email(self, email):
        print("validating login email")
        existing = User.query.filter_by(email=email.data).first()
        if existing == None:
            raise ValidationError("email is wrong. try again")
    def validate_password(self, password):
        print("validating login password")
        user = User.query.filter_by(username=self.username.data).first()
        if user:
            if not bcrypt.check_password_hash(user.password, self.password.data):
                raise ValidationError("incorrect password, try again")

class RegisterForm(FlaskForm):
    username = StringField("username", validators=[DataRequired(),Length(4,20)])
    email = StringField("email", validators=[DataRequired(),Length(4,20)])
    password = PasswordField("password", validators=[DataRequired(),Length(4,20)])
    submit = SubmitField("sign up")
    def validate_username(self, username):
        existing = User.query.filter_by(username=username.data).first()
        if existing:
            raise ValidationError("username already exists. choose another one")
    def validate_email(self, email):
        existing = User.query.filter_by(email=email.data).first()
        if existing:
            raise ValidationError("email already taken. choose another one")


class MarkReadBookForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    author = StringField("Author", validators=[DataRequired()])
    rating = DecimalRangeField("Rating 0-10")
    response = TextAreaField("Response")
    submit = SubmitField("submit")
