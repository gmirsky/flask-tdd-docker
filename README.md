# Python Flask-RESTX container

Illustration of a test based development docker container example with Python, Flask, SQL-Alchemy, Postgres and Docker-compose.

This sample docker application utilizes Python and Flask along with utilizing pytest, flake8, black, isort, werkzeug, sql-alchemy and swagger to store data in a separate Postgres database container and build the needed Rest API interfaces and support GUIs.

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
        "username": "old_devil",
        "email": "old_devil@vanapagan.com",
        "created_date": "2021-09-27T19:25:54.391979"
    },
    {
        "id": 2,
        "username": "seven_twelfths",
        "email": "seven_twelfths@septunx.com",
        "created_date": "2021-09-27T19:25:54.391979"
    },
    {
        "id": 3,
        "username": "ima.dummy",
        "email": "ima.dummy@fakedomain.com",
        "created_date": "2021-09-27T19:25:54.391979"
    },
    {
        "id": 4,
        "username": "go_away",
        "email": "go_away@noreply.com",
        "created_date": "2021-09-27T19:25:54.391979"
    },
    {
        "id": 5,
        "username": "pebcak",
        "email": "pebcak@braindeadusers.com",
        "created_date": "2021-09-27T19:25:54.391979"
    }
]
$
```

## Testing

### Kick off the coded pytest functional and unit tests

All tests can be found in the `/tests` directory and subdirectories.

```
$ docker-compose exec api python -m pytest "src/tests" -p no:warnings
================================== test session starts ==================================
platform linux -- Python 3.9.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /usr/src/app/src/tests, configfile: pytest.ini
plugins: xdist-2.2.1, cov-2.12.0, forked-1.3.0
collected 34 items

src/tests/test_admin.py ..                                                        [  5%]
src/tests/test_users.py ..............                                            [ 47%]
src/tests/test_users_unit.py ..............                                       [ 88%]
src/tests/functional/test_ping.py .                                               [ 91%]
src/tests/unit/test_config.py ...                                                 [100%]

================================== 34 passed in 0.77s ===================================
$
```

### Run the tests with code coverage

Code coverage tells you how much of your code is tested by your test scripts and conditions.

```bash
$ docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src"
================================ test session starts =================================
platform linux -- Python 3.9.5, pytest-6.2.4, py-1.10.0, pluggy-0.13.1
rootdir: /usr/src/app/src/tests, configfile: pytest.ini
plugins: xdist-2.2.1, cov-2.12.0, forked-1.3.0
collected 34 items

src/tests/test_admin.py ..                                                     [  5%]
src/tests/test_users.py ..............                                         [ 47%]
src/tests/test_users_unit.py ..............                                    [ 88%]
src/tests/functional/test_ping.py .                                            [ 91%]
src/tests/unit/test_config.py ...                                              [100%]

----------- coverage: platform linux, python 3.9.5-final-0 -----------

Name                        Stmts   Miss Branch BrPart  Cover
-------------------------------------------------------------

src/__init__.py                21      1      2      0    96%
src/api/__init__.py             6      0      0      0   100%
src/api/ping.py                 6      0      0      0   100%
src/api/users/__init__.py       0      0      0      0   100%
src/api/users/admin.py          7      0      0      0   100%
src/api/users/crud.py          22      0      0      0   100%
src/api/users/models.py        17      0      2      1    95%
src/api/users/views.py         63      0     10      0   100%

src/config.py                  15      1      2      1    88%
-------------------------------------------------------------

TOTAL                         157      2     16      2    98%

================================= 34 passed in 1.48s =================================
$
```

You can also run the tests with coverage and generate an HTML report of the results

```bash
$ docker-compose exec api python -m pytest "src/tests" -p no:warnings --cov="src" --cov-report html
```

## Code health

### Lint the python code to make it standard.

```bash
$ docker-compose exec api flake8 src
```

### Python Black and Python Isort

#### Run black and isort with check options

```bash
$ docker-compose exec api black src --check
$ docker-compose exec api isort src --check-only
```

#### Fix formatting and python imports with black and isort

```bash
$ docker-compose exec api black src
$ docker-compose exec api isort src
```

### Swagger

Python Swagger will automatically generate OpenAPI specifications and documentation. Since we are using Flask-RESTX, it is automatically included. All that is needed is to redirect the output to `/doc` which is accomplished by code in `src/api/__init__.py`

api = Api(version="1.0", title="Users API", doc="/doc") redirects the documentation endpoint from `http://localhost:5004/` to `http://localhost:5004/doc`

Open your browser to http://localhost:5004/doc and you should see the following.

![doc1](/Users/gregorymirsky/flask-tdd-docker/doc1.png)

If you click on one of the entries you get even more information. All of it automatically generated.

![doc2](/Users/gregorymirsky/flask-tdd-docker/doc2.png)

Database admin GUI

Additionally, Flask-RESTX allows you to genrate a GUI (that should only be deployed in DEV and/or QA) to aid in debugging. Navigate to http://localhost:5004/admin/user/ 

![admin](/Users/gregorymirsky/flask-tdd-docker/admin.png)

This is a GUI all driven off of the Python Flask-RESTX libraries.