# FSND_CAPSTONE

## Introduction

capstone project is a casting agency company that is responsable for creating movies and casting actors for those movies.  


## Getting started

### run postgresql on terminal

`sudo service postgresql start`

### Database Setup for tests

`createdb capstone`

### PIP Dependencies

`pip install -r requirements.txt`

### run flask app locally

`python3 app.py` || `python app.py`

### Auth0 user login url

to login to auth0 and generate token with role permissions

`locally`
  https://dev-f0u7wasufi70tiya.us.auth0.com/authorize?
  audience=capstone&
  response_type=token&
  client_id=3nKZJN3Z9YmYErGJYC6Kw3tUKSGDe8Oc&
  redirect_uri=http://localhost:8080

`Deployed URL`
[render_server](https://dev-f0u7wasufi70tiya.us.auth0.com/authorize?
  audience=capstone&
  response_type=token&
  client_id=3nKZJN3Z9YmYErGJYC6Kw3tUKSGDe8Oc&
  redirect_uri=https://fsnd-capstone-2vf2.onrender.com)
  
## User Roles to login to Auth0

## Casting Assistant

* `Can view actors and movies

`Email: <casting_assistant@example.com>`
`Password: ABcd12345`
  
## Casting Director

* All permissions a Casting Assistant has and…
* Add or delete an actor from the database
* Modify actors or movies

`Email: <casting_director@example.com>`
`Password: ABcd12345`

### Executive Producer

* All permissions a Casting Director has...
* Add or delete a movie from the database

`Email: executive_producer@example.com`
`Password: ABcd12345`

### deployed webservice url on render

[capstone_app](https://fsnd-capstone-2vf2.onrender.com)

### url endpoint
`GET /movies`
get all movies from the database

input:
  url: http://localhost:8080/movies
    headers:{'Authorization': Bearer {token}}
{
 "movies": [
    {
        "id": 1,
        "Release Date": "2014/8/24",
        "Title": "John wick"
    },
    {
     "id": 2,
      "Release Date": "2023\7\21",
      "Title": "Oppenheimer"
    },
    ],
    "success": true
}

`GET /movie/{id}`
get specified movie with id that is provided.

input:
  url: http://localhost:8080/movie/1
    headers:{'Authorization': Bearer {token}}
Output:
{
    {
        "id": 1,
        "Release Date": "2014/8/24",
        "Title": "John wick"
    },
  "success": true
}

`PATCH /movie/{id}`
update movie data with the id that is provided

Input:
  url: http://localhost/movie/1
    headers:{'Authorization': Bearer {token}}
    body:
    {
        "id": 1,
        "Release Date": "2014/8/24",
        "Title": "John"
    },

Output:
{
    {
        "id": 1,
        "Release Date": "2014/8/24",
        "Title": "John"
    },
  "success": true
}

`POST /movie`

create a movie

Input:
  url: http://localhost:8080/movie
  headers:{'Authorization': Bearer {token}}
  body:
{
  "id": 3
  "release_date": "2024/1/11",
  "title": "hunger games",
}

Output:
{
 {
  "id": 3
  "release_date": "2024/1/11",
  "title": "hunger games",
}
  "success": true
}

`DELETE /movie/{id}`
delete a movie from a database

Input:
  url: DELETE http://localhost:8080/movie/5
  headers:{'Authorization': Bearer {token}}

Output:
{
  "success": True, "message": 'specified movie has been deleted successfully'
}

`GET /actors`
get all actors from the database

input:
  url: http://localhost:8080/actors
    headers:{'Authorization': Bearer {token}}
{
 "actors": [
    {
        "id": 1,
        "name": "Cillian Murphy",
        "age":47,
        "gender": "male",
        "movie_id":2
    },
     {
        "id": 2,
        "name": "Keanu Reeves",
        "age":59,
        "gender": "male",
        "movie_id":1
    },
    ],
    "success": true
}

`GET /actor/{id}`
get specified movie with id that is provided.

input:
  url: http://localhost:8080/actor/1
    headers:{'Authorization': Bearer {token}}
Output:
{
    {
        "id": 1,
        "name": "Cillian Murphy",
        "age":47,
        "gender": "male",
        "movie_id":2
    },
  "success": true
}

`PATCH /actor/{id}`
update movie data with the id that is provided

Input:
  url: http://localhost/actor/1
    headers:{'Authorization': Bearer {token}}
    body:
    {
        "id": 1,
        "name": "Cillian",
        "age":47,
        "gender": "male",
        "movie_id":2
    },

Output:
{
     {
        "id": 1,
        "name": "Cillian",
        "age":47,
        "gender": "male",
        "movie_id":2
    },
  "success": true
}

`POST /actor`

create a movie

Input:
  url: http://localhost:8080/actor
  headers:{'Authorization': Bearer {token}}
  body:
    {
        "id": 3,
        "name": "Robert John Downey",
        "age":58,
        "gender": "male",
        "movie_id":3
    },

Output:
{
    {
        "id": 3,
        "name": "Robert John Downey",
        "age":58,
        "gender": "male",
        "movie_id":3
    },
  "success": true
}

`DELETE /actor/{id}`
delete an actor from a database

Input:
  url: localhost:8080/actor/5
  headers:{'Authorization': Bearer {token}}

Output:
{
  "success": True,
   "message": 'specified actor has been deleted successfully'
}

Error Handling
output format:
{   
    "success": False, 
    "error": 422, 
    "message": "Unprocessable"
}
Error Handling types:

* 400: Bad Request
* 404: Resource Not Found
* 405: Method Not Allowed
* 422: Not Processable
* 500: Internal Server Error