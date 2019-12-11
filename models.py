import os
from sqlalchemy import (
    Column, String, Integer, Table, PrimaryKeyConstraint,
    ForeignKey,
)
from flask_sqlalchemy import SQLAlchemy

database_filename = "database.db"
project_dir = os.path.dirname(os.path.abspath(__file__))
database_path = "sqlite:///{}".format(
    os.path.join(project_dir, database_filename))

db = SQLAlchemy()


def setup_db(app):
    app.config["SQLALCHEMY_DATABASE_URI"] = database_path
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)


class ModelUtils:
    def insert(self):
        """inserts a new record into the Model
        EXAMPLE
            `movie = Movies(title=title, release_date=release_date)`
            `movie.insert()`
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a record from the model
        the record must exist in the model
        EXAMPLE
            `movie = Movie(title=title, release_date=release_date)`
            `movie.delete()`
        """
        db.session.delete(self)
        db.session.commit()

    def update(self):
        """updates a record in the model
        the record must exist in the model
        EXAMPLE
            `movie = Movie.query.filter(Movie.id == id).one_or_none()`
            `movie.title = 'New Movie'`
            `movie.update()`
        """
        db.session.commit()


# there'll need to be a many-to-many relationship between movies and actors
# this is a helper table for the relationship
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
relationship_table = Table('relationship_table',
                           Column('movie_id', Integer, ForeignKey('movie.id'), nullable=False),
                           Column('actor_id', Integer, ForeignKey('actor.id'), nullable=False),
                           PrimaryKeyConstraint('movie_id', 'actor_id'))


class Movie(db.Model, ModelUtils):
    """Movie model
    a movie must have a unique title
    a movie must also have a release_date
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, required=True)
    release_date = Column(Integer, required=True)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"


class Actor(db.Model, ModelUtils):
    """Actor model
    an actor must have a name, age and gender
    movies is a foreign key pointing to the movies the actor has been in
    """

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), required=True)
    gender = Column(String(6), required=True)
    movies = db.relationship('Movie', backref='movies_list', lazy=True)

    def __repr__(self):
        return f"<Actor {self.id} {self.name}>"
