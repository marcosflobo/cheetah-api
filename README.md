[![Build Status](https://travis-ci.org/marcosflobo/cheetah-api.svg?branch=master)](https://travis-ci.org/marcosflobo/cheetah-api) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3d73f037de7f44d18f03215fc717df12)](https://www.codacy.com/app/marcosflobo/cheetah-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=marcosflobo/cheetah-api&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/3d73f037de7f44d18f03215fc717df12)](https://www.codacy.com/app/marcosflobo/cheetah-api?utm_source=github.com&utm_medium=referral&utm_content=marcosflobo/cheetah-api&utm_campaign=Badge_Coverage)
# cheetah-api
Backend API for [cheetah](https://github.com/marcosflobo/cheetah) Web application to visualize and manage graphical representation of work using agile methodologies for agile teams

# Agile board
Please checkout or [Kanban board](https://github.com/marcosflobo/cheetah/projects/1) to follow up the ongoing tasks.

# Docker deployment
The minimal setup is:
- PostgreSQL database with data
- Cheetah-api running and pointing to the PostgreSQL database

For this, we provide Dockefiles for both services. We will:
1. Setup configuration file
2. Build PostgreSQL and cheetah-api Docker images
3. Create a Docker network to be able to communicate both services
4. Deploy PostgreSQL and cheetah-api Docker containers 
## Setup configuration file
Edit ./etc/config.conf file and set parameters
```ini
host = 0.0.0.0
[...]
db_host = cheetah_api_postgresql_test
```
Save the file and let't create the Docker image

## Build docker image cheetah-api
From the project dir, run
```bash
docker build -t cheetah_api .
```

## Build Docker image PostgreSQL
From ./integration_tests dir, run:
```bash
docker build -t cheetah_api_postgresql .
```
Now we have the images created, let's setup the network and run the containers.

## Create Docker network
We need a Docker network to be able to communicate both services.
```bash
docker network create cheetah_net
```
Please note that, if you change here the network name, you have to change it too in the next docker commands.

## Run PostgreSQL database as Docker container
We provide a PostgreSQL Dockerfile with test data (See next chapter for this). You can build the image and then run the container.
```bash
docker run --rm -p 5432:5432 --net cheetah_net --name cheetah_api_postgresql_test cheetah_api_postgresql
```

## Run cheetah-api as Docker container
We provide a Dockerfile to run cheetah-api service
```bash
docker run --rm -p 8081:80 --net cheetah_net --name cheetah-api cheetah_api:latest
```
Where 8081 is the port in your host and the 80 is the port configured for cheetah-api in etc/config.conf file.
Please note that the container name for PostgreSQL service should be set in "db_host" parameter in ./etc/config.conf file. 

## Testing the Docker environment
From a host, just run:
```bash
curl -d '{"authenticate":{"username":"foo","password":"foo"}}' -H "Content-Type: application/json" -X POST http://localhost:8081/v1/authenticate
```
Please note that user "foo" with password "foo" is provided in the PostgreSQL Dockerfile as sample data.

# Quick integration tests setup
## Setup PosgreSQL database using Docker
1. Install docker in your system
2. Run ./integration_tests/docker_up.sh

This will put in place small demo data, like user foo/foo.

## Run server
1. Modify the ./integration_tests/etc/config.conf file updating the port from the port opened in the PosgreSQL docker container 
2. Run
```bash
python -m cheetahapi.main -c /path/to/cheetah-api/integration_tests/etc/config.conf
```
You will get something like
```bash
 * Serving Flask app "main" (lazy loading)
 * Environment: production
   WARNING: Do not use the development server in a production environment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://localhost:8081/ (Press CTRL+C to quit)
```
Please see [here how to interact with API](https://github.com/marcosflobo/cheetah-api/blob/master/docs/cheetah-api.md), the first thing is GET A TOKEN.

# Tests
To execute the tests and get the report xml file. From the root dir of the project:
```bash
nosetests -w tests --with-xunit --with-coverage --cover-package=cheetahapi
```
