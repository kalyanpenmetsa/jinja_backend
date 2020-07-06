FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP /app/src/main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000
RUN apk add --no-cache gcc musl-dev linux-headers
RUN pip install -r requirements.txt
COPY src/main.py .
CMD ["python", "-m", "flask", "run"]
