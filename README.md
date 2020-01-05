# Item CMS

## Overview
Item CMS is a basic RESTful APIs framework design to manage items, the not typed structure is designed to be suitable for a wide range of products / items.

## Tech Stack (Key Dependencies)
The tech stack will include:

* **[Python3](https://www.python.org/)** and **[Flask](http://flask.palletsprojects.com)** as server language and server framework.

* **[SQLAlchemy](https://www.sqlalchemy.org/)** ORM library.

* **[Flask-Migrate](https://flask-migrate.readthedocs.io/en/latest/)** for creating and running schema migrations.

* **[Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#)** to handle cross origin requests.

## Installing Dependencies

### Python 3.8

Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)

### PostgreSQL
Follow instructions to install the latest version of  PostgreSQL for your platform in the [PostgreSQL download](https://www.postgresql.org/download/)

### Virtual Enviornment
Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)

### PIP Dependencies
With your virtual environment setup and running, install dependencies by running:

```bash
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

### Database Setup
With Postgres running, in terminal run:
```bash
createdb itemcms
```

### Running the server
```bash
# -----------------------------------------------------------------------------
# gunicorn
# -----------------------------------------------------------------------------

# Heroku
web: gunicorn --bind 127.0.0.1:5000 --pythonpath backend/src wsgi:app


# Local
# NOTE change "Billy" with your postgresql user
cd <mainDir>
source env/bin/activate
export DATABASE_URL="postgresql://Billy@localhost:5432/itemcms" &&
export DEBUG=True &&
gunicorn --bind 127.0.0.1:5000 --pythonpath backend/src wsgi:app --reload --log-level debug

# -----------------------------------------------------------------------------
```

## db drop and create all

Got to: http://127.0.0.1:5000/reset-db

## Base endpoint

Got to: http://127.0.0.1:5000/items
