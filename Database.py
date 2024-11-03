import sqlite3
import numpy as np
import pandas as pd
#Database
conn = sqlite3.connect('songs.db')

cursor = conn.cursor()

def create_tables():
    #sample
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS sample (
            sampleID INTEGER PRIMARY KEY AUTOINCREMENT,
            country TEXT NOT NULL,
            UNIQUE(sampleID, country)
        );
        '''
    )
    #indicator_set
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS indicator_set (
            sampleID INTEGER UNIQUE,
            happiness_index REAL,
            life_satisfaction REAL,
            unemployment_rate REAL,
            suicide_mortality_rate REAL,
            FOREIGN KEY (sampleID) REFERENCES sample (sampleID) ON UPDATE CASCADE ON DELETE CASCADE
        );
        '''
    )
    #song
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS song (
            songID INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            artist TEXT NOT NULL,
            lyric_sentiment REAL,
            lyrics TEXT,
            UNIQUE(title, artist)
        );
        '''
    )
    #sample_song
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS sample_song (
            sampleID INTEGER, 
            songID INTEGER, 
            FOREIGN KEY (sampleID) REFERENCES sample (sampleID) ON UPDATE CASCADE ON DELETE CASCADE,
            FOREIGN KEY (songID) REFERENCES song (songID) ON UPDATE CASCADE ON DELETE CASCADE,
            PRIMARY KEY(sampleID, songID)
        );
        '''
    )
    conn.commit()

def getSongID(title, artist):
    cursor.execute(
        '''
        SELECT songID FROM song
        WHERE title = ? and artist = ?
        ''', (title, artist)
    )
    songID = cursor.fetchone()
    if songID is not None:
        print("Song already stored.")
        songID = songID[0]
    return songID
def insertSong(title, artist, lyric_sentiment, lyrics):
    cursor.execute(
        '''
        INSERT OR IGNORE INTO song (title, artist, lyric_sentiment, lyrics)
        VALUES (?, ?, ?, ?)
        ''', (title, artist, lyric_sentiment, lyrics)
    )
    conn.commit()
    return cursor.lastrowid
def insertSample(country):
    cursor.execute(
        '''
        INSERT OR IGNORE INTO sample (country)
        VALUES (?)
        ''', (country,)
    )
    conn.commit()
def getAllSamples():
    cursor.execute(
        '''
        SELECT sampleID, country FROM sample;
        '''
    )
    return cursor.fetchall()
def getSampleID(country):
    cursor.execute(
        '''
        SELECT sampleID FROM sample
        WHERE country = ?
        ''', (country,)
    )
    sampleID = cursor.fetchone()
    if sampleID is not None:
        sampleID = sampleID[0]
    return sampleID
def insertSampleSong(sampleID, songID):
    cursor.execute(
        '''
        INSERT OR IGNORE INTO sample_song
        VALUES (?, ?)
        ''', (sampleID, songID)
    )
    conn.commit()
def getAllSongs(sampleID):
    cursor.execute(
        '''
        SELECT songID FROM sample_song
        WHERE sampleID = ?
        ''', (sampleID,)
    )
    return cursor.fetchall()
def getLyricSentiment(songID):
    cursor.execute(
        '''
        SELECT lyric_sentiment FROM song
        WHERE songID = ?;
        ''', (songID)
    )
    lyric_sentiment = cursor.fetchone()
    if lyric_sentiment is not None:
        lyric_sentiment = lyric_sentiment[0]
    return lyric_sentiment
def insertIndicatorSampleID(sampleID):
    cursor.execute(
        f'''
        INSERT OR IGNORE INTO indicator_set (sampleID) 
        VALUES (?);
        ''', (sampleID,)
    )
    conn.commit()
def updateIndicator(sampleID, indicator, value):
    if indicator not in getIndicators():
        cursor.execute(
            f'''
            ALTER TABLE indicator_set
            ADD COLUMN {indicator} REAL;
            '''
        )
        conn.commit()
    cursor.execute(
        f'''
        UPDATE indicator_set
        SET {indicator} =  ?
        WHERE sampleID = ?;
        ''', (value, sampleID)
    )
    conn.commit()
    print("added ", sampleID, value)

def getIndicators():
    cursor.execute(
        '''
            PRAGMA table_info(indicator_set);
        '''
    )
    columns = cursor.fetchall()
    columns = np.array(columns)[1:,1]
    return columns

def getIndicatorDF():
    query = '''
            SELECT *
            FROM sample
            JOIN indicator_set
            USING (sampleID);
            '''
    return pd.read_sql_query(query, conn)