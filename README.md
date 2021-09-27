# Python Flask-RESTX container

A test based development docker container example with Python, Flask, Postgres and Docker

This sample docker application utilizes Python and Flask along with utilizing pytest, flake8, black, isort, werkzeug and swagger to store data in a separate Postgres database container.

The intent of this example is to illustrate building docker application containers with a testing, linting and formatting framework simulatenously with the application code to insure code quality and to spot errors early in the development process.

This RESTful API will follow RESTful design principles using basic HTTP verbs: GET, POST, PUT, and DELETE.

|  Endpoint  | HTTP Method | CRUD Method |      Result       |
| :--------: | :---------: | :---------: | :---------------: |
|   /users   |     GET     |    READ     |   get all users   |
| /users/:id |     GET     |    READ     | get a single user |
|   /users   |    POST     |   CREATE    |    add a user     |
| /users/:id |     PUT     |   UPDATE    |   update a user   |
| /users/:id |   DELETE    |   DELETE    |   delete a user   |

## Pre-requisites

- Python 3.9
- Docker 20.x or later
- Docker-compose 1.29.x or later

### Check your versions

Check your Python version:

```bash
$ python3 --version
Python 3.9.7
```

Check your docker and docker-compose versions:

```bash
$ docker -v
Docker version 20.10.6, build 370c289
```

```bash
$ docker-compose -v
docker-compose version 1.29.1, build c34c88b2
```

## Clone the repository to a local directory

```bash
$ git clone .......
cd ........
```

## Build the containers

### Build the docker images

```bash
$ docker-compose build --no-cache
```

### View the docker images you just built

```bash
$ docker image ls
REPOSITORY                TAG       IMAGE ID       CREATED          SIZE
flask-tdd-docker_api      latest    0e7164cb677b   2 minutes ago   671MB
flask-tdd-docker_api-db   latest    cb035db0b1f2   2 minutes ago   192MB
$
```

### View the current docker container networks

```bash
$ docker network ls
NETWORK ID     NAME      DRIVER    SCOPE
a5673b5d4434   bridge    bridge    local
6695e6307922   host      host      local
be2a79923637   none      null      local
$
```

### Run the containers

```bash
$ docker-compose up -d
```

Check the docker container networks again to see the new docker network

```bash
$ docker network ls
NETWORK ID     NAME                       DRIVER    SCOPE
a5673b5d4434   bridge                     bridge    local
58e7a42032ca   flask-tdd-docker_default   bridge    local
6695e6307922   host                       host      local
be2a79923637   none                       null      local
```

Check the docker volumes

```bash
$ docker volume ls
DRIVER    VOLUME NAME
local     275064541db7734bcaeda08e58f30249df7ecd43bd69efb7a5e493ef570c87e8
$
```



### Check the running containers

```bash
$ docker ps -a 
```

### Create the test Postgres database we will use with the containers

```bash
$ docker-compose exec api python manage.py recreate_db
```

### Check to see if we can do basic communication with our docker API container

```bash
$ curl http://localhost:5004/ping
```

You should get a response like this:

```json
{
    "status": "success",
    "message": "pong!"
}
```

### Check to see if we can access any user data in the database

```bash
$ curl http://localhost:5004/users 
```

You should get a response like this (which is expected)

```xml
[]
```

So, we have no data in the database so lets seed the database with some test data.

### Seed the database with test data

```bash
$ docker-compose exec api python manage.py seed_db
```

### Check again to see if we can access any user data in the database

```bash
$ curl http://localhost:5004/users
[
    {
        "id": 1,
        "username": "greg",
        "email": "greg@vanapagan.com",
        "created_date": "2021-09-27T19:07:01.238385"
    },
    {
        "id": 2,
        "username": "gregory",
        "email": "gregory@septunx.com",
        "created_date": "2021-09-27T19:07:01.238385"
    }
]
$
```

