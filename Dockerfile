FROM python:3.7-alpine
MAINTAINER Sidhartha Roy

# This sets the environment such that python runs in
# unbuffered mode in a Docker container it prints output directly
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /requirements.txt
# no-cache --> dont store registry index in our dockerfile
# minimize the extra files and packages that are included in our
# dockercontainer
RUN apk add --update --no-cache postgresql-client
# sets up an alias for our dependencies that we
# can use to remove all the dependencies later
# these are all the temporary dependencies required to install
# the python dependencies i.e. the postgres client
RUN apk add --update --no-cache --virtual .tmp-build-deps \
     gcc libc-dev linux-headers postgresql-dev
RUN pip install -r /requirements.txt

# deletes the temporary requirements
RUN apk del .tmp-build-deps

RUN mkdir /app
WORKDIR /app
COPY ./app /app

# This create a new user called user
# -D means that the user will have app level authorization only
# This user is create to make sure that docker does not run
# the user with root permissions. This also limits the scope an attacker would
# have within our docker container
RUN adduser -D user
# This switched the user to user that was created in
# the previous line
USER user



