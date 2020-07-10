FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers nginx supervisor \
    && adduser -D -H -u 1000 -s /bin/sh www-data -G www-data \
    && chown -R www-data:www-data /app
COPY app/ .
COPY requirements.txt .
COPY server-conf/nginx.conf /etc/nginx/
COPY server-conf/supervisord.conf /etc/
COPY server-conf/uwsgi.ini /app/
COPY application.conf /app/
RUN pip install -r requirements.txt
CMD ["/usr/bin/supervisord"]
