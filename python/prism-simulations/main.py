import numpy as np
from pprint import pprint
from matplotlib.ticker import MaxNLocator
import matplotlib.pyplot as plt
from subprocess import call
from random import choices
import sys
import os

try:
	sys.path.append("../create-prism-models/")
	from prism_model import PRISMModel
except:
	print('prism_model.py not found.')

try:
	os.makedirs("build/")
except FileExistsError:
	pass
LOG_FILE = "build/log.txt"
PRISM_FILE = "build/model.prism"
SIM_SAMPLES = "5000"
RESULT_FILE = "build/result.res"

NUM_TRIALS = 1000
ROUNDS = 20

# paths to find verification results. Change if necessary.
CH4_HONEST_MC_DIR = '../chapter-4-results/verification/honest/model-checking'
CH4_SPLIT_MC_DIR = '../chapter-4-results/verification/split-world/model-checking/'
CH5_IMC_MC_DIR = '../chapter-5-idtmc-results/'
CH6_SMBO_MC_DIR = '../chapter-6-results/thesis-results/model-checking/'

# Code randomly picks an element from each list to construct model. Used for chapter 6.
c_freq_list = [[1,1,3], [1,3,1], [3,1,1], [1,2,2], [2,1,2], [2,2,1]]
c_init_list = [[1,0,0], [0,1,0], [0,0,1]]
s_init_list = [[1,0,0,0,0], [0,1,0,0,0], [0,0,1,0,0] , [0,0,0,1,0], [0,0,0,0,1]]

def type_IDs(num_client_types, data):
    type_ids = {}
    for i in range(1, num_client_types+1):
        type_ids[i] = []
        for client in data:
            if data[client]['TYPE'] == i:
                type_ids[i].append(client)
    return type_ids


# Pick random clients to concstruct the .prism model with.
def extract_random_clients(type_ids, model_data, concrete_data):
    sample = []
    sample_data = {}
    for ctype in type_ids:
        clients = choices(type_ids[ctype], k=model_data['freq'][ctype])
        sample.extend(clients)
    for client in sample:
        sample_data[len(sample_data)] = concrete_data[client]
    return sample_data


# Call PRISM using the terminal and extract each property result.
def simulator_results(props, props_file):
    results = {}
    for i in range(1, len(props)+1):
        property_results = []
        with open(LOG_FILE, 'wb') as f:
            terminal_call = ["prism", PRISM_FILE, props_file, "-prop", str(i),
                             "-const", "T=1:1:{rounds}".format(
                                 rounds=ROUNDS),
                             "-sim", "-simsamples", SIM_SAMPLES,
                             "-exportresults", RESULT_FILE]
            call(terminal_call, stdout=f)
        with open(RESULT_FILE, 'r') as f:
            for j, line in enumerate(f):
                if j == 0:
                    continue
                line = line.strip()
                line = line.split('\t')
                property_results.append(float(line[1]))
                if not line:
                    break
        results['prop_' + str(i)] = property_results
    return results


# Run trials.
def run_trials(concrete_data, is_rand, props, props_file, model_data):
    print('progress: 0% ', flush=True, end="")
    step = 0.1
    trial_results = {}
    type_ids = type_IDs(model_data['c_types'], concrete_data)
    for trial in range(NUM_TRIALS):
        if is_rand:
            rand_client_freq = choices(c_freq_list, k=1)[0]
            rand_client_init = choices(c_init_list, k=1)[0]
            rand_server_init = choices(s_init_list, k=1)[0]
            model_data['freq'][1] = rand_client_freq[0]
            model_data['freq'][2] = rand_client_freq[1]
            model_data['freq'][3] = rand_client_freq[2]
            model_data['c_init'] = rand_client_init
            model_data['s_init'] = rand_server_init
        #print(model_data)
        sample_data = extract_random_clients(type_ids, model_data, concrete_data)
        pm = PRISMModel(sample_data, model_data['s_types'], model_data['c_init'],
                        model_data['s_init'], model_data['is_split'], 
                        model_data['is_ext'], model_data['is_sim'], PRISM_FILE)
        pm.write_file()
        result = simulator_results(props, props_file)
        trial_id = len(trial_results)
        trial_results[trial_id] = {}
        trial_results[trial_id]['client_indexes'] = sample_data
        trial_results[trial_id]['simulator_results'] = result
        while (trial+1)/NUM_TRIALS >= step:
            print('{p:2.0f}% '.format(p=step*100), flush=True, end="")
            step += 0.1
    return trial_results


