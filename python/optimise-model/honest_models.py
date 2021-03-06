from json import loads
from prism_code_strings import honest_extended_server
from prism_code_strings import honest_original_client
from prism_code_strings import honest_original_rewards
from prism_code_strings import honest_original_server
from prism_code_strings_init import honest_init
from prism_code_strings_init import honest_original_client_init
from prism_code_strings_init import honest_original_server_init
from prism_code_strings_init import honest_extended_server_init


class HonestModels(object):

    def __init__(self, options, space, profiles):
        self.mul_init = options.mul_init
        # First, we load json data to get the python lists we want...
        connect_rates = loads(space['connect_rates'])
        client_count = loads(space['client_count'])
        client_init = loads(space['client_init'])
        server_init = loads(space['server_init'])
        # ...and finally write the strings needed to construct our PRISM files
        self.client_count = client_count
        self.connect_rates, self.profiles, self.client_init, self.server_init = \
            self.write_strings(connect_rates, profiles,
                               client_init, server_init)

    # Write all the strings as part of the PRISM code given client and server data
    def write_strings(self, connect_rates, profiles, client_init, server_init):
        bool_val = ['false', 'true']
        init_flag = True
        client_id = 1
        str_connect_rates = '//client connect rates\n'
        str_profiles = '//client profiles\n'
        str_client_init = '//initial states for each client\n'
        str_server_init = '//initial states for each server\n'
        for i in range(len(self.client_count)):
            for j in range(self.client_count[i]):
                str_connect_rates += 'prob g{id} = {gossip} ;\n'.format(
                    id=client_id, gossip=connect_rates[i])
                if init_flag and client_init[i] == 1:
                    str_client_init += 'const bool c{id}_sth_init = true;\n'.\
                        format(id=client_id)
                    init_flag = False
                else:
                    str_client_init += 'const bool c{id}_sth_init = false;\n'.\
                        format(id=client_id)
                for k in range(len(profiles[i])):
                    str_profiles += 'prob p_{id}_{s} = {probability} ;\n'.\
                        format(id=client_id, s=k+1, probability=profiles[i][k])
                str_profiles += '\n'
                client_id += 1
        for i in range(len(server_init)):
            index = server_init[i]
            str_server_init += 'const bool s{id}_init = {bool_val};\n'.\
                format(id=i+1, bool_val=bool_val[index])
        return str_connect_rates, str_profiles, str_client_init, str_server_init

    # Write PRISM models
    def write_original_model(self, filename):
        if self.mul_init:
            original_model = """dtmc
			""" + honest_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + honest_original_client_init + """
			""" + honest_original_server_init + """
			""" + honest_original_rewards
        else:
            original_model = """dtmc
			""" + self.client_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + honest_original_client + """
			""" + self.server_init + """
			""" + honest_original_server + """
			""" + honest_original_rewards

        with open(filename, 'w') as fp:
            fp.write(original_model)

    def write_extended_model(self, filename):
        if self.mul_init:
            extended_model = """dtmc
			""" + honest_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + honest_original_client_init + """
			""" + honest_extended_server_init + """
			""" + honest_original_rewards
        else:
            extended_model = """dtmc
			""" + self.client_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + honest_original_client + """
			""" + self.server_init + """
			""" + honest_extended_server + """
			""" + honest_original_rewards

        with open(filename, 'w') as fp:
            fp.write(extended_model)
