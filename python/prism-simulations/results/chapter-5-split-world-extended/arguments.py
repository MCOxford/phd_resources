output_dir = 'ch5_split_imc_ext/'
	is_random = False
	do_trials = True
	props = {
		1: {
			'filename': output_dir + 'ch5_imc_concrete_split_ext_detect.png',
			'y_label': 'Detection rate',
			'mc_file': CH5_IMC_MC_DIR + 'splitworld_ext_pmin_detect.txt',
		},
	}
	props_file = "props_split_ext.props"
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
		'is_split': True,
		'is_ext': True,
	}
