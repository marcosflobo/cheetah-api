docker build -t cheetah_api_postgresql .
docker run --rm -p 5432:5432 --net cheetah_net --name cheetah_api_postgresql_test cheetah_api_postgresql
