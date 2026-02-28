from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base, sessionmaker

db = SQLAlchemy()

# Create a database connection
engine = create_engine('sqlite:///data/library.sqlite')

# Create a database session
Session = sessionmaker(bind=engine)
session = Session()

class Author(db.Model):
    __tablename__ = 'authors'

    author_id = Column(Integer, primary_key=True, autoincrement=True)
    author_name = Column(String)
    author_date_of_birth = Column(String)
    author_date_of_death = Column(String)

    def __str__(self):
        return f"Author(author_id = {self.author_id}, name = {self.author_name})"

class Book(db.Model):
    __tablename__ = 'book'

    book_id = Column(Integer, primary_key=True, autoincrement=True)
    book_isbn = Column(Integer)
    book_title = Column(String)
    book_publication_year = Column(Integer)

    author_id = Column(Integer, ForeignKey('authors.author_id'), nullable=False)

    def __str__(self):
        return f"Book(book_id = {self.book_id}, title = {self.book_title})"

karel = Author(author_name='Karel', author_date_of_birth="24 November 1999")
harry_potter = Book(book_isbn=123, book_title="Harry Potter", book_publication_year=1990, author_id=karel.author_id)