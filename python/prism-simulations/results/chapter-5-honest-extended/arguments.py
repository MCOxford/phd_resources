output_dir = 'ch5_honest_imc_ext/'
	is_random = False
	do_trials = True
	props = {
		1: {
			'filename': output_dir + 'ch5_imc_honest_ext_all_updated.png',
			'y_label': 'Prob(Clients all updated)',
			'mc_file': CH5_IMC_MC_DIR + 'honest_ext_pmin_all_updated.txt',
		},
	}
	props_file = "props_honest_ext.props"
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
		'is_ext': True,
	}
