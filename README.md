# Capstone project

This is the final project for Udacity's Full Stack Nanodegree program.

It's currently hosted on Heroku and can be accessed on [capstone-gafeol.herokuapp.com](https://capstone-gafeol.herokuapp.com/).

The focus of the project is developing a Movie and Actor API, best described in the following sessions, using Flask, SQLAlchemy and Postgres.

## Motivation for project

The main motivation for this project was reviewing the subjects treated on Udacity's FSND.

With this project I was able to review concepts such as:

- Creating database migrations
- SQLAlchemy and Postgres development
- Flask API development
- Authentication with Auth0
- Roles-based access control
- Unit tests in Python
- Deployment on Heroku
- Code and project Documentation
- PEP 8 style guidelines

Thus practicing some of the skills necessary for a full-stack developer.

## Project set up

To install the project dependencies, run `pip install -r requirements.txt`.

By running:

```bash
. ./setup.sh
```

You'll have configured the development variables required by Flask.

Later running:

```bash
flask run
```

Should start running the project in Debug mode.

Then, by accessing [http://127.0.0.1:5000/](http://127.0.0.1:5000/) one should be able to locally access the Capstone project website.

## API

The API is configured to answer with the following response codes:

```bash
200: Success
400: Bad request
401: Unauthorized
404: Cannot be found
```

If a certain route requires a permission and that permission is missing, a 401 error will be returned, with a message explaining further the reason for the error, such as:

```bash
{
  "error": 401,
  "message": "Authorization header is expected.",
  "success": false
}
```

The API tests are included in the `test_app.py` file, on the root project folder.

### Actor

#### GET /actors

The permission "read:actor" is required for this request.

On successful requests, this endpoint responds with a 200 status and body:

```bash
{
    "success": True,
    "actors": [...]
}
```

#### POST /actors

The permission "add:actor" is required for this request.

On successful requests, this endpoint responds with a 201 status and body:

```bash
{
    "success": True,
    "created": 1
}
```

With "created" having the id of the created object.

#### PATCH /actors

The permission "modify:actor" is required for this request.

This method expects the request body to have the 'id' of the object that is being changed.

On successful requests, this endpoint responds with a 200 status and body:

```bash
{
    "success": True,
    "patched": {...}
}
```

With "patched" having the changed object.

#### DELETE /actors/<int:id>

The permission "delete:actor" is required for this request.

On successful requests, this endpoint responds with a 200 status and body:

```bash
{
    "success": True,
    "patched": {...}
}
```

With "patched" having the changed object.

### Movie

#### GET /movies

The permission "read:movie" is required for this request.

On successful requests, this endpoint responds with a 200 status and body:

```bash
{
    "success": True,
    "movies": [...]
}
```

#### POST /movies

The permission "add:movie" is required for this request.

On successful requests, this endpoint responds with a 201 status and body:

```bash
{
    "success": True,
    "created": 1
}
```

With "created" having the id of the created object.

#### PATCH /movies

The permission "modify:movie" is required for this request.

This method expects the request body to have the 'id' of the object that is being changed.

On successful requests, this endpoint responds with a 200 status and body:

```bash
{
    "success": True,
    "patched": {...}
}
```

With "patched" having the changed object.

#### DELETE /movies/<int:id>

The permission "delete:movie" is required for this request.

On successful requests, this endpoint responds with a 200 status and body:

```bash
{
    "success": True,
    "patched": {...}
}
```

With "patched" having the changed object.

## RBAC

The authentication is made via "Bearer Token" using the Auth0 authentication platform.

The roles defined are:

- Casting Assistant

An assistant has the "read:actor" and "read:movie" permissions.

Sample credentials:

Email: assistant@assistant.com
Password: 8hdZAAMx8E9gzMT

- Casting Director

A casting director has the permissions for casting assistant plus "add:actor", "patch:actor", "delete:actor" and "patch:movie".

Sample credentials:

Email:  director@director.com
Password: q9fdgGKdYw8JtVP

- Executive Director

An executive director has the permissions for a casting director plus "add:movie" and "delete:movie".

Sample credentials:

Email: admin@admin.com
Password: v8RKK3si3zvwQUz

The required tokens for each role were added on the [.flaskenv](.flaskenv) file, but if, for some reason, they have already expired you can use the application web interface to generate new tokens using the sample credentials specified.


## Secrets

A `.flaskenv` file should be created containing the following secrets:

```bash
AUTH0_SECRET=xxxxxxxxxxxxxxxxx
EXECUTIVE_TOKEN=xxxxxxxxxxxxxxxxxx
DIRECTOR_TOKEN=xxxxxxxxxxxxxxxxxxx
ASSISTANT_TOKEN=xxxxxxxxxxxxxxxxxxxx
FLASK_SECRET_KEY=xxxxxxxxxxxxxx
AUTH0_DOMAIN=xxxxxxxxxxxxxxxxxxxxx
API_AUDIENCE=xxxxxxxxxxxxxxxxxxxxxx
CLIENT_ID=xxxxxxxxxxxxxxxxxxx
```

