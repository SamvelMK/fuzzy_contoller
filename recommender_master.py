from FuzzyController.fuzzy_controller import MovieController
import time

if __name__ == '__main__':
    starttime = time.time()

    mv = MovieController()
    print('Welcome to Fuzzy Movie Recommender System')
    print('')
    name = input('What is your name? ')
    mv.create_sim_instance(name)
    
    print(f'Welcome {name}.')
    print('')
    mood = input('How would you rate your mood now from 0 (Very Upset) to  10 (Very Happy).')
    print('')
    print('Thank You!')
    physical_state = input('How would you rate your physical state from 0 (Exhausted) to 10 (Very Lively)')
    print('')
    print('Thank You! I am generating a few recommendations for you.')
    print('')

    mv.calculate(int(mood), int(physical_state))
    print(mv.results())

    print('Time taken = {} seconds'.format(time.time() - starttime))