<a><img src="https://www.electricaltechnology.org/wp-content/uploads/2018/01/fff.png" title="FuzzyControlSystem" alt="FuzzyControlSystem"></a>


## Building a Mamdani Fuzzy Control System for Movie Recommendations. 


### Requirements:

The program requires Python 3.7.4.

### Installing
    
To download the necessary libraries run the follwing command in the terminal: 

```
pip install -r requirements.txt
```

### Content

* /Pipline
    pipline_functions.py
* /Data
    * clean_data.csv
    * netflix_titles.csv
* /Fuzzy Controller
    * fuzzy_controller.py
    * system.py
* pipline_master.py
* recommender_master.py

### Data Processing Pipline
The data for this demonstration case comes from NetFlix and is available at https://www.kaggle.com/shivamb/netflix-shows/data.
You can also download the dataset directly from the commend line by running the following command in the terminal:
* Note: You need to have kaggle installed:
```
pip install kaggle
```
And you need the kaggle.json (the token) file placed in the same directory.

```
kaggle datasets download -d shivamb/netflix-shows
```

The data processing pipline takes the raw kaggle dataset and prepares it for the analysis. Because this is a demonstration case I did not went to much into the proper data cleaning process. I build a couple of features based on the available data and applied some basic cleaning procedures. Totally unnecessary for this case, but wanted to have fun, I decided run the pipline tasks in parallel. In other words the dataset is partitioned into 10 parts and then the cleaning tasks are implemented on each partition in parallel. Afterwards, the cleaned segments are concatinated. At the end a clean_data.csv file is outputed.

The pipline selects only 'Movies' released in the United States and are only in the Mature category according to the Netflix Categorizatino scheme.
The dataset included the following features:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 6234 entries, 0 to 6233
Data columns (total 12 columns):
show_id         6234 non-null int64
type            6234 non-null object
title           6234 non-null object
director        4265 non-null object
cast            5664 non-null object
country         5758 non-null object
date_added      6223 non-null object
release_year    6234 non-null int64
rating          6224 non-null object
duration        6234 non-null object
listed_in       6234 non-null object
description     6234 non-null object
dtypes: int64(2), object(10)
memory usage: 584.6+ KB
```
For this demonstration case I created the following features:

```
<class 'pandas.core.frame.DataFrame'>
RangeIndex: 352 entries, 0 to 351
Data columns (total 11 columns):
show_id            352 non-null int64
title              352 non-null object
release_year       352 non-null int64
description        352 non-null object
description_len    352 non-null int64
title_len          352 non-null int64
mv_dur             352 non-null int64
genre              352 non-null object
polarity           352 non-null float64
subjectivity       352 non-null float64
rotten_score       352 non-null float64
dtypes: float64(3), int64(5), object(3)
memory usage: 30.3+ KB
```
__Description_len__ and the __title_len__ are the length of the description and the title of the movie (number of characters). Later on I decided not to use these features. mv_dur is the movie duration in minutes. __Polarity__ and __subjectivity__ scores are from the sentiment analysis of the description text. The polarity (ranges from -1 to 1) reflects the positivity of the text whereas the subjectivty score reflects the extent to which it is oppinionated (ranges from 0-1). The __rotten score__ is the *Rotten Tomattoes* review score. This was necessary because netflix does not provide review data. To obtain this score I used the *Rotten Tomatoes* python API. Because of the time constraint I decided to limit the Fuzzy Control System to only the following features: *release_year, movie duration, polarity, subjectivity and rotten score.*

### Fuzzy Control System

The Fuzzy Control System includes three blocks: 1) __Fuzzification__, 2) __Inference,__ 3) __Defuzzification.__

In the __Fuzzification__ stage, the crisp input is converted to a fuzzy set which is passed to the __Inference__ engine. The fuzzy input sets activate certain rules in the rule base which gives a fuzzy output set. Afterwards __Deffuzzification__ converts the fuzzy ouput set into a crisp value.

For this system I decided to use two types of input variables: User's internal state and features of the movies in the database.
The User's internal state includes the user's mood (Very Happy -> Very Upset) and the physical state (Exchausted -> Very lively). The features of the movies are the ones presented above. Now the system is only going to ask the user to specify the to internal states and the rest is going to be taken from the respective database. 

For the fuzzification block I need to specify the Universe of Discourse (i.e., the domain of the inputs), the set of terms for each linguistic variables (Very Old', 'Old', 'Not So Old', 'New', 'Very New') and the respective membership function for each term.
Because this is a demonstration case, I wanted to show how you can specify different membership functions. For this I used three types of membership functions: *Triangular*, *Gaussian* and *S-Shaped*. The Skit-Fuzzy module in python allows for automatic generation of triangular membership function. For this you need to specify only the number of the terms and the terms themselves. Other functions you must specify manually (maybe you could do it automatically but couldn't find it in the documentation). For example, I specified a *Gaussian* membership function for the duration of the movie. For each term you need to specify the mean and the standard deviation of the curve. For the system output (i.e., recommendation score) I specified an *S-Shapped* membership function. For this you need to specify the uper and the lower bounds (0,1 in this case).

Here, I will not go in depth of how the fuzzification works (I will soon write a more detailed blog on this) it would suffice to say that the membership function maps the Universe of Discourse and the set of terms to the fuzzy range of [0,1]. After which each input variable can be converted into a fuzzy set that reflects its degree of membership to the specified terms.

The second block is the *Inference* engine. Here one needs to specify the rules by which the fuzzy inputs are connected to the output fuzzy output. The rules look like this:

> * __Rule 1:__
    * If *{Mood}* is <u>Very Happy</u> __AND__ *{Physcial State}* is <u>Very Lively</u> __AND__ the movie *{Reviews}* are <u>Average</u> __OR__ *{Release Year}* is <u>New</u> __OR__  *{Release Year}* is <u>Very New</u> __THEN__ <span style="color:red">__Recommend.__</span>

This is codded as:

```
rule_1 = ctrl.Rule(mood['Very Happy'] & physical_state['Very Lively'] & (reviews['Average'] | release_year['New'] |
                                release_year['Very New']), recommend['Recommend'])
```
The rule base of the current system includes 16 rules in total. It is important to assure the input values activate at least one of the rules in the rule base otherwise you will get an empty set. The rules for this system were derived somewhat arbitrarily. In reality there are regorouse approaches to do that. There is also a way of deriving these rules from the data (e.g., fuzzy adaptive system, fuzzy neural networks).

The third block is the *Defuzzification*. In short, the convert the fuzzy sets to a crisp output value the Mamdani rull cuts the curve based on the fuzzy values and then calculates the area under the curve and takes the centroid of the area.

Now let's take a look how the system runs! :)

To run the system type the following in the command line:

```
python recommender_master.py
```

You should see the following:

<<<<<<< HEAD
<img src="https://github.com/SamvelMK/fuzzy_contoller/blob/master/images/Capture.jpg" width="40" height="40" />
=======
<img src="https://github.com/SamvelMK/fuzzy_contoller/blob/master/myFile.gif" width="1000" height="400" />
>>>>>>> 8b41acadd1763eb7997af6c0a6813a25098dde4c


