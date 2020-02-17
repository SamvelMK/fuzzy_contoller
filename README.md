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

The pipline selects only 'Movies' released in the United States.
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
Description_len and the title_len are the length of the description and the title (number of characters). Later on I decided not to use these features. mv_dur is the movie duration in minutes. __Polarity__ and __subjectivity__ scores are from the sentiment analysis of the description text. The polarity (ranges from -1 to 1) reflects the positivity of the text whereas the subjectivty score reflects the extent to which it is oppinionated (ranges from 0-1). The __rotten score__ is the *Rotten Tomattoes* review score. This was necessary because netflix does not provide review data. To obtain this score I used the *Rotten Tomatoes* python API. Because of the time constraint I decided to limit the Fuzzy Control System to only the following features: *release_year, movie duration, polarity, subjectivity and rotten score.*
