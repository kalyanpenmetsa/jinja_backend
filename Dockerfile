FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers nginx
COPY app/ .
COPY requirements.txt .
COPY nginx.conf /etc/nginx/
RUN pip install -r requirements.txt
CMD ["uwsgi", "--ini=uwsgi.ini"]
