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

### On Ubuntu 18.04
```bash
# https://linuxize.com/post/how-to-create-python-virtual-environments-on-ubuntu-18-04/
sudo apt install python3-venv
# Within the directory
python3 -m venv env
source env/bin/activate
```

### Database Setup
With Postgres running, in terminal run:

```bash
# On Ubuntu 18.04
sudo -u postgres psql
create user billy password 'billy123';
create database itemcms owner billy;
```

### PIP Dependencies
With your virtual environment setup and running, install dependencies by running:

```bash
# with active virtual environment
pip3 install -r requirements.txt
```

This will install all of the required packages we selected within the `requirements.txt` file.

## Running the server
```bash
# -----------------------------------------------------------------------------
# gunicorn
# -----------------------------------------------------------------------------

# Heroku
web: gunicorn --bind 127.0.0.1:5000 --pythonpath backend/src wsgi:app


# Local
# NOTE change "billy" with your postgresql user
cd <mainDir>
source env/bin/activate
export DATABASE_URL="postgresql://billy:billy123@127.0.0.1:5432/itemcms" &&
export DEBUG=True &&
gunicorn --bind 127.0.0.1:5000 --pythonpath backend/src wsgi:app --reload --log-level debug

# -----------------------------------------------------------------------------
```

### db drop and create all

Got to: http://127.0.0.1:5000/reset-db

## Test with Unit Test
```bash
cd <mainDir>
source env/bin/activate

# run the tests
export DATABASE_URL="postgresql://billy:billy123@127.0.0.1:5432/itemcms" && export DEBUG=True && python backend/src/test_api.py

```

