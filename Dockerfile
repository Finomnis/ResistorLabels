FROM python:3.7-slim
WORKDIR /resistorLabels
COPY requirements.txt /resistorLabels
COPY Roboto-Bold.ttf /resistorLabels

RUN apt update && apt install -y libpq-dev gcc
RUN pip install -r requirements.txt