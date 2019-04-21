# Udacity Data Engineer Nanodegree Project 1

Extract stuff with Postgres and Pandas

## Getting Started

### Prerequisites

Python 3

Docker Compose

Run the following commands to get the docker container up and running locally:

```
docker-compose up -d
```

To close the docker container when done:

```
docker-compose down
```

Run the following commands in `project_template/` to carry out the ETL part of the project

```
virtualenv --python=python3 venv
. venv/bin/activate
pip install -r requirements.txt
python create_tables.py
python etl.py
```

To connect to the db to verify the tables are populated:

```
psql "postgresql://student:student@127.0.0.1/sparkifydb"
```
