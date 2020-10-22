import time
import pickle
import sys
import numpy as np

from benderopt_min import minimize
from hyperopt import fmin, tpe, space_eval, Trials, STATUS_OK
from parameters import BenderoptParameters, HyperoptParameters
from honest_models import HonestModels
from splitworld_models import SplitworldModels
from prism_data import PRISMData
from sql_writer import SqlWriter
from optimiser_args import OptimiserArgs
from utilities import choose_probabilities
from copy import deepcopy
from pprint import pprint
import json

# Parse command-line arguments
arguments = OptimiserArgs()
options = arguments.parse_args()

# Initialise problem Parameters
if options.hyperopt:
    parameters = HyperoptParameters(options.mul_init)
else:
    parameters = BenderoptParameters(options.mul_init)
distributions = parameters.distributions

"""
Load previous experiment data if a file is supplied. Otherwise, create 
a new Trials object (hyperopt) or create a new list (benderopt)
"""
try:
    trials = pickle.load(open(options.trials, "rb"))
    if options.hyperopt:
        trial_len = len(trials.trials)
    else:
        trial_len = len(trials)
    if trial_len >= options.evaluations:
        err_msg = 'size of trial data ({x}) equals or exceeds the number of evaluations to be done ({y})'
        raise ValueError(err_msg.format(x=trial_len, y=options.evaluations))
    print("Rerunning from {x} trials to {y} (+{z}) trials...".
        format(x=trial_len, 
               y=options.evaluations,
               z=options.evaluations-trial_len)
        )
    decision = None 
    while True:
        decision = input('Is this ok (y/n)? ')
        if decision == 'y':
            break
        if decision == 'n':
            print("Quitting...")
            sys.exit()
    evaluation_num = trial_len
except IOError:
    if options.hyperopt:
        print('No trial data found. Creating new hyperopt Trials object...')
        trials = Trials()
    else:
        print('No trial data found. Creating new benderopt observation list...')
        trials = []
    evaluation_num = 0

# Create SQLite database
sql_database = SqlWriter(options)

# filenames
LOG_FILE = 'build/log.txt'
RESULT_FILE = 'build/result.txt'
PRISM_FILE = 'build/model.prism'
STDOUT = options.std_out


"""
The 'black-box' function we want to investigate. Acts as a wrapper function.
Find the worst case for a given model type and property using the defined
probability intervals.
"""
def objective_function(sanitiser):
    def wrapper(*args, **kwargs):
        global evaluation_num
        space, profiles = sanitiser(*args, **kwargs)
        for i in range(len(profiles)):
            distributions_copy = deepcopy(distributions[str(i)])
            profiles[i] = choose_probabilities(distributions_copy,
                                               profiles[i])
        if options.is_split:
            prism_model = SplitworldModels(options, space, profiles)
        else:
            prism_model = HonestModels(options, space, profiles)
        prism_model.write_original_model(PRISM_FILE)
        prism_data = PRISMData(options, PRISM_FILE, space, LOG_FILE, 
        					   RESULT_FILE)
        prism_data.perform_verification()
        props_value = prism_data.extract_result()
        evaluation_num += 1
        values = (evaluation_num, str(props_value), str(profiles[0]),
                  str(profiles[1]), str(profiles[2]), space['client_count'],
                  space['connect_rates'], space['client_init'],
                  space['server_init'],)
        sql_database.write_data(values)
        loss = -max(props_value)
        if options.hyperopt:
            return {'loss': loss, 'status': STATUS_OK}
        else:
            return loss
    return wrapper


# Used for hyperopt
@objective_function
def hyperopt(space):
    c1p = [float(i) for i in space['type_one'].values()]
    c2p = [float(i) for i in space['type_two'].values()]
    c3p = [float(i) for i in space['type_three'].values()]
    profiles = [c1p, c2p, c3p]
    return space, profiles


# Used for benderopt
@objective_function
def benderopt(client_count, connect_rates, client_init, server_init,
              p_1_1, p_1_2, p_1_3, p_1_4,
              p_2_1, p_2_2, p_2_3, p_2_4,
              p_3_1, p_3_2, p_3_3, p_3_4):
    space = dict()
    space['client_count'] = client_count
    space['connect_rates'] = connect_rates
    space['client_init'] = client_init
    space['server_init'] = server_init
    space['p_1_1'] = float(p_1_1)
    space['p_1_2'] = float(p_1_2)
    space['p_1_3'] = float(p_1_3)
    space['p_1_4'] = float(p_1_4)
    space['p_2_1'] = float(p_2_1)
    space['p_2_2'] = float(p_2_2)
    space['p_2_3'] = float(p_2_3)
    space['p_2_4'] = float(p_2_4)
    space['p_3_1'] = float(p_3_1)
    space['p_3_2'] = float(p_3_2)
    space['p_3_3'] = float(p_3_3)
    space['p_3_4'] = float(p_3_4)
    profiles = [[float(p_1_1), float(p_1_2), float(p_1_3), float(p_1_4)],
                [float(p_2_1), float(p_2_2), float(p_2_3), float(p_2_4)],
                [float(p_3_1), float(p_3_2), float(p_3_3), float(p_3_4)]]
    return space, profiles


def run():
    start_time = time.time()
    try:
        if options.hyperopt:
            best_sample = fmin(fn=hyperopt,
                               space=parameters.space, 
                               algo=tpe.suggest,
                               max_evals=options.evaluations,
                               trials=trials)
        else:
            optimization_problem = {
                'parameters': parameters.optimization_problem_parameters,
                'observations' : trials,
            }
            best_sample = minimize(benderopt,
                                   optimization_problem,
                                   trials,
                                   number_of_evaluation=options.evaluations)
    except KeyboardInterrupt:
        best_sample = "N/A"
        print('Process interrupted.')
    finally:
        end_time = time.time()
        with open(options.trials, "wb") as f:
            pickle.dump(trials, f)
            print('{file} updated'.format(file=options.trials))
        print('\nFinished. Writing to file...')
        with open(STDOUT, 'w') as f:
            duration = "--- Execution time: %s seconds ---\n" % (
                end_time - start_time)
            f.write(duration)
            f.write("suggested parameters that optimise performance:\n")
            if options.hyperopt:
                f.write(str(space_eval(parameters.space, best_sample)) + '\n')
            else:
                f.write(str(best_sample) + '\n')
            if options.is_split:
                f.write('Model type used: split-world\n')
            else:
                f.write('Model type used: honest\n')
            if options.mul_init:
                f.write('Multiple initial states used\n')
            profiles = [
                [
                    float(best_sample["p_1_1"]),
                    float(best_sample["p_1_2"]),
                    float(best_sample["p_1_3"]),
                    float(best_sample["p_1_4"]),
                ],
                [
                    float(best_sample["p_2_1"]),
                    float(best_sample["p_2_2"]),
                    float(best_sample["p_2_3"]),
                    float(best_sample["p_2_4"]),
                ],
                [
                    float(best_sample["p_3_1"]),
                    float(best_sample["p_3_2"]),
                    float(best_sample["p_3_3"]),
                    float(best_sample["p_3_4"]),
                ]
            ]
            for i in range(len(profiles)):
                distributions_copy = deepcopy(distributions[str(i)])
                profiles[i] = choose_probabilities(distributions_copy,
                                                   profiles[i])
                f.write("\nSuggested distribution for client type {i}: ".format(i=i+1))
                f.write(str(profiles[i]))


if __name__ == "__main__":
    import os
    try:
        os.makedirs("build")
    except FileExistsError:
        pass
    run()