# Write all trial data to a .py in the form of a dictionary.
def write_results(trial_results, trial_data_file, variable_name):
    with open(trial_data_file, 'w') as f1:
        f1.write('{name} = '.format(name=variable_name))
        pprint(trial_results, stream=f1)


# Plot .png graph plotting both simulator and verification results.
def plot_graph(trial_results, prop_num, y_label, mc_file, matplot_file):
	prop_key = 'prop_' + str(prop_num)
	min_val = np.array([np.Infinity]*ROUNDS, dtype=float)
	max_val = np.zeros((ROUNDS, ), dtype=float)
	mc_result = []
	for trial in trial_results:
		prop_results = np.array(trial_results[trial]['simulator_results'][prop_key])
		for i in range(ROUNDS):
			r = prop_results[i]
			min_y = np.amin(r)
			max_y = np.amax(r)
			if min_y < min_val[i]:
				min_val[i] = min_y
			if max_y > max_val[i]:
				max_val[i] = max_y
	x = np.arange(1, ROUNDS+1)
	with open(mc_file, 'r') as f:
		for i, line in enumerate(f):
			if 'T' in line:
				continue
			line = line.strip()
			if not line:
				break
			line = line.split()
			mc_result.append(float(line[1]))
	mc_result = np.array(mc_result)
	f, ax = plt.subplots()
	plt.xticks(fontsize=10)
	plt.yticks(fontsize=10)
	plt.style.use('seaborn-white')
	plt.grid()
	ax.xaxis.set_major_locator(MaxNLocator(nbins=ROUNDS, integer=True))
	ax.set_ylabel(y_label, fontsize=14)
	ax.set_xlabel('Gossip Round', fontsize=14)
	ax.set_xlim([1, ROUNDS])
	ax.set_ylim([0, np.amax(max_val)*1.05])
	l1 = ax.plot(x, min_val, color='b', linestyle='solid',
		         linewidth=1.5, label='Range of Simulation Results')
	l2 = ax.plot(x, max_val, color='b',
		         linestyle='solid', linewidth=1.5)
	l3 = ax.plot(x, mc_result, color='r',
		         linestyle='dashed', linewidth=2.0, label='Verification Result')
	fi = ax.fill_between(x, min_val, max_val, facecolor='c',
		                 alpha=0.25)
	ax.legend()
	plt.savefig(matplot_file, dpi=300, bbox_inches='tight')
	print('\n{file} created.'.format(file=matplot_file))


def main(do_trials, concrete_data, is_rand, props, props_file, model_data, output_dir):
	if do_trials:
		trials_data = run_trials(concrete_data, is_rand, props, props_file, model_data)
		write_results(trials_data, output_dir + 'trial_data.py', 'trials_data')
	else:
		try:
			from trial_data import trials_data
		except ImportError:
			print('trial_data could not be found')
	for prop in props:
		plot_graph(trials_data, prop, props[prop]['y_label'], 
        		   props[prop]['mc_file'], props[prop]['filename'])


if __name__ == '__main__':
	try:
		from ch4_data import ch4_data
		from ch5_data import ch5_data
		from ch6_data import ch6_data
	except ImportError:
		print('data not found. Have you supplied them correctly?')
		sys.exit()
	# Change parameter values here
	output_dir = 'results/new-chapter-6-split-world/'
	# If false, skip to just plotting the graph with given data
	do_trials = True
	# If false, code does not generate random parameters to overwrite model_data with
	is_random = True
	# List of properties in the order as they are in the .props file.
	props = {
		1: {
			'filename': output_dir + 'ch6_smbo_detect_concrete_initial.png',
			'y_label': 'Detection Probability',
			'mc_file': CH6_SMBO_MC_DIR + 'split_original_detection.txt',
		},
	}
	props_file = "files/props_split_init.props"
	model_data = {
		'freq': {
			1: 1,
			2: 3,
			3: 1,
		},
		'c_types': 3,
		'c_init': [0, 0, 1],
		's_types': 5,
		's_init': [1, 0, 0, 0, 0],
		'is_split': True,
		'is_ext': False,
		'is_sim': True,
	}
	# -----
	try:
		os.makedirs(output_dir)
	except FileExistsError:
		pass
	main(do_trials, ch6_data, is_random, props, props_file, model_data, output_dir)

