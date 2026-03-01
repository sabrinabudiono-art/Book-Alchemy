from flask import Flask, request, render_template, redirect, url_for
from data_models import db, Author, Book
from sqlalchemy import or_

app = Flask(__name__)

import os

basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{os.path.join(basedir, 'data/library.sqlite')}"
db.init_app(app)

@app.route("/")
def home():
    """
        Display the homepage with a list of books. Supports sorting
        by book title (default) or author name and searching by book
        title or author name
    """
    sort = request.args.get("sort", "title")
    search = request.args.get("search", "").strip()

    query = db.session.query(Book, Author).join(Author)

    if search:
        query = query.filter(
            or_(
                Book.book_title.ilike(f"%{search}%"),
                Author.author_name.ilike(f"%{search}%")
            )
        )

    if sort == "author":
        query = query.order_by(Author.author_name.asc())
    else:
        query = query.order_by(Book.book_title.asc())

    books_author_tuple = query.all()

    return render_template(
        "home.html",
        books_author_tuple=books_author_tuple,
        current_sort=sort,
        current_search=search
    )

@app.route('/add_author', methods=['GET', 'POST'])
def add_author():
    """
      Add a new author to the database.
    """
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
    """
        Add a new book to the database.
    """
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

@app.route("/book/<int:book_id>/delete", methods=["POST"])
def delete_book(book_id):
    """
        Delete a new book from the database.
    """
    book = Book.query.get_or_404(book_id)

    author_id = book.author_id
    book_title = book.book_title

    db.session.delete(book)
    db.session.commit()

    return redirect(url_for("home", deleted=book_title))

#with app.app_context():
#   db.create_all()

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
