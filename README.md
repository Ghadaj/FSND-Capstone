# Casting Agency

## Introduction
This is the capstone project for Udacity FSND, the aim of this project is to showcase the skills and knowledge gained throughout the course. In this project I created flask app with API endpoints to interact with the CastingAgency DB, for example to get the list of actors in the agency, or to remove an actor. The application is hosted live on Heroku and uses Auth0 for authentication.

## Getting Started
### Heroku URL
https://mycastingagency.herokuapp.com


### Authentication: 
Auth0 tokens used for the authentication. There are 3 roles for the casting agency:

**Casting Assistant**

- Can view actors and movies

**Casting Director**

- Can view actors and movies

- Add or delete an actor from the database

- Modify actors or movies

**Executive Producer**

- Can view actors and movies

- Add or delete an actor from the database

- Modify actors or movies

- Add or delete a movie from the database

## Test
You can test the app by running the test_app.py or using Postman collection.
Please replace ASSISTANT_TOKEN, DIRECTOR_TOKEN, and PRODUCER_TOKEN in setup with access tokens before you run th test_app.py

To get the access tokens Please visit https://cs-fsnd.us.auth0.com/authorize?audience=castingAgency&response_type=token&client_id=RNBSVZ42ii0OKMlOaRYSPaX9LboZoV0F&redirect_uri=https://localhost:8080/resultand sign in with login-credentials provided in the setup.sh, after you successfully signed in extract the access_token from the routed page and insert it in setup.sh file

## Resource Endpoint 
### GET '/movies'
* Genreal
    * Fetches the list of movies
    * Request Arguments: None
    * Returns: An object that contains movies array, and a success boolean value.
* Sample: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies`

```
{
    "movies": [
        {
            "id": 1,
            "release_date": "2021-09-12",
            "title": "My Movie"
        },
        {
            "id": 3,
            "release_date": "2021-09-22",
            "title": "My Movie"
        }
    ],
    "success": true
}

```


### GET '/actors'
* Genreal
    * Fetches the list of actors
    * Request Arguments: None
    * Returns: An object that contains actors array, and a success boolean value.
* Sample: `curl -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors`

```
{
    "actors": [
        {
            "age": 45,
            "gender": "Female",
            "id": 4,
            "name": "Actor"
        },
        {
            "age": 45,
            "gender": "Female",
            "id": 5,
            "name": "Actor"
        },
        {
            "age": 45,
            "gender": "Female",
            "id": 3,
            "name": "Actor"
        }
    ],
    "success": true
}

```

### POST '/movies'
* General
    * Add a new movie
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the created movie.
* Sample: `curl http://127.0.0.1:5000/movies -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"title\": \"My Movie\",\"releas_date\": \"2021-09-22\"}"`
```
{
    "title": "My Movie",
    "releas_date": "2021-09-22"
    
}
```

### POST '/actors'
* General
    * Add a new actor
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the created actor.
* Sample: `curl http://127.0.0.1:5000/actors -X POST -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"name\": \"Actor\",\"age\": \"45\",\"gender": \"Female\"}"`
```
{
    "name": "Actor",
    "age": "45",
    "gender": "Female"
    
}

```


### PATCH '/movies/1'
* General
    * Updates the specified movie
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the updated movie.
* Sample: `curl http://127.0.0.1:5000/movies/1 -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"title\":\"My updated Movie\"}"`
```
{   
    "title": "My updated Movie",
    "releas_date": "2021-09-22"
    
}
```

### PATCH '/actors/1'
* General
    * Updates the specified actor
    * Request Arguments: None
    * Returns: An object that contains a success boolean value and the updated actor.
* Sample: `curl http://127.0.0.1:5000/actors/1 -X PATCH -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d "{\"name\":\"Updated Actor\"}"`
```
{
    "name": "Updated Actor",
    "age": "45",
    "gender": "Female"
    
}
```

### DELETE '/movies/2'
* Genreal
    * Delete the specified movie
    * Request Arguments: The movie's ID
    * Returns: An object than contains a success boolean value and the ID of the deleted movie.
* Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/movies/2`
```
{
  "deleted": 2,
  "success": true
}
```

### DELETE '/actors/2'
* Genreal
    * Delete the specified actor
    * Request Arguments: The actor's ID
    * Returns: An object than contains a success boolean value and the ID of the deleted actor.
* Sample: `curl -X DELETE -H "Authorization: Bearer $TOKEN" http://127.0.0.1:5000/actors/2`
```
{
  "deleted": 2,
  "success": true
}
```
