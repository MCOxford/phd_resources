#!/bin/bash

# Options for smbo.py:
# -e (--evaluations) - The number of trials to perform. Default value is 500.
# -s (--split) - Perform model checking on splitworld models instead of honest.
# -db (--database) - Which database to write data into. Default is to write to build/test_db.sqlite.
# -mulinit (--multipleinitialstates) - Model check over multiple initial state. Default is to have only one dependent on chosen parameters.
# -p (--propertyno) - Which property to evaluate by inputting an integer depending on where property is listed in the file. Default is to use the first listed property in the .props file.
# -symm (--symmreduction) - Automatically apply symmetry reduction on models.
# -hopt (--hyperopt) - Use the hyperopt optimiser. Otherwise, benderopt is used.
# -props (--propfile) - Which property file to use (REQUIRED).
# -out (--output) - Where to write suggested parameters to. Default file path is build/output_one.txt
# -t (--trials) - Where to write (or read) trial data. If smbo.py cannot find trial data, it will create a new data structure to save trial data to (REQUIRED).

# Example commands

# normal models (hyperopt)
python smbo.py -e 200 -t results/hyperopt-unique-initial-state/trials.hyperopt -props files/honest.props -hopt -symm -db results/hyperopt-unique-initial-state/honest_200e_prop1.sqlite -out results/hyperopt-unique-initial-state/honest_200e_prop1.txt;
python smbo.py -e 200 -t results/hyperopt-multiple-initial-states/trials.hyperopt -props files/honest.props -mulinit -hopt -symm -db results/hyperopt-multiple-initial-states/honest_200e_prop1_mulinit.sqlite -out results/hyperopt-multiple-initial-states/honest_200e_prop1_mulinit.txt;

# normal models (benderopt)
python smbo.py -e 200 -t results/benderopt-unique-initial-state/trials.benderopt -props files/honest.props -symm -db results/benderopt-unique-initial-state/honest_200e_prop1.sqlite -out results/benderopt-unique-initial-state/honest_200e_prop1.txt;
python smbo.py -e 200 -t results/benderopt-multiple-initial-states/trials.benderopt -props files/honest.props -mulinit -symm -db results/benderopt-multiple-initial-states/honest_200e_prop1_mulinit.sqlite -out results/benderopt-multiple-initial-states/honest_200e_prop1_mulinit.txt;

# split-world model (hyperopt)
d="results/hyperopt-multiple-initial-states";
d1="results/benderopt-unique-initial-state";
python smbo.py -e 200 -t ${d1}/splitworld_trials.hyperopt -props files/splitworld.props -s -hopt -symm -db ${d1}/splitworld_200e_prop1.sqlite -out ${d1}/splitworld_200e_prop1.txt;
python smbo.py -e 25 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -hopt -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;
python smbo.py -e 50 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -hopt -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;
python smbo.py -e 75 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -hopt -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;
python smbo.py -e 100 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -hopt -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;

# split-world model (benderopt)
d="results/benderopt-multiple-initial-states";
d1="results/benderopt-unique-initial-state";
python smbo.py -e 200 -t ${d1}/splitworld_trials.benderopt -props files/splitworld.props -s -symm -db ${d1}/splitworld_200e_prop1.sqlite -out ${d1}/splitworld_200e_prop1.txt;
python smbo.py -e 25 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;
python smbo.py -e 50 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;
python smbo.py -e 75 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;
python smbo.py -e 100 -t ${d}/splitworld_trials.hyperopt -props files/splitworld.props -mulinit -s -symm -db ${d}/splitworld_100e_prop1_mulinit.sqlite -out ${d}/splitworld_100e_prop1_mulinit.txt;

# stability testing (normal models)
for i in 1 2 3
do
	for j in 1 2 3 4
	do
		d="results/honest-stability-test";
		python stability_test.py -e 10 -t ${d}/trials_${i}_${j}.hyperopt -props files/honest.props -hopt -symm -ft ${i} -fp ${j} -db ${d}/honest_stability_${i}_${j}.sqlite -out ${d}/honest_stability_${i}_${j}.txt;
	done
done

# stability testing (split-world models)
for i in 1 2 3
do
	for j in 1 2 3 4
	do
		d="results/split-world-stability-test";
		python stability_test.py -e 10 -t ${d}/trials_${i}_${j}.hyperopt -props files/splitworld.props -s -hopt -symm -ft ${i} -fp ${j} -db ${d}/splitworld_stability_${i}_${j}.sqlite -out ${d}/splitworld_stability_${i}_${j}.txt;
	done
done
