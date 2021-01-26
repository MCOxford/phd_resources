output_dir = 'output/'
do_trials = True
props = {
	1: {
	    'filename': 'output/ch4_client_prop_concrete_extended.png',
	    'y_label': 'Expected Client Proportion',
	    'mc_file': CH4_HONEST_MC_DIR + 'honest_newDesign_clientProportion.txt',
	},
	2: {
	    'filename': 'output/ch4_log_conn_sthonly_concrete_extended.png',
	    'y_label': 'Expected Cumulative Log Connections',
	    'mc_file': CH4_HONEST_MC_DIR + 'honest_newDesign_logConn_sthOnly.txt',
	},
	3: {
	    'filename': 'output/ch4_log_conn_sthproof_concrete_extended.png',
	    'y_label': 'Expected Cumulative Log Connections',
	    'mc_file': CH4_HONEST_MC_DIR + 'honest_newDesign_logConn_sthProof.txt',
	},
}
props_file = "props_honest_ext.props"
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
	'is_ext': True,
}
