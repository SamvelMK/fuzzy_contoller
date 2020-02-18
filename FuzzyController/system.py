
import numpy as np
import pandas as pd
import skfuzzy as fuzz
from skfuzzy import control as ctrl
from datetime import datetime

# Function to set up the Fuzzy System: 
def set_up_system():
    # Defining the Universe of Discourse of Each Linguistic Variable.
    # Movie Characteristics
    release_year = ctrl.Antecedent(np.arange(1967, 2021, 1), 'Year')
    title_len = ctrl.Antecedent(np.arange(3, 49, 1), 'Title Length')
    desc_len = ctrl.Antecedent(np.arange(120, 161, 1), 'Description Length')
    duration = ctrl.Antecedent(np.arange(53, 210, 1), 'Movie Length')
    polarity = ctrl.Antecedent(np.arange(-1, 1, 0.0001), 'Polarity')
    subjectivity = ctrl.Antecedent(np.arange(53, 209, 1), 'Subjectivity')
    reviews = ctrl.Antecedent(np.arange(0, 100, 1), 'Reviews')

    # Internal State of the user
    mood = ctrl.Antecedent(np.arange(0, 11, 0.1), 'Mood')
    physical_state = ctrl.Antecedent(np.arange(0, 11, 0.1), 'Physcial State')
    time = ctrl.Antecedent(np.arange(0, 25, 1), 'Time of The Day')

    # Automatically generated Triangular membership functions for a set of antecedents.

    release_year.automf(5, names=['Very Old', 'Old', 'Not So Old', 
                                    'New', 'Very New'])
    title_len.automf(5, names=['Very Short', 'Short', 'Not So Short',
                                'Long', 'Very Long'])
    desc_len.automf(5, names=['Very Short', 'Short', 'Not So Short',
                                'Long', 'Very Long'])
    polarity.automf(5, names=['Very Negative', 'Negative', 'Not So Negative', 
                                'Positive', 'Very Positive'])
    subjectivity.automf(5, names=['Very Subjective', 'Subjective', 'Not So Subjective', 
                                'Objective/Factual', 'Very Objective/Factual'])
    time.automf(5, names=['Very Early', 'Early', 'Not So Early', 
                            'Late', 'Very Late'])
    reviews.automf(3, names=['Poor', 'Average', 'Good'])

    ### User State
    mood.automf(5, names=['Very Upset', 'Upset', 'Neutral', 
                            'Happy', 'Very Happy'])
    physical_state.automf(5, names=['Exhausted', 'Tired', 
                                        'Not So Tired', 'Lively', 'Very Lively'])

    # Manually generated gaussian membership functions for the Linguistic Variable 'Movie Duration' (For demo purposes).

    duration['Very Short'] = fuzz.gaussmf(duration.universe, 53, 15)
    duration['Short'] = fuzz.gaussmf(duration.universe, 93, 15)
    duration['Not So Short'] = fuzz.gaussmf(duration.universe, 133, 15)
    duration['Long'] = fuzz.gaussmf(duration.universe, 173, 15)
    duration['Very Long'] = fuzz.gaussmf(duration.universe, 200, 15)

    ### Defining the Consequent
    recommend = ctrl.Consequent(np.arange(0, 1.1, 0.1), 'Recommendation Score')
    
    # Define the membership function of the consequent. For this I chose a sigmoid membership function. 
    recommend['Recommend'] = fuzz.smf(recommend.universe, 0, 1)
    
    rule_1 = ctrl.Rule(mood['Very Happy'] & physical_state['Very Lively'] & (reviews['Average'] | release_year['New'] |
                                release_year['Very New']), recommend['Recommend'])

    rule_2 = ctrl.Rule(mood['Very Happy'] & physical_state['Lively'] & (reviews['Average'] | release_year['New']), 
                                recommend['Recommend'])

    rule_3 = ctrl.Rule(mood['Very Happy'] & physical_state['Not So Tired'] & (reviews['Good'] | release_year['New']) &
                                    duration['Not So Short'], recommend['Recommend'])

    rule_4 = ctrl.Rule(mood['Very Happy'] & physical_state['Tired'] & (reviews['Good'] | release_year['New']) & duration['Short'] &
                                subjectivity['Subjective'] & polarity['Not So Negative'], recommend['Recommend']) # I become super picky when i'm tired so I need to make sure that the content of the 
                                                                                                                    # movie is not too negative and it's not full of factual data (less analysis on my part 
                                                                                                                    # when I watch a movie).
                                                                                                                    
    rule_5 = ctrl.Rule(mood['Very Happy'] & physical_state['Exhausted'] & (reviews['Good'] | release_year['New']) & duration['Very Short'] & 
                            (subjectivity['Subjective'] | subjectivity['Very Subjective']) & polarity['Not So Negative'] & (desc_len['Short'] | 
                                desc_len['Very Short']), recommend['Recommend'])

    rule_6 = ctrl.Rule(mood['Happy'] & physical_state['Very Lively'] & (reviews['Good'] | release_year['Not So Old']),
                            recommend['Recommend'])

    rule_7 = ctrl.Rule(mood['Happy'] & (physical_state['Very Lively'] | physical_state['Lively']) & (reviews['Average'] |
                                release_year['Not So Old']), recommend['Recommend'])

    rule_8 = ctrl.Rule(mood['Happy'] & physical_state['Not So Tired'] & (reviews['Average'] | release_year['Not So Old'] |
                        release_year['New']), recommend['Recommend'])

    rule_9 = ctrl.Rule(mood['Happy'] & physical_state['Tired'] & reviews['Good'] & (release_year['Not So Old'] |
                        release_year['New']) & polarity['Not So Negative'] & duration['Short'], recommend['Recommend'])

    rule_10 = ctrl.Rule(mood['Happy'] & physical_state['Exhausted'] & reviews['Good'] & release_year['Not So Old']
                        & polarity['Very Positive'] & (duration['Short'] | duration['Very Short']), recommend['Recommend'])

    rule_11 = ctrl.Rule(mood['Neutral'] & (physical_state['Very Lively'] | physical_state['Lively'] | physical_state['Not So Tired']) &
                        (reviews['Average'] | reviews['Good']) & (release_year['Not So Old'] | release_year['New'] | release_year['Very New']) 
                        & (duration['Not So Short'] | duration['Short']) & (time['Early'] | time['Not So Early']), recommend['Recommend'])

    rule_12 = ctrl.Rule(mood['Neutral'] & physical_state['Tired'] & reviews['Good']
                        & (release_year['Not So Old'] | release_year['New']) & duration['Short'] & (time['Early'] | time['Not So Early'])
                        , recommend['Recommend'])

    rule_13 = ctrl.Rule(mood['Neutral'] & physical_state['Exhausted'] & reviews['Good']
                        & (release_year['Not So Old'] | release_year['New']) & duration['Very Short'] & (time['Early'] | time['Not So Early'])
                        , recommend['Recommend'])

    rule_14 = ctrl.Rule(mood['Upset'] & (physical_state['Very Lively'] | physical_state['Lively'] | physical_state['Not So Tired']) &
                        (reviews['Good'] | reviews['Average'] ) & (release_year['New'] | release_year['Very New']) & 
                        (polarity['Positive'] | polarity['Very Positive']), recommend['Recommend'])

    rule_15 = ctrl.Rule((mood['Upset'] | mood['Very Upset']) & (physical_state['Tired'] | time['Late'] | time['Very Late']) &
                        (reviews['Good'] | reviews['Average'] ) & (release_year['New'] | release_year['Very New']) & 
                        (polarity['Positive'] | polarity['Very Positive']) & (duration['Short'] | duration['Very Short']),
                        recommend['Recommend'])

    rule_16 = ctrl.Rule((mood['Upset'] | mood['Very Upset']) & (physical_state['Exhausted'] | time['Late'] | time['Very Late']) &
                        (reviews['Good'] | reviews['Average'] ) & (release_year['New'] | release_year['Very New']) & 
                        (polarity['Positive'] | polarity['Very Positive']) & duration['Short'],
                        recommend['Recommend'])
    
    # Initialize the Fuzzy Rule Base.
    netflix_ctrl = ctrl.ControlSystem([rule_1, rule_2, rule_3, rule_4, rule_5, rule_6, rule_7, rule_8,
                                        rule_9, rule_10, rule_11, rule_12, rule_13, rule_14, rule_15, rule_16])
    
    return netflix_ctrl