## Authentication
The authentication, related profiles, privileges and roles are implemented with [Auth0](https://auth0.com/)


### Profile roles and privileges

| Actor         | Role                           | CURD Privileges      |
| ------------- | ------------------------------ | -------------------- |
| Admin         | Administrator (Login required) | All privileges       |
| User          | User          (Login required) | See the schema below |
| Public        | Public     (NO login required) | See the schema below |

### Public CURD privileges

| Tables          | Create | Read   | Update | Delete  |
| --------------- | ------ | ------ | ------ |  ------ |
| items           | False  | True   | False  | False   |
| categories      | False  | True   | False  | False   |

### User CURD privileges

| Tables          | Create | Read   | Update | Delete  |
| --------------- | ------ | ------ | ------ |  ------ |
| items           | False  | True   | True   | False   |
| categories      | False  | True   | True   | False   |

## Test Auth0 role / endpoint


### Get the token

[Login Page](https://f0dev.auth0.com/authorize?audience=item&response_type=token&client_id=BNQ3moQ1kbaRMtdtXZX2XAlJs35cMnVk&redirect_uri=http://127.0.0.1:5000/login-results)

```
------------------------------------------
Admin:
------------------------------------------
email: -----> admin@itemcms.herokuapp.com
password: --> PoloCottoBene123
------------------------------------------
User
------------------------------------------
email: -----> user@itemcms.herokuapp.com
password: --> PolloCottoMale123
------------------------------------------
```
**NOTE:** Look on the address bar and grab your access token from the url

### Check the token
1. [jwt.io Admin token debug](https://jwt.io/#debugger-io?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJURkNSalpCUTBFd1JqWXdOa1EzUkVZMFJUZENNRE00T1RJd01rVkZNRVkzTlRNM1FVTXpOUSJ9.eyJpc3MiOiJodHRwczovL2YwZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTBmZTM1NTI0ZTg5YzBjYzZjNWFkODAiLCJhdWQiOiJpdGVtIiwiaWF0IjoxNTc4MzQ3Mzk4LCJleHAiOjE1NzgzNTQ1OTgsImF6cCI6IkJOUTNtb1Exa2JhUk10ZHRYWlgyWEFsSnMzNWNNblZrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJjcmVhdGU6Y2F0ZWdvcnkiLCJjcmVhdGU6aXRlbSIsImRlbGV0ZTpjYXRlZ29yeSIsImRlbGV0ZTppdGVtIiwidXBkYXRlOmNhdGVnb3J5IiwidXBkYXRlOml0ZW0iXX0.aEPS2o9HlOL8UJL5f7bzf0_Qus1YRlQuJuym2UmAoijx1dSWCdxxLBXNFv54mam-2obxTU-QbuIF5wwrWyn1sN7-bcBl0bKl31EnapGj9y5yDTDIrEN8tAhZ6nNMKZ_I5N1-aLPcalnTy_oBv1QPKC46moc64UpanYBrtRvyIk2t7mjhvPqvp5wMFWges26K-G9iJlNUMTczqv8lQJ8JYzxj09OugVLcNeFuPogOSQ5vKz0gQ8fHgep3ABjBYeNafaGRsfF7z9twJLirRgn8QgeR7PNG3yNdF_RWHnzxykVUcVJxDh3sJhBLszuNgKfOgreChgSpll_Vc44FMNmVOQ&publicKey=-----BEGIN%20PUBLIC%20KEY-----%0AMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtR0HQq5YpHGqBDKYBICU%0An8kSbeCdeCihYrk176ejQDCpatIh5JHF7T2wQHO9Aj5sggTsYdPOqyVGdJrCEvqO%0AqZBoOGXuq1s%2FrS5IG6LSCX4YJP8gPlbHsSGQ0%2FBoJL6byqjA%2FG6LJIoZZXl1fKRW%0AYFR6OpcqrD2KKaUqiMSBSlp7qMlTJFCTqXuN2QByBnn021LHrdAPbswxuVTc6VKd%0AjT381SmLZ8Ti5EEexY9%2FXDMJMXmp3d%2BP4q7dN%2B14qhgpBhlD16F3emAGctIKiTxQ%0AlezHxOfnyrij621hbnZrfOo1GdZgMPsCM47x5fgwnoB1lCVrNpAx57XYZQWKHptw%0A5wIDAQAB%0A-----END%20PUBLIC%20KEY-----%0A)
2. [jwt.io User token debug](https://jwt.io/#debugger-io?token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsImtpZCI6IlJURkNSalpCUTBFd1JqWXdOa1EzUkVZMFJUZENNRE00T1RJd01rVkZNRVkzTlRNM1FVTXpOUSJ9.eyJpc3MiOiJodHRwczovL2YwZGV2LmF1dGgwLmNvbS8iLCJzdWIiOiJhdXRoMHw1ZTBmZjNkYjljMDI3YTBlOWU0NmExOTAiLCJhdWQiOiJpdGVtIiwiaWF0IjoxNTc4MzQ3OTQwLCJleHAiOjE1NzgzNTUxNDAsImF6cCI6IkJOUTNtb1Exa2JhUk10ZHRYWlgyWEFsSnMzNWNNblZrIiwic2NvcGUiOiIiLCJwZXJtaXNzaW9ucyI6WyJ1cGRhdGU6Y2F0ZWdvcnkiLCJ1cGRhdGU6aXRlbSJdfQ.fqEzPr4WIceKpdbN_GRWodVkg0K_rugI-tDT5LPQ9sr-YIKgwtQTn29PVTIDhAWow6La5KsDLTmgJKUgv-wYx7LbJGq7mMIYMpQjxvoSmNnTInBnOELDX3szwbBUvwYtyzvXuRctp5YjNLS5MZO4ClHeswbi7b7c98TQJ5h4NQyS_vWMfo--Hsd11SBGeFT_K5rL3LJ060otQxxInMsikj9VZIvfIoUtnxw9N1qlvmIymvvGlkU3--YrULKjmBjQzozi3HFA7hOBTb3I4nvn-6lJh7GcXrvecrKorW8T0EjDDPwNloWK9xIYLak7yXOR5ma1tn13sW5lTB20mhh6_A&publicKey=-----BEGIN%20PUBLIC%20KEY-----%0AMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAtR0HQq5YpHGqBDKYBICU%0An8kSbeCdeCihYrk176ejQDCpatIh5JHF7T2wQHO9Aj5sggTsYdPOqyVGdJrCEvqO%0AqZBoOGXuq1s%2FrS5IG6LSCX4YJP8gPlbHsSGQ0%2FBoJL6byqjA%2FG6LJIoZZXl1fKRW%0AYFR6OpcqrD2KKaUqiMSBSlp7qMlTJFCTqXuN2QByBnn021LHrdAPbswxuVTc6VKd%0AjT381SmLZ8Ti5EEexY9%2FXDMJMXmp3d%2BP4q7dN%2B14qhgpBhlD16F3emAGctIKiTxQ%0AlezHxOfnyrij621hbnZrfOo1GdZgMPsCM47x5fgwnoB1lCVrNpAx57XYZQWKHptw%0A5wIDAQAB%0A-----END%20PUBLIC%20KEY-----%0A)

### Check the endpoint

 - Local base url: 127.0.0.1:5000/
 - Remote base url: https://itemcms.herokuapp.com/

#### Endpoints

| Endpoint         | Method  | Requires Auth   |
| ---------------- | --------| --------------- |
| /categories      | POST    | create:category |
| /categories      | GET     | None            |
| /categories/id   | PATCH   | update:category |
| /categories/id   | DELETE  | delete:category |
| /items           | POST    | create:item     |
| /items           | GET     | None            |
| /items/id        | PATCH   | update:item     |
| /items/id        | DELETE  | delete:item     |
