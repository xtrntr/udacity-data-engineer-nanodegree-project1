import os
import glob
import psycopg2
import pandas as pd
import datetime
from sql_queries import *

def process_song_file(cur, filepath):
    """
    Inputs: database cursor, filepath

    The filepath is assumed to point to a songfile otherwise it will fail.
    It extracts both song and artist information to store into the songs and artists table respectively.
    """

    # open song file
    song_df = pd.read_json(filepath, lines=True)

    # insert song record
    song_data = list(song_df[['song_id', 'title', 'artist_id', 'year', 'duration']].values[0])
    cur.execute(song_table_insert, song_data)

    # insert artist record
    artist_data = list(song_df[['artist_id', 'artist_name', 'artist_location', 'artist_latitude', 'artist_longitude']].values[0])
    cur.execute(artist_table_insert, artist_data)

def process_log_file(cur, filepath):
    """
    Inputs: database cursor, filepath

    The filepath is assumed to point to a logfile otherwise it will fail.
    Only rows with the column `page` == "NextSong" are processed.
    It extracts time information from the column `ts` to store into time table.
    It extracts user information to store into the user table.
    It extracts songplay information by joining the song and artist table and extracting some other rows from the logfile.
    """

    # open log file
    df = pd.read_json(filepath, lines=True)

    # filter by NextSong action
    df = df[df.page == "NextSong"]

    # convert timestamp column to datetime
    df["ts"] = df["ts"].apply(lambda x : datetime.datetime.fromtimestamp(x/1000.0))

    # insert time data records
    time_data = [df["ts"].dt, df["ts"].dt.hour, df["ts"].dt.day, df["ts"].dt.weekofyear,
                 df["ts"].dt.month, df["ts"].dt.year, df["ts"].dt.weekday]
    time_df = pd.DataFrame({"start_time": df["ts"],
                            "hour": df["ts"].dt.hour,
                            "day": df["ts"].dt.day,
                            "week": df["ts"].dt.weekofyear,
                            "month": df["ts"].dt.month,
                            "year": df["ts"].dt.year,
                            "weekday": df["ts"].dt.weekday})

    for i, row in time_df.iterrows():
        cur.execute(time_table_insert, list(row))

    # load user table
    user_df = pd.DataFrame({"user_id": df["userId"],
                            "first_name": df["firstName"],
                            "last_name": df["ts"],
                            "gender": df["gender"],
                            "level": df["level"]})

    # insert user records
    for i, row in user_df.iterrows():
        cur.execute(user_table_insert, row)

    # insert songplay records
    for index, row in df.iterrows():

        # get songid and artistid from song and artist tables
        results = cur.execute(song_select, (row.song, row.artist, row.length))
        songid, artistid = results if results else None, None

        if songid or artistid:
            print(songid, artistid)
        # insert songplay record
        songplay_data = (row.ts, row.userId, row.level, songid,
                         artistid, row.sessionId, row.location, row.userAgent)
        cur.execute(songplay_table_insert, songplay_data)


def process_data(cur, conn, filepath, func):
    """
    Inputs: database cursor, postgres, directory filepath, python function
    python function must have a function signature similar to `process_log_file`, `process_song_file`

    given a directory of files, recursively walk through all folders and collect the filenames in a list
    apply the given function on all the collected filenames after.
    """

    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()
