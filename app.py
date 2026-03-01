from flask import Flask, request, render_template, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from data_models import db, Author, Book

app = Flask(__name__)

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

@app.route('/')
def home():
    books_author_tuple = db.session.query(Book, Author) \
        .join(Author, Book.author_id == Author.author_id) \
        .all()
    return render_template('home.html', books_author_tuple=books_author_tuple)


@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    if request.method == 'POST':
        new_author = Author(
            author_name=request.form.get('name'),
            author_date_of_birth=request.form.get('birthdate'),
            author_date_of_death=request.form.get('date_of_death'))

        db.session.add(new_author)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_author.html')


@app.route('/add_book', methods=['GET', 'POST'])
def add_book():
    if request.method == 'POST':
        new_book = Book(
            book_isbn=request.form.get('isbn'),
            book_title=request.form.get('title'),
            book_publication_year=request.form.get('publication_year'),
            author_id = int(request.form.get('author_id')))

        db.session.add(new_book)
        db.session.commit()
        return redirect(url_for('home'))
    authors = Author.query.all()
    return render_template('add_book.html', authors=authors)


#with app.app_context():
#   db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
