'''
Sources:
sentiment analysis inspiration: https://www.kaggle.com/code/ekrembayar/f-r-i-e-n-d-s-text-mining-data-visualization
AFINN docs: https://github.com/fnielsen/afinn
sqlite doc: https://www.sqlite.org/
Genius API docs: https://docs.genius.com/
Genius API tutorial: https://www.youtube.com/watch?v=cU8YH2rhN6A
Googletrans doc: https://pypi.org/project/googletrans/

'''

import os
import lyricsgenius
import json
from dotenv import load_dotenv
from pprint import pprint
import sqlite3
from afinn import Afinn
from googletrans import Translator
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time


#API keys
load_dotenv()

#Sentiment Analyzer
afinn = Afinn()

#Lyrics Retrieval
genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')

genius = lyricsgenius.Genius(genius_access_token)

#Music Metadata Retrieval
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')))


#Database
conn = sqlite3.connect('songs.db')

cursor = conn.cursor()

#Translator
translator = Translator()



def drop_tables():
    cursor.execute(
        '''
        DROP TABLE IF EXISTS sample;
        '''
    )
    cursor.execute(
        '''
        DROP TABLE IF EXISTS song;
        '''
    )
    cursor.execute(
        '''
        DROP TABLE IF EXISTS sample_song;
        '''
    )
    cursor.execute(
        '''
        DROP TABLE IF EXISTS indicator_set;
        '''
    )

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



#Translates lyrics string into English
def translateLyrics(lyrics):
    language = translator.detect(lyrics).lang
    print(f"Translator detected lyrics language: {language}")
    if language == "en":
        return lyrics
    englishLyrics = translator.translate(lyrics, dest='en').text
    return englishLyrics

#Adds entire entry to db
def addSong(title, artist, country):
    #check song exists in 'song'
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
    else:
        lyrics = None
        lyric_sentiment = None
        time.sleep(1)
        print(f"Searching Genius for {title} by {artist}...")
        lyrics = genius.search_song(title, artist)

        if lyrics:
            lyrics = str(lyrics.lyrics)
            lyrics.replace("'", "")
            lyrics.replace('"', "")
            lyrics.replace('\0', "")
            try:
                print(f"Translating lyrics...")
                lyrics = translateLyrics(lyrics)
                # lyrics = re.sub(r'[^a-zA-Z0-9\s]', '', lyrics)
                # print(f"Lyrics: {lyrics[:200]}...")
                print(f"Scoring lyric sentiment...")
                lyric_sentiment = afinn.score(lyrics)
            except Exception as e:
                print(e)

        print(f"Sentiment Score: {lyric_sentiment}")
        cursor.execute(
            '''
            INSERT INTO song (title, artist, lyric_sentiment, lyrics)
            VALUES (?, ?, ?, ?)
            ''', (title, artist, lyric_sentiment, lyrics)
        )
        songID = cursor.lastrowid

    cursor.execute(
        '''
        SELECT sampleID FROM sample
        WHERE country = ?
        ''', (country,)
    )
    sampleID = cursor.fetchone()
    if sampleID is None:
        cursor.execute(
            '''
            INSERT INTO sample (country)
            VALUES (?, ?)
            ''', (country)
        )
        sampleID = cursor.lastrowid
    else:
        sampleID = sampleID[0]

    cursor.execute(
        '''
        INSERT OR IGNORE INTO sample_song
        VALUES (?, ?)
        ''', (sampleID, songID)
    )
    conn.commit()


def addIndicator(country, indicator, value):
    cursor.execute(
        '''
        SELECT sampleID from sample
        WHERE country = ?
        ''', (country,)
    )
    sampleID = cursor.fetchone()
    if sampleID is None:
        cursor.execute(
            '''
            INSERT INTO sample (country)
            VALUES (?)
            ''', (country,)
        )
        sampleID = cursor.lastrowid
    else:
        sampleID = sampleID[0]
    print(sampleID)
    cursor.execute(
        f'''
        SELECT sampleID
        FROM indicator_set
        WHERE sampleID = ?;
        ''', (sampleID,)
    )
    existingSample = cursor.fetchall()
    if existingSample is None or not len(existingSample):
        cursor.execute(
            f'''
            INSERT INTO indicator_set (sampleID, {indicator}) VALUES (?, ?);
            ''', (sampleID, value)
        )
        print("Inserting: ", indicator, value, sampleID)
        print(cursor.rowcount)
    else:
        cursor.execute(
            f'''
            UPDATE indicator_set
            SET {indicator} = ?
            WHERE sampleID = ?;
            ''', (value, sampleID)
        )
        print(indicator, value, sampleID)
        print(cursor.rowcount)
    conn.commit()
def getSpotifySongs():
    #Build samples
    #For each country, get the top 50 songs
    top50 = {
        "Finland": "37i9dQZEVXbMxcczTSoGwZ",
        "Australia": "37i9dQZEVXbJPcfkRz0wJ0",
        "United Kingdom": "37i9dQZEVXbLnolsZ8PSNw",
        "Singapore": "37i9dQZEVXbK4gjvS1FjPY",
        "Malta": "1wDofcZqDg1mZcB1fsgyRJ",
        "Cyprus": "1NNauN205jiVeH2ixReshi",
        "China": "3qwyQJzNAt4BDfnijpKkbi",
        "Mauritius": "1zzPjTFXgEHqHlVByDJbio",
        "Indonesia": "37i9dQZEVXbObFQZ3JLcXt",
        "Mozambique": "3NNGZJegNwvQicqWqMoe80",
        "Iran": "6xU0Vcp5xKCEdBLEe9meYB",
        "Burkina Faso": "5vS9YRoXoMTNvmoI0OXqo3",
        "Ghana": "4t5QcqXgA5gmtomjxt774E",
        "Ethiopia": "7dM4QqLCVFDWKNHlOtI1fB",
        "Sierra Leone": "7DfKFjIairBxWXQJGbkYVe",

        "Israel": "37i9dQZEVXbJ6IpvItkve3",
        "Canada": "37i9dQZEVXbKj23U1GF4IR",
        "United States": "37i9dQZEVXbLRQDuF5jeBp",
        "Mexico": "37i9dQZEVXbO3qyFxbkOE1",
        "Poland": "37i9dQZEVXbN6itCcaL3Tt",
        "Slovakia": "37i9dQZEVXbKIVTPX9a2Sb",
        "Portugal": "37i9dQZEVXbKyJS56d1pgi",
        "Bosnia and Herzegovina": "7fFD8oaaun0RYN9kebQ5sF",
        "Kyrgyzstan": "7r1eHVwCqHvKUSGQb15BjX",
        "Algeria": "4eSH1o9RQqnbN8ZX7CIVUI",
        "Gabon": "3jDALIM1pSL9yfj8yKDWzR",
        "Ukraine": "37i9dQZEVXbKkidEfWYRuD",
        "Tunisia": "1rfwanToJd9SOVoT1WAJNY",
        "India": "37i9dQZEVXbLZ52XmnySJg",
        "Eswatini": "1Lrz87gcrKq8CigqG0Exy8",
    }

    songs = {}
    for country in list(top50.keys()):
        songs[country] = []
        playlist = sp.playlist_tracks(top50[country])
        for item in playlist['items']:
            track = item['track']
            songs[country].append(track)
    songs = json.loads(json.dumps(songs, indent=4))
    with open('SpotifyIndex.json', 'w') as f:
        json.dump(songs, f, indent=4)
    return songs

