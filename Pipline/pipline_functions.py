import pandas as pd
import numpy as np
from textblob import TextBlob
from rotten_tomatoes_client import RottenTomatoesClient
import multiprocessing as mp

class Pipline:
    def __init__(self):
        pass
    def check(self, movie_genre):
        ''' The function checks whether the  '''
        genres = ['action', 'animation', 'comedy', 'drama', 'horror', 'sci-fi']
        for genre in genres:
            if genre in movie_genre.lower():
                return genre

    def sentiment(self, description):
        ''' The function takes the description of the movie and returns: polarity and subjectivity scores. '''
        bolb = TextBlob(str(description))
        return bolb

    def rotten_tomatoes(self, title):
        try: # This exception handling is essential for the cases where the title is not found.
            result = RottenTomatoesClient.search(term=title, limit=1)['movies'][0]['meterScore']
            return result
        except:
            result = 'NaN'

    def filter_data(self, data):
        ''' Selects only the movies realesed >= 2016 in the US. It also selects only mature movies.'''
        
        data = data[(data.type == 'Movie') & # select only Movies.
                    (data.country == 'United States') & 
                    data.rating.apply(lambda x: x in ['R', 'NC-17', 'TV-MA'])].dropna() # selects only mature films.
        
        return data

    def create_features(self, data):
        ''' Creates features of the length of description, title, movie duration and gener of the movie. '''
        
        data['description_len'] = data.description.apply(lambda x: len(x)) # adding a column with the lenght of the description
        data['title_len'] = data.title.apply(lambda x: len(x)) # adding a column with the length of the title
        data['mv_dur'] = data.duration.apply(lambda x: int(x.split()[0])) # adding a column with the movie duration
        data['genre'] = data.listed_in.apply(lambda x: self.check(x)) # adding a column with the movie duration
        
        return data

    def semantic_analyisis(self, data, text_column):
        '''Calculates polarity and subjectvity scores of a given text.'''
        
        data['polarity'] = data[text_column].apply(lambda x: self.sentiment(x).polarity) # adding a column with the polarity scores
        data['subjectivity'] = data[text_column].apply(lambda x: self.sentiment(x).subjectivity) # adding a column with the polarity scores
        
        return data

    def add_reviews(self, data):
        data['rotten_score'] = data.title.apply(lambda x: self.rotten_tomatoes(x))

        data.drop(['director', 'type', 'cast', 'country', 'date_added',
                    'rating', 'duration', 'listed_in'],
                axis=1, inplace = True)
        data = data[data.notna()] # # removing all the None entries (ONLY for this demo purposes. :))
        data.dropna(inplace=True)

        return data


    def pipline(self, data):

        d1 = self.filter_data(data)
        d2 = self.create_features(d1)
        d3 = self.semantic_analyisis(d2, 'title')
        d4 = self.add_reviews(d3)

        return d4

