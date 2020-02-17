import numpy as np
import pandas as pd
from datetime import datetime
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from FuzzyController.system import set_up_system

class MovieController:
    def __init__(self):
        
        self.data = pd.read_csv('Data/clean_data.csv', index_col=[0]).reset_index(drop=True) # Read in the movies data set
        self.netflix_ctrl = set_up_system()
        
    def create_sim_instance(self, name):
        self.name = ctrl.ControlSystemSimulation(self.netflix_ctrl) # Create a simulation instance
    
    def calculate(self, mood, physical_state):
        self.movie_set = {'Title' : [], 'Description' : [], 'Duration (minutes)' : [], 'Rotten_Scores' : [], 'Scores' : []}
        for index in range(len(self.data)):
            try:
                self.name.input['Mood'] = mood
                self.name.input['Physcial State'] = physical_state
                self.name.input['Year'] = self.data.release_year.iloc[index]
                self.name.input['Description Length'] = int(self.data.description_len.iloc[index])
                self.name.input['Movie Length'] = int(self.data.mv_dur.iloc[index])
                self.name.input['Polarity'] = int(self.data.polarity.iloc[index])
                self.name.input['Subjectivity'] = int(self.data.subjectivity.iloc[index])
                self.name.input['Reviews'] = int(self.data.rotten_score.iloc[index])
                self.name.input['Time of The Day'] = datetime.now().hour
                
                self.name.compute()
                self.movie_set['Title'].append(self.data.title.iloc[index])
                self.movie_set['Description'].append(self.data.description.iloc[index])
                self.movie_set['Duration (minutes)'].append(self.data.mv_dur.iloc[index])
                self.movie_set['Rotten_Scores'].append(self.data.rotten_score.iloc[index])
                self.movie_set['Scores'].append(self.name.output['Recommendation Score'])


            except: # This is necessary for cases where a given movie does not activate any of the rules in the rule base.
                pass
    
    def results(self):
        res = pd.DataFrame.from_dict(self.movie_set)
        first = res.sort_values(by=['Scores', 'Rotten_Scores'], ascending=[False, False])[0:5] # Sorts by the Recommendation score and then by the Rotten Score. And selects the first 5.
        return first

