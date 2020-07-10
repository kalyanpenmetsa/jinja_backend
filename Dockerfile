FROM python:3.7-alpine
WORKDIR /app
RUN apk add --no-cache gcc musl-dev linux-headers
COPY app/ .
COPY requirements.txt .
RUN pip install -r requirements.txt
CMD ["uwsgi", "--socket", "0.0.0.0:4000", "--protocol=http", "-w", "wsgi:app"]
