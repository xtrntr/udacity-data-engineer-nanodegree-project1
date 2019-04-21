# PREREQUISITES

level_type_create = ("""
do $$ begin
    create type level as ENUM ('free', 'paid');
exception
    when duplicate_object then null;
end $$;
""")

# CREATE TABLES

songplay_table_create = ("""
create table if not exists songplays (
songplay_id serial primary key,
start_time timestamp,
user_id integer,
level level,
song_id text,
artist_id text,
session_id integer,
location text,
user_agent text
);
""")

user_table_create = ("""
create table if not exists users (
user_id integer,
first_name text,
last_name text,
gender char(1),
level level
);
""")

song_table_create = ("""
create table if not exists songs (
song_id text,
title text,
artist_id text,
year integer,
duration double precision
);
""")

artist_table_create = ("""
create table if not exists artists (
artist_id text,
name text,
location text,
lattitude real,
longitude real
);
""")

time_table_create = ("""
create table if not exists time (
start_time timestamp,
hour integer,
day integer,
week integer,
month integer,
year integer,
weekday integer
);
""")

# INSERT RECORDS

songplay_table_insert = ("""
insert into songplays (start_time, user_id, level, song_id,
                       artist_id, session_id, location, user_agent)
                       values (%s, %s, %s, %s, %s, %s, %s, %s)
""")

user_table_insert = ("""
insert into users (user_id, first_name, last_name, gender, level) values (%s, %s, %s, %s, %s)
""")

song_table_insert = ("""
insert into songs (song_id, title, artist_id, year, duration) values (%s, %s, %s, %s, %s)
""")

artist_table_insert = ("""
insert into artists (artist_id, name, location, lattitude, longitude) values (%s, %s, %s, %s, %s)
""")

time_table_insert = ("""
insert into time (start_time, hour, day, week, month, year, weekday) values (%s, %s, %s, %s, %s, %s, %s)
""")

# FIND SONGS

song_select = ("""
select songs.song_id, artists.artist_id from
(songs join artists on songs.artist_id=artists.artist_id)
where songs.song_id=%s and artists.name=%s and songs.duration=%s;
""")

# QUERY LISTS

setup_queries = [level_type_create]
create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
