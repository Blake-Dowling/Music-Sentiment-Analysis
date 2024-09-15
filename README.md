The goal of this application is to analyze the sentiment of lyrics across various musical genres. 
The Genius API does not allow selection of random songs by genre, nor is there a genre attribute in the retrieved object.

Available attributes: 
Genius can only be used for lyrics, basically. Tried artist and song objects, and only release date, atrist, lyrics.
We should get attributes such as country, genre, etc from another source and add to our db.


Questions for group:
What trends do we want to analyze?
Sentiment of single over time? Sentiment of all genres over time? Cluster artists (all genres) by sentiment? Judge artists by user comment/rating sentiment? Cluster sentiment by country?
How do we get a representative population of a genre?
How should we combine multiple lexicons?