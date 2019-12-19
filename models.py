import os
from sqlalchemy import (
    Column, String, Integer, Table, ForeignKey,
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
    db.create_all()


def db_drop_and_create_all():
    """drops the database tables and starts fresh
    can be used to initialize a clean database"""
    db.drop_all()
    db.create_all()


# there'll need to be a many-to-many relationship between movies and actors
# this is a helper table for the relationship
# https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#many-to-many-relationships
movie_actor_relationship_table = Table('movie_actor_relationship_table', db.Model.metadata,
                                       Column('movie_id', Integer, ForeignKey('movies.id')),
                                       Column('actor_id', Integer, ForeignKey('actors.id')))


class Movie(db.Model):
    """Movie model
    a movie must have a unique title
    a movie must also have a release_date
    """

    __tablename__ = "movies"

    id = Column(Integer, primary_key=True)
    title = Column(String(80), unique=True, nullable=False)
    release_date = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Movie {self.id} {self.title}>"

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

    @staticmethod
    def update():
        """updates a record in the model
        the record must exist in the model
        EXAMPLE
            `movie = Movie.query.filter(Movie.id == id).one_or_none()`
            `movie.title = 'New Movie'`
            `movie.update()`
        """
        db.session.commit()

    def format(self):
        """returns a formatted response of the data in the model"""
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'movies': 'all acted movies here'  # TODO: get this from relationship table
        }


class Actor(db.Model):
    """Actor model
    an actor must have a name, age and gender
    movies is a foreign key pointing to the movies the actor has been in
    """

    __tablename__ = "actors"

    id = Column(Integer, primary_key=True)
    name = Column(String(80), nullable=False)
    gender = Column(String(6), nullable=False)
    movies = db.relationship('Movie', secondary=movie_actor_relationship_table,
                             backref='movies_list', lazy=True)

    def __repr__(self):
        return f"<Actor {self.id} {self.name}>"

    def insert(self):
        """inserts a new record into the Model
        EXAMPLE
            `actor = Actor(name=name, gender=gender)`
            `actor.insert()`
        """
        db.session.add(self)
        db.session.commit()

    def delete(self):
        """deletes a record from the model
        the record must exist in the model
        EXAMPLE
            `actor = Actor.query.filter(Movie.id == id).one_or_none()`
            `actor.delete()`
        """
        db.session.delete(self)
        db.session.commit()

    @staticmethod
    def update():
        """updates a record in the model
        the record must exist in the model
        EXAMPLE
            `actor = Actor.query.filter(Movie.id == id).one_or_none()`
            `actor.title = 'New Movie'`
            `actor.update()`
        """
        db.session.commit()

    def format(self):
        """returns a formatted response of the data in the model"""
        return {
            'id': self.id,
            'name': self.name,
            'gender': self.gender,
            'movies': 'all acted movies here'  # TODO: get this from relationship table
        }
