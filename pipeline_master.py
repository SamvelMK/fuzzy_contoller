import pandas as pd
import numpy as np
from textblob import TextBlob
from rotten_tomatoes_client import RottenTomatoesClient
import multiprocessing as mp
from Pipline.pipline_functions import Pipline
import time


if __name__ == '__main__':    
    print(f'Launching the data cleaning pipline!')
    starttime = time.time()
    pipe = Pipline()

    processes = []
    num_partitions = 10 #number of partitions to split dataframe
    num_cores = mp.cpu_count() #number of cores on your machine
    
    d = pd.read_csv('Data/netflix_titles.csv')
    data = d.copy()
    data_split = np.array_split(data, num_partitions)
    
    pool = mp.Pool(num_cores)
    df = pd.concat(pool.map(pipe.pipline, data_split))
    pool.close()

    df.to_csv('Data/clean_data.csv')

    print('Time taken = {} seconds'.format(time.time() - starttime))