# Pull base image
FROM python:3.9.6-alpine

# Install dependencies
COPY ./requirements.txt /app/requirements.txt

# set work directory
WORKDIR /app
COPY . ./app
RUN apk add --no-cache gcc musl-dev build-base postgresql-dev libffi-dev
RUN pip install -r requirements.txt

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

EXPOSE 8080
