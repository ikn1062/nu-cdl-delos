# syntax=docker/dockerfile:1

FROM python:3.10-slim-bullseye

WORKDIR /app

COPY mongopy.py .
COPY requirements.txt .

RUN pip install -r requirements.txt

CMD [ "python3", "-u", "mongopy.py"]

