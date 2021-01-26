# Change parameter values here
	output_dir = 'results/new-chapter-6-honest/'
	# If false, skip to just plotting the graph with given data
	do_trials = True
	# If false, code does not generate random parameters to overwrite model_data with
	is_random = True
	# List of properties in the order as they are in the .props file.
	props = {
		1: {
		    'filename': output_dir + 'ch6_smbo_client_prop_concrete_initial.png',
		    'y_label': 'Expected Client Proportion',
		    'mc_file': CH6_SMBO_MC_DIR + 'honest_original_clientprop.txt',
		},
	}
	props_file = "files/props_honest_init.props"
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
		'is_split': False,
		'is_ext': False,
		'is_sim': True,
	}