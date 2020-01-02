# Item CMS

## Overview
Item CMS is a basic RESTful APIs framework design to manage items, the not typed structure is designed to be suitable for a wide range of products / items.

## Tech Stack (Key Dependencies)
Our tech stack will include:

* **[SQLAlchemy](https://www.sqlalchemy.org/)** ORM library.
* **[db](#db)** database.
* **[Python3](https://www.python.org/)** and **[Flask](http://flask.palletsprojects.com)** as server language and server framework
* **[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)** for creating and running schema migrations

## Resources

* https://martin-thoma.com/flask-gunicorn/
* https://docs.gunicorn.org/en/stable/settings.html#bind
* https://stackoverflow.com/questions/16416172/how-can-i-modify-procfile-to-run-gunicorn-process-in-a-non-standard-folder-on-he

## db schema diagram
@TODO

## Authentication
The authentication, related profiles, privileges and roles are implemented with [Auth0](https://auth0.com/)

### Profile and role

| Actor         | Role          | CURD Privileges      |
| ------------- | ------------- | -------------------- |
| Admin         | Administrator | All                  |
| User          | User          | See the schema below |

## User CURD privileges

| Tables          | Create | Update | Read   | Delete  |
| --------------- | ------ | ------ | ------ |  ------ |
| items           | True   | True   | True   | True    |
| categories      | True   | True   | True   | False   |

## Development Setup

#### Install

```bash

# @TODO

```

#### Running the server

```bash


# -----------------------------------------------------------------------------
# gunicorn
# -----------------------------------------------------------------------------

# Heroku
web: gunicorn --bind 127.0.0.1:5000 --pythonpath backend/src wsgi:app

# Local
# https://docs.gunicorn.org/en/stable/settings.html#bind
cd <mainDir>
source env/bin/activate
export DATABASE_URL="postgresql://Billy@localhost:5432/itemcms" &&
export DEBUG=True &&
gunicorn --bind 127.0.0.1:5000 --pythonpath backend/src wsgi:app --reload

# -----------------------------------------------------------------------------

```

## Testing base endpoints

#### GET / Return 200

```bash
curl -X GET http://127.0.0.1:5000/
```

#### GET /abc Return 404

```bash
curl -X GET http://127.0.0.1:5000/abc
```
