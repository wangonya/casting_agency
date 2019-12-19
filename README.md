# Casting Agency

Casting Agency models a company that is responsible for creating movies and managing and assigning actors to those movies.

Hosted on heroku. [Link](https://udacity-casting-agency.herokuapp.com/).

## Motivation

This is my capstone project for the Udacity FSWD nanodegree.

## Dependencies

All dependencies are listed in the `requirements.txt` file. 
They can be installed by running `pip3 install -r requirements.txt`.

## Authentication

The API has three registered users:

1. Assistant

```
email: assistant@casting.com
password: assistant@casting.com1
```

2. Director

```
email: director@casting.com
password: director@casting.com1
```

3. Producer

```
email: producer@casting.com
password: producer@casting.com1
```

The Auth0 domain and api audience can be found in `setup.sh`.

## Endpoints

### `GET /movies`

Gets all movies from the db.

Response:

```json5
{
  "movies": [
    {
      "id": 1,
      "movies": "all acted movies here",
      "release_date": "2021-02-02",
      "title": "Movie"
    },
    {
      "id": 2,
      "movies": "all acted movies here",
      "release_date": "2019-01-01",
      "title": "New movie"
    }
  ],
  "success": true
}
```

### `POST /movies`

Adds a new movie to the db.

Data:

```json5
{
  "title": "title",
  "release_date": "release_date"
}
```

Response:

```json5
{
  'success': true,
  'movie': 'title'
}
```

### `PATCH /movies/<int:id>`

Edit data on a movie in the db.

Data:

```json5
{
  "title": "new title",
  "release_date": "2021-02-02"
}
```

Response:

```json5
{
  'success': true,
  'movie': {
              "id": 1,
              "movies": "all acted movies here",
              "release_date": "2021-02-02",
              "title": "new title"
            }
}
```

### `DELETE /movies/<int:id>`

Delete a movie from the db.

Response:

```json5
{
  'success': true,
  'delete': 1
}
```

### `GET /actors`

Gets all actors from the db.

Response:

```json5
{
  "actors": [
    {
      "gender": "M",
      "id": 1,
      "movies": "all acted movies here",
      "name": "actor"
    },
    {
      "gender": "F",
      "id": 2,
      "movies": "all acted movies here",
      "name": "ewwe"
    }
  ],
  "success": true
}
```

### `POST /actors`

Adds a new actor to the db.

Data:

```json5
{
  "name": "name",
  "gender": "F"
}
```

Response:

```json5
{
  'success': true,
  'actor': 'name'
}
```

### `PATCH /actors/<int:id>`

Edit data on a actor in the db.

Data:

```json5
{
  "name": "new name",
  "gender": "M"
}
```

Response:

```json5
{
  'success': true,
  'actor': {
              "gender": "M",
              "id": 1,
              "movies": "all acted movies here",
              "name": "new name"
            }
}
```

### `DELETE /actors/<int:id>`

Delete a actor from the db.

Response:

```json5
{
  'success': true,
  'delete': 1
}
```

## Tests

To run the tests, run `python3 tests.py`.