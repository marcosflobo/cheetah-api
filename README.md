[![Build Status](https://travis-ci.org/marcosflobo/cheetah-api.svg?branch=master)](https://travis-ci.org/marcosflobo/cheetah-api) [![Codacy Badge](https://api.codacy.com/project/badge/Grade/3d73f037de7f44d18f03215fc717df12)](https://www.codacy.com/app/marcosflobo/cheetah-api?utm_source=github.com&amp;utm_medium=referral&amp;utm_content=marcosflobo/cheetah-api&amp;utm_campaign=Badge_Grade) [![Codacy Badge](https://api.codacy.com/project/badge/Coverage/3d73f037de7f44d18f03215fc717df12)](https://www.codacy.com/app/marcosflobo/cheetah-api?utm_source=github.com&utm_medium=referral&utm_content=marcosflobo/cheetah-api&utm_campaign=Badge_Coverage)
# cheetah-api
Backend API for [cheetah](https://github.com/marcosflobo/cheetah) Web application to visualize and manage graphical representation of work using agile methodologies for agile teams

# Agile board
Please checkout or [Kanban board](https://github.com/marcosflobo/cheetah/projects/1) to follow up the ongoing tasks.

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