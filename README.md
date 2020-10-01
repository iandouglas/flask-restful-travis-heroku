# Python 3, Flask 1.1.2, Flask-RESTful, PostgreSQL, TDD with Coverage, Travis-CI and Heroku

Whew, that's a mouthful. I should come up with a more clever name.

![Agent Coulson, Iron Man, explaining the long name of SHIELD](https://thumbs.gfycat.com/OldfashionedCrazyAmericanbittern-size_restricted.gif)

I'm often asked by students at [Turing](https://turing.io) to help them get
started with Python projects, usually in Flask. So here's a way to scale that
knowledge and get everyone started all in one place.

### Table of Contents

1. [What this Repo is](#what-this-repo-is)
1. [What this Repo is Not](#what-this-repo-is-not)
1. [What to do after cloning](#what-do-to-after-cloning)
1. [Virtual Environment setup](#virtual-environment-setup)
1. [Requirements](#requirements), aka "requirements.txt"
1. [Database Setup](#database-setup)
1. [Heroku Procfile](#heroku-procfile)
1. [Travis-CI setup](#travis-ci-setup)
1. [Configuration Secret](#configuration-secret)
1. [Running tests](#running-tests)
1. [Command Line Things](#command-line-things)
1. [Endpoints](#endpoints) to get you started


## What this Repo is

A quick and easy way to get rolling with Python 3, Flask 1.1.2, the 
Flask-RESTful framework for building an API, database storage with PostgreSQL,
TDD with test coverage built in, and deployment notes on continuous integration
with Travis-CI which deploys to Heroku afterward.

This is a shell of a project with a single 'users' table, and RESTful routes
to CRUD a user via JSON. Full happy path and sad path testing is included. It
sets up CORS as well.


## What this Repo is Not

This is not a step-by-step guide of how to use Python, Flask, Flask-RESTful,
PostgreSQL, SQLalchemy, Travis-CI or Heroku. There are other learning channels
for that.


## What do to after cloning

You don't have to fork this repo unless you want to contribute back to it in
the future.

After you clone this repo, delete the `.git` folder. This is your project, not
mine. I don't need to show up as a contributor on other projects out there.
Giving me a footnote credit in your own README back to this repo is enough.

Then, do everything under here:


## Virtual Environment setup

```bash
# build a virtual environment to install your Python packages
python3 -m venv ./venv

# 'activate' the virtual environment for your project
# do this every time you start a new terminal and enter your project folder
source venv/bin/activate

# install your Python packages
pip3 install -r requirements.txt
```

To shut off your virtual environment, run `deactivate` at a terminal where you
have an active virtual environment.


## Requirements

Here's a brief explanation of what's in the requirements.txt file and why:

Flask setup:
```
Flask==1.1.2
Flask-RESTful==0.3.8
```

Database setup:
```
Flask-SQLAlchemy==2.4.4
psycopg2-binary==2.8.6
SQLAlchemy==1.3.19
flask_migrate==2.5.3
```

Cool command-line processor:
```
flask-script==2.0.6
```

CORS setup
```
Flask-Cors==3.0.9
```

Security, will "sanitize" user input; also recommend sanitizing things on the
way OUT of your database as well
```
bleach==3.2.1
```

Testing stuff
```
pytest==6.1.0
coverage==5.3
```

Production WSGI
```
gunicorn==20.0.4
```

Python code styling checks
```
pep8==1.7.1
pycodestyle==2.6.0
```

To run the code style checks, run this:
```bash
pycodestyle .| grep -v "venv\|migrations"
```


## Database Setup

Let's assume your project is called "shield":

```bash
createdb shield_dev
createdb shield_test

export DATABASE_URL=postgresql://localhost:5432/shield_dev

# examine any database models you have set up
python3 manage.py db migrate

# "upgrade" your database schema to use the changes you've made in your models
python3 manage.py db upgrade

# then apply the same for your test database:
export DATABASE_URL=postgresql://localhost:5432/shield_test
python3 manage.py db upgrade

```

Note that this pattern is different than Rails. You change your models, then
you run the "migrate" tool which builds your migration file, then you apply the
migration file to your database with the "upgrade" command.

To roll back a database change, use "downgrade" instead of "upgrade".

The code will use an environment variable called DATABASE_URL that you will
need to set on Travis-CI and on Heroku. Your Travis-CI setting for this flag
will be something like what you have above for your test database, since 
PostgreSQL will be running on "localhost" on Travis-CI.

On Heroku, though, you'll need to get your database credentials from the Heroku
user interface and it'll be a very long string that approximately follows this
pattern:

```
postgresql://username:password@hostname:port/database_name
```


## Heroku Procfile

The Profile provided should be all you need.

```
web: gunicorn run:app
```

At a high level, `gunicorn` is a production-ready HTTP request/response 
handler. It will execute your "runner" file, in this case the `run:` portion
of the Procfile references your `run.py` script. If you change the runner
filename, you'll need to change it here too (just without the .py extension).

The `:app` portion references the variable in `run.py` on line 10 that it uses
to actually execute your Flask application. 


## Travis-CI Setup

Check the `.travis.yml` file. You'll need to update a database name in there,
and set up your Heroku stuff.

I recommend making a copy of the contents of this file, and then running
`travis setup heroku` and allow it to overwrite what it needs, then paste back
in the parts that the setup removes.


## Configuration Secret

Be sure to generate a long random string and set an environment variable
called SECRET_KEY on your local environment and especially on Heroku.


## Running Tests

Here's where I nerd out on testing.

I hand this repo to you with 100% test coverage in 27 tests with 132 assertions
just to check on a handful of user crud endpoints.

If you just want to run your tests, `pytest` by itself will do the job.

If you want some cool test coverage reports similar to SimpleCov, you can do
the following:
```bash
# remove any previous test caching, previous coverage reports, and a database
# of coverage data from the last time you ran this
rm -rf .pytest_cache/ coverage_html_report/ .coverage

# set your database url for your test database and use 'coverage' to launch
# pytest
DATABASE_URL=postgresql://localhost/shield_test coverage run -m pytest

# generate the HTML reports
coverage html

# open the coverage report in your browser
open coverage_html_report/index.html

# count how many 'assert' calls you make in your tests
# my last project using this structure had 76 tests and 296 assertions that
# made sure every little thing got tested
grep -R assert tests | grep '.py:' | wc -l
```


## Command Line Things

The 'flask-script' package allows you to set up custom commands, similar to
rake tasks in Rails.

run `python3 manage.py routes` to see a list of your endpoint routes:
```
Map([<Rule '/api/v1/users' (POST, GET, HEAD, OPTIONS) -> usersresource>,
 <Rule '/api/v1/users/<user_id>' (PATCH, DELETE, GET, OPTIONS, HEAD) -> userresource>,
 <Rule '/static/<filename>' (OPTIONS, GET, HEAD) -> static>])
```

I also have one called "db_seed" if you need something to pre-seed a database.

## Endpoints

- GET and PATCH endpoints will return a 200 status code on success
- POST endpoints will return a 201 status code on success
- DELETE endpoints will return a 204 status code on success

Failure conditions will return an appropriate 400-series or 500-series error
and a JSON payload indicating helpful errors in a format such as:
```json
{
  "error": 404,
  "message": "Resource not found"
}
```

---
#### GET /api/v1/users

Description:
- fetches all users in the database
- returns 200 status code on success

Required Request Headers:
- none

Required Request Body:
- none

Response Body: (TBD)
```json
{
  "success": true,
  "results": [
    {
      "id": 1,
      "username": "ian",
      "email": "ian.douglas@iandouglas.com",
      "links": {
        "get": "/api/v1/users/1",
        "patch": "/api/v1/users/1",
        "delete": "/api/v1/users/1",
        "index": "/api/v1/users"
      }
    },
    {...} 
  ]
}
```

---
#### GET /api/v1/users/1

Description:
- fetches one user from the database
- returns 200 status on success

Required Request Headers:
- none

Required Request Body:
- none

Response Body: (TBD)
```json
{
  "success": true,
  "id": 1,
  "username": "ian",
  "email": "ian.douglas@iandouglas.com",
  "links": {
    "get": "/api/v1/users/1",
    "patch": "/api/v1/users/1",
    "delete": "/api/v1/users/1",
    "index": "/api/v1/users"
  }
}
```

---
#### DELETE /api/v1/users/1

Description:
- deletes one user from the database
- returns 204 status on success 

Required Request Headers:
- none

Required Request Body:
- none

Response Body: (TBD)
- none

---
#### POST /api/v1/users

Description:
- creates a user
- returns 201 status code on success

Required Request Headers:
- none

Required Request Body:
- JSON payload of:
  - 'username', required, must be unique, cannot be blank
  - 'email', required, must be unique, cannot be blank
```json
{
  "username": "ian",
  "email": "ian.douglas@iandouglas.com"
}
```

Response Body: (TBD)
- json payload indicating user was created, including RESTful routes
  to edit/delete/get the user record
```json
{
  "success": true,
  "id": 1,
  "username": "ian",
  "email": "ian.douglas@iandouglas.com",
  "links": {
    "get": "/api/v1/users/1",
    "patch": "/api/v1/users/1",
    "delete": "/api/v1/users/1",
    "index": "/api/v1/users"
  }
}
```
#### PATCH /api/v1/users/1

Description:
- updates a user by ID

Required Request Headers:
- none

Required Request Body:
- JSON payload of:
  - 'username', optional, must be unique, cannot be blank
  - 'email', optional, must be unique, cannot be blank
```json
{
  "username": "ian",
  "email": "ian.douglas@iandouglas.com"
}
```

Response Body: (TBD)
- json payload indicating road trip was updated, including a restful route
  to fetch road trip information
```json
{
  "success": true,
  "id": 1,
  "username": "ian",
  "email": "ian.douglas@iandouglas.com",
  "links": {
    "get": "/api/v1/users/1",
    "patch": "/api/v1/users/1",
    "delete": "/api/v1/users/1",
    "index": "/api/v1/users"
  }
}
```
