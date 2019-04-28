# Udacity Data Engineer Nanodegree Project 1

The objective is to build an ETL pipeline to analyze the data that's collected on songs and user activity on a new music streaming app, particularly what songs users are listening to.

## Getting Started

### Prerequisites

- Python 3
- Docker Compose

### Running locally

Run the following commands to get the docker container for Postgres up and running locally:

```
docker-compose up -d
```

To close the Postgres docker container when done:

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

### Data
- `Song datasets`: all json files are nested in subdirectories under */data/song_data*. A sample of a song file is:

```
{"num_songs": 1, "artist_id": "ARD7TVE1187B99BFB1", "artist_latitude": null, "artist_longitude": null, "artist_location": "California - LA", "artist_name": "Casual", "song_id": "SOMZWCG12A8C13C480", "title": "I Didn't Mean To", "duration": 218.93179, "year": 0}
```

- `Log datasets`: all json files are nested in subdirectories under */data/log_data*. A sample of a single row of a log file is:

```
{"artist":null,"auth":"Logged In","firstName":"Walter","gender":"M","itemInSession":0,"lastName":"Frye","length":null,"level":"free","location":"San Francisco-Oakland-Hayward, CA","method":"GET","page":"Home","registration":1540919166796.0,"sessionId":38,"song":null,"status":200,"ts":1541105830796,"userAgent":"\"Mozilla\/5.0 (Macintosh; Intel Mac OS X 10_9_4) AppleWebKit\/537.36 (KHTML, like Gecko) Chrome\/36.0.1985.143 Safari\/537.36\"","userId":"39"}
```

## Design rationale
The schema used is the Star Schema:
There is one main fact table containing all the measures associated to each event (user song plays,
and 4 dimentional tables, each (except time) with a primary key that is being referenced from the fact table.

For most `INSERT` SQL queries, we do nothing when there is a conflict of the primary key, except for the `user` table,
where we modify the `level` if the free tier user converts into a paid user.

### Custom types
`level` - enum of "free", "paid"

### Fact Table
`songplay` - records in log data associated with song plays
- songplay_id (INT) PRIMARY KEY: ID of each user song play
- start_time (TIMESTAMP) NOT NULL: Timestamp of beggining of user activity
- user_id (INT) NOT NULL: ID of user
- level (LEVEL): User level
- song_id (TEXT): ID of Song played
- artist_id (TEXT): ID of Artist of the song played
- session_id (INT): ID of the user Session
- location (TEXT): User location
- user_agent (TEXT): Agent used by user to access Sparkify platform

### Dimension Tables
`users` - users in the app
- user_id (INT) PRIMARY KEY: ID of user
- first_name (TEXT): Name of user
- last_name (TEXT): Last Name of user
- gender (CHAR(1)): Gender of user {M | F}
- level (LEVEL): User level

`songs` - songs in music database
- song_id (TEXT) PRIMARY KEY: ID of Song
- title (TEXT): Title of Song
- artist_id (TEXT): ID of song Artist
- year (INT): Year of song release
- duration (DOUBLE PRECISION): Song duration in milliseconds

`artists` - artists in music database
- artist_id (TEXT): PRIMARY KEY: ID of Artist
- name (TEXT): Name of Artist
- location (TEXT): Name of Artist city
- lattitude (REAL): Lattitude location of artist
- longitude (REAL): Longitude location of artist

`time` - timestamps of records in songplays broken down into specific units for convenience
- start_time (TIMESTAMP): Timestamp of row
- hour (INT): Hour associated to start_time
- day (INT): Day associated to start_time
- week (INT): Week of year associated to start_time
- month (INT): Month associated to start_time
- year (INT): Year associated to start_time
- weekday (INT): Name of week day associated to start_time
