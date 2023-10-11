FROM python:3.12-slim

COPY requirements.txt /
RUN pip install -r requirements.txt

COPY ./app /app

ENTRYPOINT ["python", "/app/main.py"]
