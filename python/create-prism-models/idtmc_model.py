from prism_model import PRISMModel

"""
Class for constructing and writing an IDTMC model compatible with PRISM. Note 
that we don't distinguish the clients by their type - one client will always
have the latest STH data.
"""
class IDTMCModel(PRISMModel):

	def __init__(self, data, num_servers, server_init, is_split, is_ext, is_sim, 
				 is_abs, file_path):

		# Do we include formulae/labels for abstraction?
		self.is_abs = is_abs

		super().__init__(data, num_servers, [0], server_init, is_split,
				 is_ext, is_sim, file_path)

	# write abstraction formulae and expressions (for non-sim normal models only)
	@property
	def abstract_expressions(self):
		abstract_expressions = ''
		updated_client_gossips = []
		nonupdated_client_gossips = []
		formula_csth = '\n'
		formula_ssth = '\n'
		csth_exp_nconnect_stg = []
		csth_exp_connect_stg = []
		ssth_exp_nconnect_stg = []
		ssth_exp_connect_stg = []
		csth_sum = []
		for i in self.data:
			formula_csth += 'formula abs_c{cid}_sth = ((c{cid}=2 & ( (!c{cid}_sth & c{cid}_connected_server_has_sth) | c{cid}_sth )) | (c{cid}!=2 & c{cid}_sth)?1:0);\n'.format(cid=i+1)
			csth_sum.append('abs_c{cid}_sth'.format(cid=i+1))
			updated_client_gossips.append('(c{cid}_sth & !c{cid}_skip)'.format(cid=i+1))
			nonupdated_client_gossips.append('(!c{cid}_sth & !c{cid}_skip)'.format(cid=i+1))
			#csth_exp_nconnect_stg.append('(c{cid}_sth?1:0)'.format(cid=i+1))
			#csth_exp_connect_stg.append('(c1=2 & ( (!c{cid}_sth & c{cid}_connected_server_has_sth) | c{cid}_sth )?1:0)'.format(cid=i+1))
			s = 'formula c{cid}_connected_server_has_sth = '.format(cid=i+1)
			tmp = []
			for j in range(1, self.num_servers + 1):
				tmp.append('(c{cid}s={sid} & s{sid}_sth)'.format(cid=i+1, sid=j))
			s += '|'.join(tmp)
			abstract_expressions += s + ';\n'
		abstract_expressions += 'formula updated_client_gossips = ' + '|'.join(updated_client_gossips) + ';\n'
		abstract_expressions += 'formula nonupdated_client_gossips = ' + '|'.join(nonupdated_client_gossips) + ';\n'
		for j in range(1, self.num_servers+1):
			formula_ssth += 'formula abs_s{sid}_sth = 0 + '.format(sid=j)
			s1 = '(s{sid}_sth?1:0)'.format(sid=j+1)
			s2 = '(c1=2 & ( (!s{sid}_sth & s{sid}_connected_client_has_sth) | s{sid}_sth )?1:0) '.format(sid=j)
			s3 = 'formula s{sid}_connected_client_has_sth = '.format(sid=j)
			tmp = []
			for i in self.data:
				tmp.append('(c{cid}s={sid} & c{cid}_sth)'.format(cid=i+1, sid=j))
			s3 += '|'.join(tmp)
			abstract_expressions += s3 + ';\n'
			formula_ssth += '( ( c1!=2 & s{sid}_sth ) | ( c1=2 & (!s{sid}_sth & s{sid}_connected_client_has_sth) | s{sid}_sth )?1:0);\n'.format(sid=j)
		#formula_csth += '(c1!=2?' + '+'.join(csth_exp_nconnect_stg) + ':0) +\n\t\t' + ' +\n\t\t'.join(csth_exp_connect_stg) + ';\n'
		abstract_expressions += formula_csth + formula_ssth + '\n'
		abstract_expressions += 'formula abs_stage = 0 + (c1=1 & updated_client_gossips & !nonupdated_client_gossips?1:0) +\n'
		abstract_expressions +=	'(c1=1 & !updated_client_gossips & nonupdated_client_gossips?2:0) +\n' 
		abstract_expressions += '(c1=1 & updated_client_gossips & nonupdated_client_gossips?3:0) +\n' 
		abstract_expressions += '(c1=1 & !updated_client_gossips & !nonupdated_client_gossips?4:0) +\n'
		abstract_expressions += '(c1=2?5:0) +\n'
		abstract_expressions += '(c1=3?6:0) +\n' 
		abstract_expressions += '(c1=4?7:0);\n\n'
		abstract_expressions += 'label "abs_t" = ' + '+'.join(csth_sum) + '={size} & abs_stage>=6;\n\n'.format(size=len(self.data))
		return abstract_expressions

	# write connect rate strings for each client
	@property
	def connect_rates(self):
		connect_rates = ''
		for i in self.data:
			s1 = 'prob g{cid}_L = {cr};\n'.\
				format(cid=i+1, cr=self.data[i]['GOSSIP_RATE'][0])
			s2 = 'prob g{cid}_H = {cr};\n'.\
				format(cid=i+1, cr=self.data[i]['GOSSIP_RATE'][1])
			connect_rates += s1 + s2
		return connect_rates + '\n'

	# write profile strings for each client
	@property
	def profiles(self):
		profiles = ''
		for i in self.data:
			for j in range(self.num_servers):
				s1 = 'prob p_{cid}_{sid}_L = {p};\n'.\
					format(cid=i+1, sid=j+1, p=self.data[i]['PROFILE'][j][0])
				s2 = 'prob p_{cid}_{sid}_H = {p};\n'.\
					format(cid=i+1, sid=j+1, p=self.data[i]['PROFILE'][j][1])
				profiles += s1 + s2
			profiles += '\n'
		return profiles

	# write initial STH state strings of each client
	@property
	def client_sth_init(self):
		client_sth_init = ''
		for i in self.data:
			if i == len(self.data)-1:
				if self.is_split:
					s = 'const int c{cid}_sth_init = 2;\n'.format(cid=i+1)
				else:
					s = 'const bool c{cid}_sth_init = true;\n'.format(cid=i+1)
				client_sth_init += s
			else:
				if self.is_split:
					s = 'const int c{cid}_sth_init = 0;\n'.format(cid=i+1)
				else:
					s = 'const bool c{cid}_sth_init = false;\n'.format(cid=i+1)
				client_sth_init += s
		return client_sth_init + '\n'

	# write action string for [choose]
	@property
	def choose(self):
		choose = ''
		for i in range(1, self.num_servers+1):
			if self.is_sim:
				s = """[p_1_{sid}_L, p_1_{sid}_H] : (c1_flag'=true)&(c1'=2)&(c1s'={sid})""".\
					format(sid=i)
			else:
				s = """[p_1_{sid}_L, p_1_{sid}_H] : (c1'=2)&(c1s'={sid})""".format(sid=i)
			choose += s
			if i < self.num_servers:
				choose += ' +\n\t\t\t\t\t '
			else:
				choose += ';'
		return choose

	# Write client modules via relabelling
	@property
	def client_modules(self):
		client_modules = ''
		for i in self.data:
			if i != 0:
				client_modules += 'module Client{cid}=Client1['.format(cid=i+1)
				for j in range(1, self.num_servers+1):
					client_modules += 'p_1_{sid}_L=p_{cid}_{sid}_L,'.\
						format(sid=j, cid=i+1)
					client_modules += 'p_1_{sid}_H=p_{cid}_{sid}_H,'.\
						format(sid=j, cid=i+1)
				client_modules += '\n'
				client_modules += 'g1_L=g{cid}_L,\n'.format(cid=i+1)
				client_modules += 'g1_H=g{cid}_H,\n'.format(cid=i+1)
				client_modules += 'c1=c{cid},\n'.format(cid=i+1)
				client_modules += 'c1s=c{cid}s,\n'.format(cid=i+1)
				client_modules += 'c1_sth=c{cid}_sth,\n'.format(cid=i+1)
				client_modules += 'c{cid}_sth=c1_sth,\n'.format(cid=i+1)
				client_modules += 'c1_skip=c{cid}_skip,\n'.format(cid=i+1)
				if self.is_split:
					client_modules += 'c1d=c{cid}d, c{cid}d=c1d,\n'.\
						format(cid=i+1)
				if self.is_sim:
					client_modules += 'c1_flag=c{cid}_flag, c0_flag=c{cidn}_flag,\n'.\
						format(cid=i+1, cidn=i)
				client_modules += 'c1_sth_init = c{cid}_sth_init'.\
					format(cid=i+1)
				client_modules += '] endmodule\n\n'
		return client_modules

	""" We don't write rewards formulae for IDTMCs - rewards-based model checking
	not compatible with IDTMCs at the moment"""
	@property
	def rewards(self):
		pass

	# Write .prism file to given file path
	def write_file(self):
		total = len(self.data)
		file = 'dtmc\n\n'
		if self.is_abs and not self.is_split:
			file += self.abstract_expressions
		else:
			print('Writing abstraction not possible with chosen options. Only compatible with non-sim normal models.')
		if self.is_sim:
			file += 'const bool c0_flag = true;\n\n'
		file += self.client_sth_init
		file += self.connect_rates
		file += self.profiles
		file += 'module Client1\n\n'
		file += '\tc1 : [0..4] init 0;\n'.format(c1s=self.c1s)
		file += '\tc1s : {c1s} init 0;\n'.format(c1s=self.c1s)
		if self.is_split:
			file += '\tc1_sth : [0..2] init c1_sth_init;\n'
			file += '\tc1d : bool init false;\n'
		else:
			file += '\tc1_sth : bool init c1_sth_init;\n'
		file += '\tc1_skip : bool init false;\n'
		if self.is_sim:
			file += '\tc1_flag : bool init false;\n\n'
			file += """\t[] c0_flag & c1=0 -> [g1_L, g1_H] : (c1'=1) + [1-g1_H, 1-g1_L] : (c1'=1) & (c1_skip'=true);\n"""
			file += '\t[] c0_flag & c1_skip=false & c1=1 -> {choose}\n'.format(choose=self.choose)
			file += """\t[] c0_flag & c1_skip=true & c1=1 -> (c1_flag'=true)&(c1'=2);\n"""
		else:
			file += """\t[connect] c1=0 -> [g1_L, g1_H] : (c1'=1) + [1-g1_H, 1-g1_L] : (c1'=1) & (c1_skip'=true);\n"""
			file += '\t[choose] c1_skip=false & c1=1 -> {choose}\n'.format(choose=self.choose)
			file += """\t[choose] c1_skip=true & c1=1-> (c1'=2);\n"""
		if self.is_split:
			if self.is_sim:
				file += """\t[update] serverg & !c1_skip & c1=2 & s_data_ok -> (c1_sth'=c_update) & (c1'=3);\n"""
				file += """\t[update] serverg & !c1_skip & c1=2 & !s_data_ok -> (c1d'=true) & (c1'=3);\n"""
				file += """\t[update] serverg & c1_skip & c1=2 -> (c1'=3);\n"""
				file += """\t[round_complete] c1=3 & !detect -> (c1'=0) & (c1s'=0) & (c1_skip'=false) & (c1_flag'=false);\n"""
			else:
				file += """\t[update] !c1_skip & c1=2 & s_data_ok -> (c1_sth'=c_update) & (c1'=3);\n"""
				file += """\t[update] !c1_skip & c1=2 & !s_data_ok -> (c1d'=true) & (c1'=3);\n"""
				file += """\t[update] c1_skip & c1=2 -> (c1'=3);\n"""
				file += """\t[round_complete] c1=3 & !detect -> (c1'=0) & (c1s'=0) & (c1_skip'=false);\n"""
			file += """\t[round_complete] c1=3 & detect -> (c1'=4) & (c1s'=0) & (c1_skip'=false);\n"""
		else:
			if self.is_sim:
				file += """\t[update] serverg & c{total}_flag & !c1_skip & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);\n""".format(total=total)
				file += """\t[update] serverg & c{total}_flag & c1=2 & ((!c1_skip & !connected_server_has_sth) | c1_skip) -> (c1'=3);\n""".format(total=total)
				file += """\t[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false) & (c1_flag'=false);\n"""
			else:
				file += """\t[update] !c1_skip & c1=2 & connected_server_has_sth  -> (c1'=3) & (c1_sth'=true);\n""".format(total=total)
				file += """\t[update] c1=2 & ((!c1_skip & !connected_server_has_sth) | c1_skip) -> (c1'=3);\n""".format(total=total)
				file += """\t[round_complete] c1=3 & !clients_all_updated -> (c1'=0) & (c1s'=0) & (c1_skip'=false);\n"""
			file += """\t[round_complete] c1=3 & clients_all_updated -> (c1'=4);\n"""
		file += """\t[END] c1=4 -> true;\n\nendmodule\n\n"""
		file += self.client_formulae
		if self.is_split:
			file += 'formula s_data_ok = pr_req_successful & !warn_msg;\n'
		file += self.client_modules
		if self.is_sim:
			if self.is_split:
				if self.is_ext:
					file += 'const int sf_init = 0;\n\n'
				else:
					file += 'const int sf_init = 2;\n\n'
			else:
				if self.is_ext:
					file += 'const bool sf_init = false;\n\n'
				else:
					file += 'const bool sf_init = true;\n\n'
		file += self.server_numbers
		file += self.server_sth_init
		if self.is_ext:
			server_IE = self.server_IE
			file += server_IE
		file += 'module Server1\n\n'
		if self.is_split:
			file += '\ts1_sth : [0..2] init s1_init;\n'
			file += '\ts1d : bool init false;\n'
			if self.is_sim:
				file += '\ts1_flag : [0..2] init sf_init;\n\n'
		else:
			file += '\ts1_sth : bool init s1_init;\n'
			if self.is_sim:
				file += '\ts1_flag : bool init sf_init;\n\n'
		if self.is_split:
			file += """\t[update] !s1d & c_data_ok -> (s1_sth'=s_update);\n"""
			file += """\t[update] !s1d & !c_data_ok -> (s1d'=true) & (s1_sth'=0);\n"""
			file += """\t[update] s1d -> true;\n"""
			if self.is_ext:
				if self.is_sim:
					file += """\t[spread1] !detect & s1_flag=0 & !s1d & s1_sth=0 -> get_real_data : (s1_sth'=1) & (s1_flag'=1) + 1-get_real_data : (s1_flag'=1);\n"""
					file += """\t[spread1] !detect & s1_flag=0 & !s1d & s1_sth=1 -> (s1_flag'=1);\n"""
					file += """\t[spread1] !detect & s1_flag=0 & !s1d & s1_sth=2 -> get_real_data : (s1d'=true) & (s1_sth'=0) & (s1_flag'=1) + 1-get_real_data : (s1_flag'=1);\n"""
					file += """\t[spread1] !detect & s1_flag=0 & s1d -> (s1_flag'=1);\n"""
					file += """\t[spread2] s1_flag=1 & !s1d & s1_sth=0 -> get_fake_data : (s1_sth'=2) & (s1_flag'=2)  + 1-get_fake_data : (s1_flag'=2);\n"""
					file += """\t[spread2] s1_flag=1 & !s1d & s1_sth=1 -> get_fake_data : (s1d'=true) & (s1_sth'=0) & (s1_flag'=2) + 1-get_fake_data : (s1_flag'=2);\n"""
					file += """\t[spread2] s1_flag=1 & !s1d & s1_sth=2 -> (s1_flag'=2);\n"""
					file += """\t[spread2] s1_flag=1 & s1d -> (s1_flag'=2);\n"""
					file += """\t[round_complete] true -> get_message : (s1d'=true) & (s1_sth'=0) & (s1_flag'=sf_init) + 1-get_message : (s1_flag'=sf_init);\n"""
				else:
					file += """\t[connect] !detect & !s1d & s1_sth=0 -> get_real_data : (s1_sth'=1) + 1-get_real_data : true;\n"""
					file += """\t[connect] !detect & !s1d & s1_sth=1 -> true;\n"""
					file += """\t[connect] !detect & !s1d & s1_sth=2 -> get_real_data : (s1d'=true) & (s1_sth'=0) + 1-get_real_data : true;\n"""
					file += """\t[connect] !detect & s1d -> true;\n"""
					file += """\t[choose] !s1d & s1_sth=0 -> get_fake_data : (s1_sth'=2) + 1-get_fake_data : true;\n"""
					file += """\t[choose] !s1d & s1_sth=1 -> get_fake_data : (s1d'=true) & (s1_sth'=0) + 1-get_fake_data : true;\n"""
					file += """\t[choose] !s1d & s1_sth=2 -> true;\n"""
					file += """\t[choose] s1d -> true;\n"""
					file += """\t[round_complete] true -> get_message : (s1d'=true) & (s1_sth'=0) + 1-get_message : true;\n"""
		else:
			file += """\t[update] !s1_sth & connected_client_has_sth -> (s1_sth'=true);\n"""
			file += """\t[update] s1_sth | (!s1_sth & !connected_client_has_sth) -> true;\n"""
			if self.is_ext:
				if self.is_sim:
					file += """\t[spread] !clients_all_updated & !s1_flag & !s1_sth -> get_data : (s1_sth'=true)&(s1_flag'=true) + 1-get_data : (s1_flag'=true);\n"""
					file += """\t[spread] !clients_all_updated & !s1_flag & s1_sth -> (s1_flag'=true);\n"""
					file += """\t[round_complete] true -> (s1_flag'=sf_init);\n"""
				else:
					file += """\t[connect] !clients_all_updated & !s1_sth -> get_data : (s1_sth'=true)+ 1-get_data : true;\n"""
					file += """\t[connect] !clients_all_updated & s1_sth -> true;\n"""
		file += '\t[END] true -> true;\n\n'
		file += 'endmodule\n\n'
		file += self.server_formulae
		if self.is_split:
			file += 'formula c_data_ok = !server_pr_req_fail & !pairwise_inconsistency;\n'
		file += self.server_modules
		with open(self.file_path, 'w') as f:
			f.write(file)
		print('prism file saved to {path}.'.format(path=self.file_path))
	
