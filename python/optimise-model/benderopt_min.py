from benderopt.base import OptimizationProblem, Observation
from benderopt.optimizer import optimizers
import numpy as np
import json

JSON_FILE = 'build/bopt_json.txt'
STEP = 0.1
step = 0.1


def update_progress(progress):
    global step
    while progress >= step:
        print('{p:2.0f}% '.format(p=step*100), flush=True, end="")
        step += STEP


"""
This method is based on the minimize method as seen in benderopt.minimizer.
Using trial data in trials, it suggests the next set of parameters to evaluate
that when the loop starts. If no trial data exists, optimizer will just suggest
a point to start at and carry on as normal. If debug is true, all samples are r
returned instead of the best sample found.
"""
def minimize(objective_function,
             optimization_problem,
             trials,
             optimizer_type="parzen_estimator",
             number_of_evaluation=100,
             seed=None,
             debug=False,
             ):

    np.random.seed(seed=seed)
    samples = []
    trial_len = len(trials)
    remaining_eval = number_of_evaluation - trial_len
    with open(JSON_FILE, 'w') as f:
        json.dump(optimization_problem, f)
    optimization_problem = OptimizationProblem.from_json(JSON_FILE)
    optimizer = optimizers[optimizer_type](optimization_problem)
    print('progress: ', flush=True, end="")
    update_progress(trial_len/number_of_evaluation)
    for _ in range(remaining_eval):
        sample = optimizer.suggest()
        samples.append(sample)
        loss = objective_function(**sample)
        obs_dict = {"loss": loss, "sample": sample}
        observation = Observation.from_dict(obs_dict)
        trials.append(obs_dict)
        trial_len += 1
        optimization_problem.add_observation(observation)
        update_progress(trial_len/number_of_evaluation)
    if debug is True:
        return samples
    print('\n')
    return optimization_problem.best_sample