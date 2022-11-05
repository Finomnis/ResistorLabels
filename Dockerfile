FROM python:3.7-slim-bullseye
WORKDIR /resistorLabels
COPY requirements.txt /resistorLabels
COPY Roboto-Bold.ttf /resistorLabels
RUN echo 'deb http://deb.debian.org/debian bullseye contrib' >> /etc/apt/sources.list

RUN apt update && apt install -y libpq-dev gcc ttf-mscorefonts-installer
RUN pip install -r requirements.txt