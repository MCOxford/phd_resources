from prism_model import PRISMModel
from idtmc_model import IDTMCModel
from data_simple import data
from imc_data_simple import imc_data

if __name__ == '__main__':

	# Simple DTMC model
	num_servers = len(data[0]['PROFILE'])
	client_init_simple = [1,0]
	server_init_simple = [1,0]
	is_split = False
	is_ext = False
	is_sim = False
	is_abs = True
	file_path_simple = 'demo_model_simple.pm'
	pm = PRISMModel(data, num_servers, client_init_simple, 
					server_init, is_split, is_ext, 
					is_sim, file_path_simple)
	pm.write_file()

	# Simple IDTMC model
	num_servers = len(imc_data[0]['PROFILE'])
	server_init = [1,0,0,0,0]
	file_path_imc = 'demo_model_imc.pm'
	qm = IDTMCModel(imc_data, num_servers, server_init,
					is_split, is_ext, is_sim, is_abs, 
					file_path_imc)
	qm.write_file()
