output_dir = 'ch5_honest_imc_init/'
	is_random = False
	do_trials = True
	props = {
		1: {
			'filename': output_dir + 'ch5_imc_honest_init_all_updated.png',
			'y_label': 'Probability of clients\\ all updated with new data',
			'mc_file': CH5_IMC_MC_DIR + 'honest_pmin_all_updated.txt',
		},
	}
	props_file = "props_honest_init.props"
	model_data = {
		'freq': {
			1: 1,
			2: 1,
			3: 1,
		},
		'c_types': 3,
		'c_init': [0, 0, 1],
		's_types': 5,
		's_init': [1, 0, 0, 0, 0],
		'is_split': False,
		'is_ext': False,
	}
