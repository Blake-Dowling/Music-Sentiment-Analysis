# Lyric Sentiment as an Emotional Health Indicator

## Objective:
- The goal of this application is to attempt to find a correlation between sentiment of musical lyrics and emotional health indicators. 
- Methods such as principle component analysis, clustering, association analysis, anomaly detection, time series analysis, and regression will be used to attempt to find such correlations across different locations and times.

## Data Collection:
- Lyrics: Top 100 songs for each selected country and year using MusicBrainz, Spotify, Genius
- Sentiment Scoring: Googletrans, AFINN, NRC, etc.
- Emotional Health Data: World Bank, OECD, UNODC, World Happiness Report, WHO

## Related Papers:
- Parent–Child Connectedness and Behavioral and Emotional Health Among Adolescents
https://www.sciencedirect.com/science/article/abs/pii/S074937970500365X

- The Language of Lyrics: An Analysis of Popular Billboard Songs Across Conditions of Social and Economic Threat
https://journals.sagepub.com/doi/abs/10.1177/0261927x09335259

- Towards Estimating Personal Values in Song Lyrics
https://arxiv.org/abs/2408.12694

- Genre of Music and Lyrical Content: Expectation Effects
https://www.tandfonline.com/doi/abs/10.1080/00221329909595560

- Sentiment Analysis of FRIENDS
https://www.kaggle.com/code/ekrembayar/f-r-i-e-n-d-s-text-mining-data-visualization

Goals:
Plot sentiment of genres by country over time.
Compare audience reviews with sentiment.
Cluster genres by sentiment.
Cluster countries by sentiment.
Compare different sentiment analysis lexicons and algorithms.
Plot popularity of genres by country over time.
Calculate how representative our sample is, and what would be needed for a representative sample. I.e. more indexes besides top 100. May involve scaling the algorithm to be applied to smaller populations instead, or using spotify user data to find what people are really listening to.

Current Questions:
How to visualize data?
Are there more trends do we want to analyze?
How to get a representative sample?

Obstacles:
- The Genius API does not allow selection of random songs by genre, nor is there a genre attribute in the retrieved object. Therefore, artist, title, country, genre, and date will be retrieved from MetaCritic, while Genius will supply the lyrics. Finally, the lyrics are analyzed with AFINN lexicon (and possibly other methods).
- Analyzing lyrics in different languages requires different lexicons or translated lyrics, which may cause score discrepancies. We decided to translate lyrics into english in order to have a controlled lexicon, which was also simpler due to having to detect the language using a translator, regardless.
- Acquiring representative samples (varying musical diversity)
- Combining numerous APIs
- Preserving sentiment with translation
- Data cleaning and accurate writing system code point representation
- Limitations of lexicons (excluded vernacular)


notes:
Spotify indexes lack randomness required for representativeness.
Popular songs overlap across countries and many are American songs, possibly due to Spotify 
being US company. Music is also pretty globalized.
Malta is all Christmas songs
Freedom of speech / censorship may influence popular music lyrics.