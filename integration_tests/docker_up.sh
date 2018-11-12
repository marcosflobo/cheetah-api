docker build -t cheetah_api_postgresql .
docker run --rm -P --name cheetah_api_postgresql_test cheetah_api_postgresql
