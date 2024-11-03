import pandas as pd
import Database
import statistics
import numpy as np


def addIndicator(country, indicator, value):
    Database.insertSample(country)
    sampleID = Database.getSampleID(country)
    Database.insertIndicatorSampleID(sampleID)
    Database.updateIndicator(sampleID, indicator, value)
    print("Updated: ", sampleID, indicator, value)


#Happiness_index
def collectHappinessIndex():
    df = pd.read_excel('WHR.xls') #2024
    for index, row in df.iterrows():
        # print(row)
        addIndicator(row['Country name'], 'happiness_index', float(round(row['Ladder score'],5)))
# 

def collectOECD(indicator):
    df = pd.read_csv(f'OECD_{indicator}.csv') #2024
    for index, row in df.iterrows():
        print("---------------")
        # print(row)
        print(row["Country"])
        # print(row["OBS_VALUE"])

        # addIndicator(row["Country"], indicator, row["OBS_VALUE"])

def collectOECD2(indicator):
    df = pd.read_csv(f'OECD_well_being.csv') #2024

    for index, row in df.iterrows():
        # print("---------------")
        # print(row)
        country = row["Reference area"]
        measure = row["Measure"]
        if measure == indicator:
            value = row["OBS_VALUE"]
            print(country, value)
            addIndicator(country, "homicides", value)

def collectWB(indicator):
    df = pd.read_csv(f'WB_{indicator}.csv') #2024
    for index, row in df.iterrows():
        print("---------------")
        # print(row)
        # print(row["Country Name"])
        country = row["Country Name"]
        value = str(row["2021"])
        print(country, value)
        if value != 'nan':
            addIndicator(row["Country Name"], indicator, value)
            print("added")

def collectWHO(indicator):
    df = pd.read_csv(f'WHO_{indicator}.csv') #2024
    for index, row in df.iterrows():
        print("---------------")
        year = row["Period"]
        sex = row["Dim1"]
        if year == 2020 and sex == "Both sexes":
            country = row["Location"]
            value = row["FactValueNumeric"]
            print(country, value)

            addIndicator(country, indicator, value)

#Updates median_lyric_sentiment in indicator table
def collectMedianSentiment():
    medianLyricSentiment = {}
    samples = Database.getAllSamples()
    for sampleID, country in samples:
        if not country in medianLyricSentiment:
            medianLyricSentiment[country] = []
        songIDs = Database.getAllSongs(sampleID)
        for songID in songIDs:
            lyric_sentiment = Database.getLyricSentiment(songID)
            if lyric_sentiment is not None:
                medianLyricSentiment[country].append(lyric_sentiment)
    for country in medianLyricSentiment:
        if len(medianLyricSentiment[country]):
            medianLyricSentiment[country] = statistics.median(medianLyricSentiment[country])
            addIndicator(country, "median_lyric_sentiment", medianLyricSentiment[country])
    return medianLyricSentiment

