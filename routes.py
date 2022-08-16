from main import app, bcrypt, login_manager
from flask import render_template, redirect, url_for, flash, get_flashed_messages
from datetime import datetime
from models import db, Book, User, FinishedBook
from wtforms.validators import DataRequired, Length, ValidationError, InputRequired
from flask_login import login_user, LoginManager, login_required, logout_user, current_user
import forms

@app.route('/')
def welcome():
    return render_template("welcome.html")




@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/index')
@login_required
def index():

    tasks =Book.query.filter_by(username=current_user.username)
    f = FinishedBook.query.filter_by(username=current_user.username)
    return render_template("index.html",  finished=f, tasks=tasks, status="All books")
@app.route('/login', methods=["GET","POST"])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                if user.email==form.email.data:
                    login_user(user)
                    return redirect(url_for('profile'))

    return render_template('login.html', form = form)
@app.route('/register', methods=["GET","POST"])
def register():
    form = forms.RegisterForm()
    if form.validate_on_submit():
        hashed = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        new_user = User(username= form.username.data, email=form.email.data, password = hashed)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html', form = form)

@app.route('/logout', methods=["GET","POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))









@app.route('/profile')
@login_required
def profile():
    return render_template("profile.html", username=current_user)




@app.route('/mark_read/<int:book_id>', methods=["GET","POST"])
@login_required
def mark_read(book_id):
    book = Book.query.get(book_id)
    form = forms.MarkReadBookForm()
    if book:
        if form.validate_on_submit():
            new_read_book = FinishedBook(username= book.username, title=form.title.data, author=form.author.data, rating=int(form.rating.data), response=form.response.data, date=book.date)
            db.session.delete(book)
            db.session.add(new_read_book)
            db.session.commit()
            return redirect(url_for("read"))
        form.title.data = book.title
        form.author.data = book.author
        return render_template('mark_read.html', book_id=book_id, book=book, form=form)
    return redirect(url_for('index'))
#different sections
@app.route('/read')#to do /represents new table
@login_required
def read():
    tasks = FinishedBook.query.filter_by(username=current_user.username)
    return render_template("read.html", tasks=tasks)


@app.route('/read_book/<int:book_id>')
@login_required
def read_book(book_id):
    book = FinishedBook.query.get(book_id)
    return render_template("read_book.html", book=book)




@app.route('/reading_now')
@login_required
def reading_now():
    tasks = Book.query.filter_by(status='reading_now', username=current_user.username)
    return render_template("index.html", tasks=tasks,status ="Reading now", finished=[])
@app.route('/want_to_read')
@login_required
def want_to_read():
    tasks = Book.query.filter_by(status='want_to_read', username=current_user.username)
    return render_template("index.html", tasks=tasks, status ="Want to read", finished=[])



@app.route("/add", methods=["GET","POST"] )
@login_required
def add():
    form = forms.AddBookForm()
    if form.validate_on_submit():
        t = Book(title=form.title.data,author = form.author.data, username = current_user.username, status=form.status.data, date=datetime.now())
        db.session.add(t)
        db.session.commit()
        flash("Book added to library")
        return redirect(url_for("index"))
    return render_template("add.html", form = form)

@app.route('/delete/<int:book_id>', methods=["GET","POST"])
@login_required
def delete(book_id):
    book = Book.query.get(book_id)
    form = forms.DeleteTaskForm()

    if book:
        print("hello1")
        if form.validate_on_submit():
            print("hello")
            db.session.delete(book)
            db.session.commit()
            flash("book has been deleted")
            return redirect(url_for("index"))
        return render_template('delete.html', book_id=book_id, book=book, form=form)
    return redirect(url_for('index'))
@app.route('/delete_finished/<int:book_id>', methods=["GET","POST"])
@login_required
def delete_finished(book_id):
    book = FinishedBook.query.get(book_id)
    form = forms.DeleteTaskForm()
    if book:
        if form.validate_on_submit():
            db.session.delete(book)
            db.session.commit()
            flash("finished book has been deleted")
            return redirect(url_for("index"))
        return render_template('delete_finished.html', book_id=book_id, book=book, form=form)
    return redirect(url_for('index'))

@app.route("/edit/<int:book_id>", methods=["GET","POST"] )
@login_required
def edit(book_id):
    book = Book.query.get(book_id)
    form = forms.AddBookForm()
    if book:
        if form.validate_on_submit():
            book.title = form.title.data
            book.author = form.author.data
            book.status = form.status.data
            db.session.commit()
            flash("book has been updated")
            return redirect(url_for("index"))
        form.title.data = book.title
        form.author.data = book.author
        return render_template('edit.html', book_id = book_id, form=form)
    return redirect(url_for('index'))

@app.route("/edit_finished/<int:book_id>", methods=["GET","POST"] )
@login_required
def edit_finished(book_id):
    book = FinishedBook.query.get(book_id)
    form = forms.MarkReadBookForm()
    if book:
        if form.validate_on_submit():
            book.title = form.title.data
            book.author = form.author.data
            book.rating = int(form.rating.data)
            book.response = form.response.data
            db.session.commit()
            flash("finished book has been updated")
            return render_template("read_book.html", book=book)
        form.title.data = book.title
        form.author.data = book.author
        form.rating.data = book.rating
        form.response.data=book.response
        return render_template('edit_read.html', book_id = book_id,book=book,  form=form)
    return redirect(url_for('index'))




