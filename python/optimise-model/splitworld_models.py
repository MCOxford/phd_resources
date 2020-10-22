from json import loads
from prism_code_strings import splitworld_extended_server
from prism_code_strings import splitworld_original_client
from prism_code_strings import splitworld_original_rewards
from prism_code_strings import splitworld_original_server
from prism_code_strings_init import split_init
from prism_code_strings_init import splitworld_original_client_init
from prism_code_strings_init import splitworld_original_server_init
from prism_code_strings_init import splitworld_extended_server_init


class SplitworldModels(object):

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
                    str_client_init += 'const int c{id}_sth_init = 2;\n'.\
                        format(id=client_id)
                    init_flag = False
                else:
                    str_client_init += 'const int c{id}_sth_init = 0;\n'.\
                        format(id=client_id)
                for k in range(len(profiles[i])):
                    str_profiles += 'prob p_{id}_{s} = {probability} ;\n'.\
                        format(id=client_id, s=k+1, probability=profiles[i][k])
                str_profiles += '\n'
                client_id += 1
        for i in range(len(server_init)):
            str_server_init += 'const int s{id}_init = {int_val};\n'.\
                format(id=i+1, int_val=server_init[i])
        return str_connect_rates, str_profiles, str_client_init, str_server_init

    # Write PRISM models
    def write_original_model(self, filename):
        if self.mul_init:
            original_model = """dtmc
			""" + split_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + splitworld_original_client_init + """
			""" + splitworld_original_server_init + """
			""" + splitworld_original_rewards
        else:
            original_model = """dtmc
			""" + self.client_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + splitworld_original_client + """
			""" + self.server_init + """
			""" + splitworld_original_server + """
			""" + splitworld_original_rewards

        with open(filename, 'w') as fp:
            fp.write(original_model)

    def write_extended_model(self, filename):
        if self.mul_init:
            extended_model = """dtmc
			""" + split_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + splitworld_original_client_init + """
			""" + splitworld_extended_server_init + """
			""" + splitworld_original_rewards
        else:
            extended_model = """dtmc
			""" + self.client_init + """
			""" + self.connect_rates + """
			""" + self.profiles + """
			""" + splitworld_original_client + """
			""" + self.server_init + """
			""" + splitworld_extended_server + """
			""" + splitworld_original_rewards

        with open(filename, 'w') as fp:
            fp.write(extended_model)
