### Description : Hosting the file for streamlit

### Importing libraries

#### WebScraping
from lyricsgenius import Genius

### NLP and Data Manipulation
import pandas as pd
from textblob import TextBlob as tb
import nltk
nltk.download('stopwords')
import string
import re


### Hosting
import streamlit as st

#### Titling and Subtitling

st.title("""
Explicit Song lyrics analysis
""")
st.text("""Made by Rohit Venkatesan & Mikhail Martins""")
st.subheader("This Application will analyze the song lyrics and give the user a recommendation.")
st.text("""
The User who shall use this application shall not depend on the results completely
""")
st.text("""(Use this application only for a second opinion recommendation)""")

artist_name = st.text_input('Enter the Artist Name: ')
song_name = st.text_input('Enter the Song Name: ')


## Stopwords/Words Corpus
nltk.download('stopwords')
from nltk.corpus import stopwords
e_words = ['fuck', 'asshole', 'shit', 'dick', 'dickhead', 'pussy', 'sex','sexy','role-play','roleplay', 'bitch', 'cunt'
        ,'bloody', 'bugger', 'bastard', 'motherfucker', 'shag', 'wanker', 'wank', 'bollocks',
        'whores', 'ass', 'weed', 'smoker','fucking','smoking', 'twat', 'twit', 'hoe', 'wet-ass', 'badass',
        'piss', 'bollocks', 'cocksucker', 'effing', 'nigga', 'twat', 'fatherfucker', 'babe', 'pussysweat', 'creampie', 'cum', 'cumshot', 'facial',
        'stripper', 'twerking', 'bootyshake', 'booty', 'bootyhole', 'asshole', 'fatass', 'phatass', 'anal', 'hentai']

text_file = open("stopwords.txt", 'r+')
stopwords = text_file.read()


### Tokenization
### Defining a class which holds all the files

class Tokens:
    
    def __init__(self, lyrics):
        self.lyrics = lyrics
    
    def tokenize_1(self):
        ### Tokenization 1
        ly_1 = self.lower()
        ly_2 = re.sub('\W+', " ", ly_1)
        ly_3 = ly_2.split()
        
        ### Explicit Word Extraction
        explicit_commons = [word for word in ly_3 if word in e_words]
        explicit_freq = nltk.FreqDist(explicit_commons).most_common(10)
        
        ### Result Consolidation
        result_1 = pd.DataFrame(explicit_freq, columns = ['Words', 'Count'])
        return explicit_commons, result_1
    
    def tokenize_2(self):
        ### For Normal Words
        ### Tokenization 2
        ly_1 = self.lower()
        ly_2 = re.sub('\W+', " ", ly_1)
        ly_3 = ly_2.split()
        
        ## Removing Explicit and Stopwords from the lyrics
        explicit_removal = [word for word in ly_3 if word not in e_words]
        all_words_clean = [word for word in explicit_removal if word not in stopwords]
        clean_words_freq = nltk.FreqDist(all_words_clean).most_common(10)
        
        ### Result Consolidation
        result_2 = pd.DataFrame(clean_words_freq, columns = ['Words', 'Count'])
        return all_words_clean, result_2
    
    ### Sentiment Analysis

class Subject:
    
    def __init__(self, lyrics, score):
        self.lyrics = lyrics
        self.score = score
        
    def Subjectivity(self):
        return tb(self).sentiment.subjectivity

    def Polarity(self):
        return tb(self).sentiment.polarity



@st.cache
def main(artist_name, song_name):
    # Authentication
    genius_api_token = "tC9lC6GkylkaHjPKzt2TwaEa_TttWFLaGfq0CKcTq5J59Ghj3DWY-e1-ufbWHOC2"
    base_url = "https://api.genius.com"

    genius = Genius(genius_api_token, skip_non_songs=True, excluded_terms=["(Remix)", "(Live)"], remove_section_headers=True)

    artist = genius.search_artist(artist_name, max_songs = 1)
    song = artist.song(song_name)

    ## Downloading Lyrics
    lyrics = song.lyrics
    
    ## Running NLP

    explicit_commons, result_1 = Tokens.tokenize_1(lyrics)
    all_words_clean, result_2 = Tokens.tokenize_2(lyrics)
    subjectivity = Subject.Subjectivity(lyrics)
    polarity = Subject.Polarity(lyrics)

    return explicit_commons, result_1, result_2, subjectivity, polarity

if st.button('Submit'):
    explicit_commons, result_1, result_2, subjectivity, polarity = main(artist_name, song_name)

    if len(explicit_commons) > 0:
        st.subheader('Explicit and Most Common Words')
        st.text('This Song contains explicit words which are not suitable for younger audiences')
        st.text('The total number of unique explicit words found in the song are: {}'.format(len(result_1)))
    else:
        st.text('There are no Explicit Words')
    
    st.text('')
    st.text('10 most common words used are as follows: ')
    st.dataframe(result_2)

    st.text('')
    st.subheader('Subjectivity')
    st.text('Value: {}%'.format(round(subjectivity * 100),3))
    st.text('A value closer to 0 would mean the song is written in an objective tone(range : 0% to 100%)')

    st.subheader('Polarity')
    st.text('Value: {}%'.format(round(polarity * 100),2))
    st.text('Polarity is whether the lyrics have a positive or a negative sentiment(range : -100% to +100%).')
    
    st.subheader('Polarity Verdict: ')
    if polarity > 0:
        st.text('Verdict: Positive')
    elif polarity < 0 :
        st.text('Verdict: Negative')
    else:
        st.text('Verdict: Neutral')

    st.text('')
    st.subheader('Recommendation')
    if len(explicit_commons) > 0:
        st.text('Since there are explicit words in the song it is not recommeded for children')
        st.text('Explicit Words in the song: ')
        st.dataframe(result_1)
    else:
        st.text('This song can be introduced to children.')
        st.text('Note: It is highly recommended that you should listen to the song first and make your own decision.')

            






