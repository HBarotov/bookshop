# pull official base image
FROM python:3.10.4-slim-bullseye

# set work directory
WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update && apt-get install -y netcat \
    libcairo2 \
    libpango-1.0-0 \
    libpangocairo-1.0-0 \
    libgdk-pixbuf2.0-0 \
    libffi-dev \
    shared-mime-info \
    gobject-introspection \
    libgirepository1.0-dev \
    gettext \
    && apt-get clean

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
COPY ./wait-for.sh .
RUN sed -i "s/\r$//g" /usr/src/app/entrypoint.sh
RUN sed -i "s/\r$//g" /usr/src/app/wait-for.sh
RUN chmod +x /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/wait-for.sh

# copy project
COPY . .

# run entrypoint.sh
ENTRYPOINT ["/usr/src/app/entrypoint.sh"]