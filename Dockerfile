FROM python:3.8-slim-buster


# setting work directory
WORKDIR /usr/src/app


# env variables
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWEITEBYTECODE 1


# install psycopg dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*


# install dependencies

RUN pip install --upgrade pip
COPY ./requirements.txt ./
COPY ./.env ./
RUN pip install -r requirements.txt

COPY ./entrypoint /.
RUN chmod +x /entrypoint

COPY . .
ENTRYPOINT [ "/entrypoint" ]