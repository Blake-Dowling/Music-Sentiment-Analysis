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

from afinn import Afinn
from googletrans import Translator
import re
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import time

import Database

#API keys
load_dotenv()

#Sentiment Analyzer
afinn = Afinn()

#Lyrics Retrieval
genius_access_token = os.getenv('GENIUS_ACCESS_TOKEN')
genius = lyricsgenius.Genius(genius_access_token)

#Music Metadata Retrieval
sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=os.getenv('SPOTIFY_CLIENT_ID'), client_secret=os.getenv('SPOTIFY_CLIENT_SECRET')))

#Translator
translator = Translator()

#Translates lyrics string into English
def translateLyrics(lyrics):
    language = translator.detect(lyrics).lang
    print(f"Translator detected lyrics language: {language}")
    if language == "en":
        return lyrics
    englishLyrics = translator.translate(lyrics, dest='en').text
    return englishLyrics

#Adds song entry (songID, title, artist, lyric_sentiment, lyrics)
#and connects to sample for given country
def addSong(title, artist, country):
    #check song exists in 'song'
    songID = Database.getSongID(title, artist)
    if songID is not None:
        print("Song already stored.")
    #Get song lyrics
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
        songID = Database.insertSong(title, artist, lyric_sentiment, lyrics)

    Database.insertSample(country)
    sampleID = Database.getSampleID(country)
    Database.insertSampleSong(sampleID, songID)

def getSpotifySongs():
    #Build samples
    #For each country, get the top 50 songs
    top50PlaylistHashes = {
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
    for country in list(top50PlaylistHashes.keys()):
        songs[country] = []
        playlist = sp.playlist_tracks(top50PlaylistHashes[country])
        for item in playlist['items']:
            track = item['track']
            songs[country].append(track)
    songs = json.loads(json.dumps(songs, indent=4))
    with open('SpotifyIndex.json', 'w') as f:
        json.dump(songs, f, indent=4)
    return songs

def addSpotifySongs():
    songs = {}
    with open("SpotifyIndex.json", 'r') as f:
        songs = json.load(f)

    for country in list(songs.keys())[:]:
        print(country)
        for i in range(len(songs[country])):
            song = songs[country][i]
            print(f"{country}: song {i+1}/{len(songs[country])}: ", song["name"], song["artists"][0]["name"], song["album"]["release_date"][:4])
            if song["album"]["release_date"][:4] == '2024':
                addSong(song["name"], song["artists"][0]["name"], country)
            else:
                print(f"Release Date {song["album"]["release_date"][:4]}. Skipping sample.")