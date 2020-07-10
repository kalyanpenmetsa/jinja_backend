FROM python:3.7-alpine
WORKDIR /app
ENV FLASK_APP /app/src/main.py
ENV FLASK_RUN_HOST 0.0.0.0
ENV FLASK_RUN_PORT 5000
COPY src/main.py .
COPY requirements.txt .
RUN python3 -m pip install -r requirements.txt
CMD ["python", "-m", "flask", "run"]
