"""
Code is essentially smbo.py but with a few changes. Used with
parameters suggested from an optimiser library to investigate whether
small fluctuations in some of the the continuous model parameters causes the 
objective function to behave erratically. 
"""
import time

from benderopt import minimize
from hyperopt import hp, fmin, tpe, rand, space_eval
from parameters import HyperoptStability
from honest_models import HonestModels
from splitworld_models import SplitworldModels
from prism_data import PRISMData
from sql_writer import SqlWriter
from optimiser_args import StabilityOptimiserArgs
from utilities import choose_probabilities
from copy import deepcopy
from random import randint

# Model parameters that give the worst-case results found (unique initial state only)
BENDEROPT_HONEST = {
    'client_count' : ['[3,1,1]'],
    'client_init_states': ['[0,0,1]'],
    'connect_rates': ['[0.5,0.5,0.5]'],
    'server_init_states': ['[0,0,1,0,0]'],
    '0': {
        's_1': 0.3668879123565087,
        's_2': 0.2566248732131312, 
        's_3': 0.027175713713532678,
        's_4': 0.2690779071661857,
        's_5': 0.08023359355064175,
    },
    '1': {
        's_1': 0.21393874414500336,
        's_2': 0.2279971450578929,
        's_3': 0.06076849802908572,
        's_4': 0.1741089991148236,
        's_5': 0.32318661365319445,
    }, 
    '2': {
        's_1': 0.03965211147346438,
        's_2': 0.09915021940963915, 
        's_3': 0.2943075813674938,
        's_4': 0.2529642146586943,
        's_5': 0.3139258730907084,
    },
}

HYPEROPT_SPLIT = {
    'client_count' : ['[1,3,1]'],
    'client_init_states': ['[1,0,0]'],
    'connect_rates': ['[0.5,0.5,0.5]'],
    'server_init_states': ['[0,0,1,0,0]'],
    '0': {
        's_1': 0.33438219267483904,
        's_2': 0.2068075423816448,
        's_3': 0.03475587840339814,
        's_4': 0.2774021413473147,
        's_5': 0.1466522451928034,
    },
    '1': {
        's_1': 0.24804575432397954,
        's_2': 0.22580942704319454, 
        's_3': 0.06304143915330328,
        's_4': 0.11347452350840198,
        's_5': 0.3496288559711207,
    }, 
    '2': {
        's_1': 0.05541083461008604,
        's_2': 0.21726869238687518,
        's_3': 0.07717983199961229,
        's_4': 0.25166913349111814,
        's_5': 0.3984715075123084,
    },
}

# Parse command-line arguments
arguments = StabilityOptimiserArgs()
options = arguments.parse_args()

# Initialise problem parameters
if options.hyperopt:
    if options.is_split:
        parameters = HyperoptStability(HYPEROPT_SPLIT, options.fix_type, options.fix_prob)
    else:
        parameters = HyperoptStability(BENDEROPT_HONEST, options.fix_type, options.fix_prob)
else:
    pass
distributions = parameters.distributions

# Create SQLite database
sql_database = SqlWriter(options)

# record current evaluation number. Used by benderopt.
evaluation_num = 0

# step for benderopt
step = 0

# filenames
LOG_FILE = 'build/log.txt'
RESULT_FILE = 'build/result.txt'
PRISM_FILE = 'build/model.prism'
STDOUT = options.std_out


"""
The 'black-box' function we want to investigate. Acts as a wrapper function.
Find the worst case for a given model type and property using the defined
probability intervals
"""
def objective_function(sanitiser):
    def wrapper(*args, **kwargs):
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
        values = (evaluation_num, str(props_value), str(profiles[0]),
                  str(profiles[1]), str(profiles[2]), space['client_count'],
                  space['connect_rates'], space['client_init'],
                  space['server_init'],)
        sql_database.write_data(values)
        return -max(props_value)
    return wrapper


@objective_function
def hyperopt(space):
    global evaluation_num
    c1p = [float(i) for i in space['type_one'].values()]
    c2p = [float(i) for i in space['type_two'].values()]
    c3p = [float(i) for i in space['type_three'].values()]
    profiles = [c1p, c2p, c3p]
    evaluation_num += 1
    return space, profiles


# Not used here
@objective_function
def benderopt(client_count, connect_rates, client_init, server_init,
              p_1_1, p_1_2, p_1_3, p_1_4,
              p_2_1, p_2_2, p_2_3, p_2_4,
              p_3_1, p_3_2, p_3_3, p_3_4):
    global evaluation_no
    global step
    space = dict()
    space['client_count'] = client_count
    space['connect_rates'] = connect_rates
    space['client_init'] = client_init
    space['server_init'] = server_init
    profiles = [[float(p_1_1), float(p_1_2), float(p_1_3), float(p_1_4)],
                [float(p_2_1), float(p_2_2), float(p_2_3), float(p_2_4)],
                [float(p_3_1), float(p_3_2), float(p_3_3), float(p_3_4)]]
    evaluation_no += 1
    while evaluation_no/options.evaluations > step:
        print('{p:2.0f}% '.format(p=step*100), flush=True, end="")
        step += 0.1
    return space, profiles


def run():
    start_time = time.time()
    try:
        if options.hyperopt:
            # We randomise parameters using only hyperopt and output the best suggestion
            best_sample = fmin(fn=hyperopt,
                               space=parameters.space, algo=rand.suggest,
                               max_evals=options.evaluations)
        else:
            pass
    except KeyboardInterrupt:
        best_sample = "N/A"
        print('Process interrupted.')
    finally:
        end_time = time.time()
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