Overview:
The goal of this application is to analyze the sentiment of musical lyrics across various musical genres, locations, and times. 

Goals:
Plot popularity of genres by country over time.
Plot sentiment of genres by country over time.
Compare audience reviews with sentiment.
Cluster genres by sentiment.
Cluster countries by sentiment.
Compare different sentiment analysis lexicons and algorithms.

Current Questions:
How to visualize data?
Are there more trends do we want to analyze?
How to get a representative sample?

Obstacles:
The Genius API does not allow selection of random songs by genre, nor is there a genre attribute in the retrieved object. Therefore, artist, title, country, genre, and date will be retrieved from MetaCritic, while Genius will supply the lyrics. Finally, the lyrics are analyzed with AFINN lexicon (and possibly other methods).