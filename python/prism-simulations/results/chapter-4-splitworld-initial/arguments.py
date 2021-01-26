output_dir = 'output/'
do_trials = True
props = {
	1: {
	    'filename': 'output/ch4_detect_concrete_initial.png',
	    'y_label': 'Expected Detection Probability',
	    'mc_file': CH4_SPLIT_MC_DIR + 'splitWorld_originalDesign_detection.txt',
	},
	2: {
	    'filename': 'output/ch4_old_data_concrete_initial.png',
	    'y_label': 'Expected Proportion',
	    'mc_file': CH4_SPLIT_MC_DIR + 'splitWorld_originalDesign_clientProportionOld.txt',
	},
	3: {
	    'filename': 'output/ch4_real_data_concrete_initial.png',
	    'y_label': 'Expected Proportion',
	    'mc_file': CH4_SPLIT_MC_DIR + 'splitWorld_originalDesign_clientProportionReal.txt',
	},
	4: {
	    'filename': 'output/ch4_fake_data_concrete_initial.png',
	    'y_label': 'Expected Proportion',
	    'mc_file': CH4_SPLIT_MC_DIR + 'splitWorld_originalDesign_clientProportionFake.txt',
	},
	5: {
	    'filename': 'output/ch4_split_sth_only_concrete_initial.png',
	    'y_label': 'Expected Cumulative Log Connections',
	    'mc_file': CH4_SPLIT_MC_DIR + 'splitWorld_originalDesign_logConn_sthOnly.txt',
	},
	6: {
	    'filename': 'output/ch4_split_sth_proof_concrete_initial.png',
	    'y_label': 'Expected Cumulative Log Connections',
	    'mc_file': CH4_SPLIT_MC_DIR + 'splitWorld_originalDesign_logConn_sthProof.txt',
	},
}
props_file = "props_split_init.props"
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
}
