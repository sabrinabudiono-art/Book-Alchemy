from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, ForeignKey

db = SQLAlchemy()


class Author(db.Model):
    """
        Represents an author in the library.
    """
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    author_date_of_birth = Column(String)
    author_date_of_death = Column(String)

    def __str__(self):
        return f"Author(author_id = {self.author_id}, name = {self.author_name})"


class Book(db.Model):
    """
        Represents a book in the library.
    """
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(Integer)
    book_title = Column(String)
    book_publication_year = Column(Integer)

    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)

    def __str__(self):
        return f"Book(book_id = {self.book_id}, title = {self.book_title})"
