# Pull base image
FROM python:3.9.6-alpine

# Install dependencies
COPY ./requirements.txt /app/requirements.txt

#Set Working Directory
WORKDIR /app
COPY . ./app
RUN apk add --no-cache gcc musl-dev build-base postgresql-dev libffi-dev
RUN pip install -r /code/requirements.txt

# Set environment varibles
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


EXPOSE 8000
