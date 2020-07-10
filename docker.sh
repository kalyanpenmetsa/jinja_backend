docker rm -f jinja
docker rmi jinja
docker build -t jinja .
docker run -d -it --name=jinja -p 9090:9090 jinja
