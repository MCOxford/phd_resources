from itertools import combinations


class PRISMModel(object):

	def __init__(self, data, num_servers, client_init, server_init, is_split,
				 is_ext, is_sim, file_path):

		# Client data
		self.data = data

		# Number of servers in the network
		self.num_servers = num_servers

		# Client initial setup information
		self.client_init = client_init

		# Server initial setup information
		self.server_init = server_init

		# Are we modelling a split-world situation?
		self.is_split = is_split

		# Do we allow server gossip?
		self.is_ext = is_ext

		# Do we create a simulator-compatible version of the model?
		self.is_sim = is_sim

		# file path to write PRISM model to
		self.file_path = file_path
	
	# write connect rate strings for each client
	@property
	def connect_rates(self):
		connect_rates = ''
		for i in self.data:
			s = 'prob g{cid} = {cr};\n'.\
				format(cid=i+1, cr=self.data[i]['GOSSIP_RATE'])
			connect_rates += s
		return connect_rates + '\n'

	# write profile strings for each client
	@property
	def profiles(self):
		profiles = ''
		for i in self.data:
			for j in range(self.num_servers):
				s = 'prob p_{cid}_{sid} = {p};\n'.\
					format(cid=i+1, sid=j+1, p=self.data[i]['PROFILE'][j])
				profiles += s
			profiles += '\n'
		return profiles

	# write initial STH state strings of each client
	@property
	def client_sth_init(self):
		update_count = [0]*len(self.client_init)
		client_sth_init = ''
		for i in self.data:
			ind = self.data[i]["TYPE"]-1
			if update_count[ind] < self.client_init[ind]:
				if self.is_split:
					s = 'const int c{cid}_sth_init = 2;\n'.format(cid=i+1)
				else:
					s = 'const bool c{cid}_sth_init = true;\n'.format(cid=i+1)
				client_sth_init += s
				update_count[ind] += 1
			else:
				if self.is_split:
					s = 'const int c{cid}_sth_init = 0;\n'.format(cid=i+1)
				else:
					s = 'const bool c{cid}_sth_init = false;\n'.format(cid=i+1)
				client_sth_init += s
		return client_sth_init + '\n'

	# returns c1s
	@property
	def c1s(self):
		return '[0..{total}]'.format(total=self.num_servers)

	# write action string for [choose]
	@property
	def choose(self):
		choose = ''
		for i in range(1, self.num_servers+1):
			if self.is_sim:
				s = """p_1_{sid} : (c1_flag'=true)&(c1'=2)&(c1s'={sid})""".\
					format(sid=i)
			else:
				s = """p_1_{sid} : (c1'=2)&(c1s'={sid})""".format(sid=i)
			choose += s
			if i < self.num_servers:
				choose += ' +\n\t\t\t\t\t '
			else:
				choose += ';'
		return choose

	# returns client formulae
	@property
	def client_formulae(self):
		tmp = []
		tmps = []
		client_formulae = ''
		if self.is_split:
			formulae1 = 'formula pr_req_successful = '
			formulae2 = 'formula warn_msg = '
			formulae3 = 'formula c_update = c1_sth + '
			formulae4 = 'formula detect = '
			if self.is_sim:
				formulae5 = 'formula serverg = '
			label = 'label "detect" = '
			for i in range(1, self.num_servers+1):
				s1 = '(c1s={sid} & s{sid}_sth+c1_sth!=3)'.format(sid=i)
				s2 = '(c1s={sid} & s{sid}d)'.format(sid=i)
				s3 = '((c1s={sid} & s{sid}_sth>c1_sth)?s{sid}_sth-c1_sth:0)'.\
					format(sid=i)
				formulae1 += s1
				formulae2 += s2
				formulae3 += s3
				if self.is_sim:
					tmps.append('s{sid}_flag=2'.format(sid=i))
				if i < self.num_servers:
					formulae1 += ' | '
					formulae2 += ' | '
					formulae3 += ' + '
				else:
					formulae1 += ';\n\n'
					formulae2 += ';\n\n'
					formulae3 += ';\n\n'
			for i in self.data:
				tmp.append('c{cid}d'.format(cid=i+1))
			detect = ' | '.join(tmp)
			formulae4 += detect + ';\n\n'
			label += detect + ';\n\n'
			if self.is_sim:
				s5 = ' & '.join(tmps)
				formulae5 += s5 + ';\n\n'
				client_formulae += formulae1 + formulae2 + formulae3 + \
					formulae4 + formulae5 + label
			else:
				client_formulae += formulae1 + formulae2 + formulae3 + \
					formulae4 + label
		else:
			client_formulae = 'formula connected_server_has_sth = ('
			for i in range(1, self.num_servers+1):
				if self.is_sim:
					tmps.append('s{sid}_flag'.format(sid=i))
				s = '(c1s={sid} & s{sid}_sth)'.format(sid=i)
				client_formulae += s
				if i < self.num_servers:
					client_formulae += ' | '
				else:
					client_formulae += ');\n'
			client_formulae += 'formula clients_all_updated = '
			for i in self.data:
				tmp.append('c{cid}_sth'.format(cid=i+1))
			s = '&'.join(tmp)
			client_formulae += s + ';\n'
			client_formulae += 'label "clients_all_updated" = ' + s + ';\n'
			if self.is_sim:
				client_formulae += 'formula serverg = '
				client_formulae += ' & '.join(tmps) + ';\n'
		return client_formulae + '\n\n'

	# Write client modules via relabelling
	@property
	def client_modules(self):
		client_modules = ''
		for i in self.data:
			if i != 0:
				client_modules += 'module Client{cid}=Client1['.format(cid=i+1)
				for j in range(1, self.num_servers+1):
					client_modules += 'p_1_{sid}=p_{cid}_{sid},'.\
						format(sid=j, cid=i+1)
				client_modules += '\n'
				client_modules += 'g1=g{cid},\n'.format(cid=i+1)
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

	# Write constants for server identification
	@property
	def server_numbers(self):
		server_numbers = ''
		for i in range(1, self.num_servers+1):
			server_numbers += 'const int SERVER{sid} = {sid};\n'.format(sid=i)
		return server_numbers + '\n'

	# Write server initial states
	@property
	def server_sth_init(self):
		server_sth_init = ''
		for i in range(1, self.num_servers+1):
			if self.server_init[i-1] == 1:
				if self.is_split:
					s = 'const int s{sid}_init = 1;\n'.format(sid=i)
				else:
					s = 'const bool s{sid}_init = true;\n'.format(sid=i)
				server_sth_init += s
			else:
				if self.is_split:
					s = 'const int s{sid}_init = 0;\n'.format(sid=i)
				else:
					s = 'const bool s{sid}_init = false;\n'.format(sid=i)
				server_sth_init += s
		return server_sth_init + '\n'

	# Write I-E formula for server gossip NB: probability fixed to 0.2
	@property
	def server_IE(self):
		server_IE = ''
		formula = 'formula get_data = '
		formula_r = 'formula get_real_data = '
		formula_f = 'formula get_fake_data = '
		formula_m = 'formula get_message = '
		lst = [str(i) for i in range(1, self.num_servers+1)]
		for i in range(1, self.num_servers+1):
			comb = list(combinations(lst, i))
			s = 'formula ch{i} = '.format(i=i)
			real = 'formula real_{num_s}c{ch} = '.format(num_s=self.num_servers, ch=i)
			fake = 'formula fake_{num_s}c{ch} = '.format(num_s=self.num_servers, ch=i)
			mssg = 'formula mssg_{num_s}c{ch} = '.format(num_s=self.num_servers, ch=i)
			if i%2 == 0 and i < self.num_servers:
				formula += 'ch{i} + '.format(i=i)
				formula_r += 'real_{num_s}c{ch} + '.format(num_s=self.num_servers, ch=i)
				formula_f += 'fake_{num_s}c{ch} + '.format(num_s=self.num_servers, ch=i)
				formula_m += 'mssg_{num_s}c{ch} + '.format(num_s=self.num_servers, ch=i)
			elif i%2 == 1 and i < self.num_servers:
				formula += 'ch{i} - '.format(i=i)
				formula_r += 'real_{num_s}c{ch} - '.format(num_s=self.num_servers, ch=i)
				formula_f += 'fake_{num_s}c{ch} - '.format(num_s=self.num_servers, ch=i)
				formula_m += 'mssg_{num_s}c{ch} - '.format(num_s=self.num_servers, ch=i)
			else:
				formula += 'ch{i};\n'.format(i=i)
				formula_r += 'real_{num_s}c{ch};\n'.format(num_s=self.num_servers, ch=i)
				formula_f += 'fake_{num_s}c{ch};\n'.format(num_s=self.num_servers, ch=i)
				formula_m += 'mssg_{num_s}c{ch};\n'.format(num_s=self.num_servers, ch=i)
			for j in range(len(comb)):
				tmp1 = []
				tmpr = []
				tmpf = []
				tmpm = []
				for k in range(len(comb[j])):
					if self.is_split:
						tmpr.append('(s{sid}_sth=1?1/5:0)'.format(sid=comb[j][k]))
						tmpf.append('(s{sid}_sth=2?1/5:0)'.format(sid=comb[j][k]))
						tmpm.append('(s{sid}d?1/5:0)'.format(sid=comb[j][k]))
					else:
						tmp1.append('(s{sid}_sth?1/5:0)'.format(sid=comb[j][k]))
				if self.is_split:
					real += '*'.join(tmpr)
					fake += '*'.join(tmpf)
					mssg += '*'.join(tmpm)
				else:
					s += '*'.join(tmp1)
				if j < len(comb) - 1:
					if self.is_split:
						real += ' +\n'
						fake += ' +\n'
						mssg += ' +\n'
					else:
						s += ' +\n'
				else:
					if self.is_split:
						real += ';\n'
						fake += ';\n'
						mssg += ';\n'
					else:
						s += ';\n'
			if self.is_split:
				server_IE += real + fake + mssg
			else:
				server_IE += s
		if self.is_split:
			server_IE += '\n' + formula_r + formula_f + formula_m
		else:
			server_IE += '\n' + formula
		return server_IE + '\n'

	# Write server formulae
	@property
	def server_formulae(self):
		tmp = []
		tmp1 = []
		tmp2 = []
		tmp3 = []
		server_formulae = ''
		if self.is_split:
			server_req_fail = 'formula server_pr_req_fail = '
			pairwise_inconsistency = 'formula pairwise_inconsistency = ('
			server_update = 'formula s_update = s1_sth + max('
			for i in self.data:
				tmp.append('(c{cid}s=SERVER1 & c{cid}_sth+s1_sth=3)'.
						   format(cid=i+1))
				tmp1.append('(c{cid}s=SERVER1 & c{cid}_sth=1)'.format(cid=i+1))
				tmp2.append('(c{cid}s=SERVER1 & c{cid}_sth=2)'.format(cid=i+1))
				tmp3.append('(c{cid}s=SERVER1 & c{cid}_sth>s1_sth?c{cid}_sth-s1_sth:0)'.
							format(cid=i+1))
			a = ' | '.join(tmp)
			b = ' | '.join(tmp1)
			c = ' | '.join(tmp2)
			d = ','.join(tmp3)
			server_req_fail += a + ';\n\n'
			pairwise_inconsistency += b + ') & (' + c + ');\n\n'
			server_update += d + ');\n\n'
			server_formulae += server_req_fail + pairwise_inconsistency + \
				server_update
		else:
			server_formulae += 'formula connected_client_has_sth = ('
			for i in self.data:
				tmp.append('(c{cid}s=SERVER1 & c{cid}_sth)'.format(cid=i+1))
			s = ' | '.join(tmp)
			server_formulae += s + ');\n\n'

		return server_formulae + '\n'

	# Write server modules via relabelling
	@property
	def server_modules(self):
		server_modules = ''
		for i in range(1, self.num_servers+1):
			if i != 1:
				server_modules += 'module Server{sid}=Server1['.format(sid=i)
				server_modules += 's1_sth=s{sid}_sth,s{sid}_sth=s1_sth,'.\
					format(sid=i)
				server_modules += 'SERVER1=SERVER{sid},'.format(sid=i)
				if self.is_split:
					server_modules += 's1d=s{sid}d,s{sid}d=s1d,'.format(sid=i)
				if self.is_sim:
					server_modules += 's1_flag=s{sid}_flag,'.\
						format(sid=i)
				server_modules += 's1_init=s{sid}_init'.format(sid=i)
				server_modules += '] endmodule\n'
		return server_modules + '\n'

	# Write rewards formulae
	@property
	def rewards(self):
		rewards = ''
		client_getConsistency_STHOnly = ''
		log_connections_STHOnly = 'formula log_connections_STHOnly = '
		client_getConsistency_STHAndProof = ''
		log_connections_STHAndProof = 'formula log_connections_STHAndProof = '
		if self.is_split:
			tmpo = []
			tmpr = []
			tmpf = []
			tmp1 = []
			tmp2 = []
			clients_old = 'formula no_clients_old = '
			clients_real = 'formula no_clients_real = '
			clients_fake = 'formula no_clients_fake = '
			for i in self.data:
				tmp1.append('(client{cid}_getConsistency_STHOnly?1:0)'.
							format(cid=i+1))
				tmp2.append('(client{cid}_getConsistency_STHAndProof?1:0)'.
							format(cid=i+1))
				tmpo.append('(c{cid}_sth=0?f:0)'.format(cid=i+1))
				tmpr.append('(c{cid}_sth=1?f:0)'.format(cid=i+1))
				tmpf.append('(c{cid}_sth=2?f:0)'.format(cid=i+1))
				client_getConsistency_STHOnly += 'formula client{cid}_getConsistency_STHOnly = c{cid}_skip=false & c{cid}=2 & ('.format(cid=i+1)
				client_getConsistency_STHAndProof += 'formula client{cid}_getConsistency_STHAndProof = c{cid}_skip=false & c{cid}=2 & ('.format(cid=i+1)
				for j in range(1,self.num_servers+1):
					client_getConsistency_STHOnly += '(c{cid}s={sid} & c{cid}_sth!=s{sid}_sth)'.format(cid=i+1, sid=j)
					client_getConsistency_STHAndProof += '(c{cid}s={sid} & (c{cid}_sth>s{sid}_sth | (c{cid}_sth=1 & s{sid}_sth=2)))'.format(cid=i+1, sid=j)
					if j < self.num_servers:
						client_getConsistency_STHOnly += ' | '
						client_getConsistency_STHAndProof += ' | '
					else:
						client_getConsistency_STHOnly += ');\n'
						client_getConsistency_STHAndProof += ');\n'
			clients_old += '+'.join(tmpo) + ';\n\n'
			clients_real += '+'.join(tmpr) + ';\n\n'
			clients_fake += '+'.join(tmpf) + ';\n\n'
			log_connections_STHOnly += '+'.join(tmp1) + ';\n\n'
			log_connections_STHAndProof += '+'.join(tmp2) + ';\n\n'
			logConn1 = client_getConsistency_STHOnly + '\n' + \
				log_connections_STHOnly
			logConn2 = client_getConsistency_STHAndProof + '\n' + \
				log_connections_STHAndProof
			rewards = clients_old + clients_real + clients_fake + \
				logConn1 + logConn2
		else:
			no_clients_updated = 'formula no_clients_updated = '
			tmp = []
			tmp1 = []
			tmp2 = []
			for i in self.data:
				tmp.append('(c{cid}_sth?f:0)'.format(cid=i+1))
				tmp1.append('(client{cid}_getConsistency_STHOnly?1:0)'.
							format(cid=i+1))
				tmp2.append('(client{cid}_getConsistency_STHAndProof?1:0)'.
							format(cid=i+1))
				client_getConsistency_STHOnly += 'formula client{cid}_getConsistency_STHOnly = c{cid}_skip=false & c{cid}=2 & ('.format(cid=i+1)
				client_getConsistency_STHAndProof += 'formula client{cid}_getConsistency_STHAndProof = c{cid}_skip=false & c{cid}=2 & ('.format(cid=i+1)
				for j in range(1,self.num_servers+1):
					client_getConsistency_STHOnly += '(c{cid}s={sid} & c{cid}_sth!=s{sid}_sth)'.format(cid=i+1, sid=j)
					client_getConsistency_STHAndProof += '(c{cid}s={sid} & c{cid}_sth & !s{sid}_sth)'.format(cid=i+1, sid=j)
					if j < self.num_servers:
						client_getConsistency_STHOnly += ' | '
						client_getConsistency_STHAndProof += ' | '
					else:
						client_getConsistency_STHOnly += ');\n'
						client_getConsistency_STHAndProof += ');\n'
			no_clients_updated += '+'.join(tmp) + ';\n\n'
			log_connections_STHOnly += '+'.join(tmp1) + ';\n\n'
			log_connections_STHAndProof += '+'.join(tmp2) + ';\n\n'
			logConn1 = client_getConsistency_STHOnly + '\n' + \
				log_connections_STHOnly
			logConn2 = client_getConsistency_STHAndProof + '\n' + \
				log_connections_STHAndProof
			rewards = no_clients_updated + logConn1 + logConn2
		return rewards

	# Write .prism file to given file path
	def write_file(self):
		total = len(self.data)
		file = 'dtmc\n\n'
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
			file += """\t[] c0_flag & c1=0 -> g1 : (c1'=1) + 1-g1 : (c1'=1) & (c1_skip'=true);\n"""
			file += '\t[] c0_flag & c1_skip=false & c1=1 -> {choose}\n'.format(choose=self.choose)
			file += """\t[] c0_flag & c1_skip=true & c1=1 -> (c1_flag'=true)&(c1'=2);\n"""
		else:
			file += """\t[connect] c1=0 -> g1 : (c1'=1) + 1-g1 : (c1'=1) & (c1_skip'=true);\n"""
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
		file += 'const double f = 1/{total};\n\n'.format(total=total)
		file += self.rewards
		file += """rewards "rounds"\n"""
		file += '\ttrue : 1/4;\n'
		file += 'endrewards\n\n'
		file += """rewards "log_connections_STHOnly"\n"""
		if self.is_sim:
			file += '\t[update] true : log_connections_STHOnly;\n'
		else:
			file += '\ttrue : log_connections_STHOnly;\n'
		file += 'endrewards\n\n'
		file += """rewards "log_connections_STHAndProof"\n"""
		if self.is_sim:
			file += '\t[update] true : log_connections_STHAndProof;\n'
		else:
			file += '\ttrue : log_connections_STHAndProof;\n'
		file += 'endrewards\n\n'
		if self.is_split:
			file += """rewards "client_proportion_old"\n"""
			file += '\ttrue : no_clients_old;\n'
			file += 'endrewards\n\n'
			file += """rewards "client_proportion_real"\n"""
			file += '\ttrue : no_clients_real;\n'
			file += 'endrewards\n\n'
			file += """rewards "client_proportion_fake"\n"""
			file += '\ttrue : no_clients_fake;\n'
			file += 'endrewards'
		else:
			file += """rewards "client_proportion"\n"""
			file += '\ttrue : no_clients_updated;\n'
			file += 'endrewards'
		with open(self.file_path, 'w') as f:
			f.write(file)
		#print('prism file saved to {path}.'.format(path=self.file_path))