import logging
import numpy as np
import pandas as pd
from asl_data import AslDb
import timeit

def add_features_ground(asl):
    # Add df columns for 'grnd-rx', 'grnd-ly', 'grnd-lx' representing
    # differences between hand and nose locations
    asl.df['grnd-ry'] = asl.df['right-y'] - asl.df['nose-y']
    asl.df['grnd-rx'] = asl.df['right-x'] - asl.df['nose-x']
    asl.df['grnd-ly'] = asl.df['left-y'] - asl.df['nose-y']
    asl.df['grnd-lx'] = asl.df['left-x'] - asl.df['nose-x']
    return asl

def initialise_asl_db():
    asl = AslDb()
    add_features_ground(asl)
    # Display first five rows (pandas data frame) of ASL database, indexed by video and frame
    # asl.df.head()
    return asl

def run_bic(asl, features_ground, words_to_train, min_c, max_c, rand_s):
    # Copied from asl_recognizer.ipynb for IDE debugging using breakpoints.
    # Execute the implementation of SelectorBIC in module my_model_selectors.py
    from my_model_selectors import SelectorBIC

    training = asl.build_training(features_ground)
    print("BIC Available Training words - words: ", training.words)
    print("BIC Quantity of Training words - num_items: ", training.num_items)
    print("BIC Chosen Training words: ", words_to_train)
    print("BIC Chosen Features: ", features_ground)
    sequences = training.get_all_sequences()
    Xlengths = training.get_all_Xlengths()
    for word in words_to_train:
        start = timeit.default_timer()
        model = SelectorBIC(sequences, Xlengths, word,
                            min_n_components=min_c,
                            max_n_components=max_c,
                            random_state = rand_s).select()
        end = timeit.default_timer()-start
        if model is not None:
            print("Training complete for {} with {} states with time {} seconds".format(word, model.n_components, end))
        else:
            print("Training failed for {}".format(word))

def run_dic(asl, features_ground, words_to_train, min_c, max_c, rand_s):
    # Copied from asl_recognizer.ipynb for IDE debugging using breakpoints.
    # Execute the implementation of SelectorDIC in module my_model_selectors.py
    from my_model_selectors import SelectorDIC

    training = asl.build_training(features_ground)
    print("DIC Available Training words - words: ", training.words)
    print("DIC Quantity of Training words - num_items: ", training.num_items)
    print("DIC Chosen Training words: ", words_to_train)
    print("DIC Chosen Features: ", features_ground)

    sequences = training.get_all_sequences()
    Xlengths = training.get_all_Xlengths()
    for word in words_to_train:
        start = timeit.default_timer()
        model = SelectorDIC(sequences, Xlengths, word,
                            min_n_components=min_c,
                            max_n_components=max_c,
                            random_state = rand_s).select()
        end = timeit.default_timer()-start
        if model is not None:
            print("Training complete for {} with {} states with time {} seconds".format(word, model.n_components, end))
        else:
            print("Training failed for {}".format(word))

def run():
    try:
        asl = initialise_asl_db()
        features_ground = ['grnd-rx', 'grnd-ry', 'grnd-lx', 'grnd-ly']
        words_to_train = ['FISH', 'BOOK', 'VEGETABLE', 'FUTURE', 'JOHN']

        min_c = 2   # default 2
        max_c = 15   # default 15
        rand_s = 14 # default 14

        # logging.info("Recogniser calling BIC Model Selector")
        # run_bic(asl, features_ground, words_to_train, min_c, max_c, rand_s)

        logging.info("Recogniser calling DIC Model Selector")
        run_dic(asl, features_ground, words_to_train, min_c, max_c, rand_s)

    except SystemExit:
        logging.exception('SystemExit occurred')
    except KeyError as e:
        cause = e.args[0]
        logging.exception('Exception KeyError caused by: ', cause)
    except Exception as e:
        logging.exception('Exception occurred: ', e)

if __name__ == '__main__':
    run()