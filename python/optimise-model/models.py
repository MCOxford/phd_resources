import numpy as np

from json import loads
from scipy.spatial.distance import cosine
from itertools import combinations
from prism_code_strings import honest_extended_formulae
from prism_code_strings import honest_extended_server
from prism_code_strings import honest_original_client
from prism_code_strings import honest_original_rewards
from prism_code_strings import honest_original_server
from prism_code_strings import splitworld_extended_server
from prism_code_strings import splitworld_original_client
from prism_code_strings import splitworld_original_rewards
from prism_code_strings import splitworld_original_server
from prism_code_strings_init import honest_init
from prism_code_strings_init import split_init
from prism_code_strings_init import honest_original_client_init
from prism_code_strings_init import honest_original_server_init
from prism_code_strings_init import honest_extended_server_init
from prism_code_strings_init import splitworld_original_client_init
from prism_code_strings_init import splitworld_original_server_init
from prism_code_strings_init import splitworld_extended_server_init


class Models(object):

    ORIGINAL_FILE = 'build/original.prism'
    EXTENDED_FILE = 'build/extended.prism'

    def __init__(self, options, space, profiles):

        self.is_split = options.is_split
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
        self.original_model, self.extended_model = self.write_models()
        # Record the average connectivity and cosine distance
        self.avg_connectivity, self.avg_cosine_distance = \
            self.calculate_avg_connectivity(profiles)
        # Finally, write .prism file
        self.write_files()

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
                if self.is_split:
                    if init_flag and client_init[i] == 1:
                        str_client_init += 'const int c{id}_sth_init = 2;\n'.\
                            format(id=client_id)
                        init_flag = False
                    else:
                        str_client_init += 'const int c{id}_sth_init = 0;\n'.\
                            format(id=client_id)
                else:
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
            if self.is_split:
                str_server_init += 'const int s{id}_init = {int_val};\n'.\
                    format(id=i+1, int_val=server_init[i])
            else:
                index = server_init[i]
                str_server_init += 'const bool s{id}_init = {bool_val};\n'.\
                    format(id=i+1, bool_val=bool_val[index])
        return str_connect_rates, str_profiles, str_client_init, str_server_init

    # Write PRISM models
    def write_models(self):
        if self.is_split:
            if self.mul_init:
                original_model = """dtmc
				""" + split_init + """
				""" + self.connect_rates + """
				""" + self.profiles + """
				""" + splitworld_original_client_init + """
				""" + splitworld_original_server_init + """
				""" + splitworld_original_rewards

                extended_model = """dtmc
				""" + split_init + """
				""" + self.connect_rates + """
				""" + self.profiles + """
				""" + splitworld_original_client_init + """
				""" + splitworld_extended_server_init + """
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

                extended_model = """dtmc
				""" + self.client_init + """
				""" + self.connect_rates + """
				""" + self.profiles + """
				""" + splitworld_original_client + """
				""" + self.server_init + """
				""" + splitworld_extended_server + """
				""" + splitworld_original_rewards
        else:
            if self.mul_init:
                original_model = """dtmc
				""" + honest_init + """
				""" + self.connect_rates + """
				""" + self.profiles + """
				""" + honest_original_client_init + """
				""" + honest_original_server_init + """
				""" + honest_original_rewards

                extended_model = """dtmc
				""" + honest_init + """
				""" + self.connect_rates + """
				""" + self.profiles + """
				""" + honest_original_client_init + """
				""" + honest_extended_formulae + """
				""" + honest_extended_server_init + """
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

                extended_model = """dtmc
				""" + self.client_init + """
				""" + self.connect_rates + """
				""" + self.profiles + """
				""" + honest_original_client + """
				""" + self.server_init + """
				""" + honest_extended_formulae + """
				""" + honest_extended_server + """
				""" + honest_original_rewards

        return original_model, extended_model

    # Compute the average connectivity between each distinct client profile.
    # @remark 1 = network is 'disconnected' i.e. impossible to spread data to
    # all clients
    def calculate_avg_connectivity(self, profiles):
        cosine_distances = list()
        connectivity_values = list()
        list_types = list(range(len(self.client_count)))
        # First check if there are no partitions in the network. If there is,
        # raise an exception
        for i in list_types:
            is_partition = True
            u = np.array(profiles[i])
            for j in list_types:
                if i == j:
                    continue
                v = np.array(profiles[j])
                if u@v != 0:
                    is_partition = False
            if is_partition:
                raise Exception("Found a partition. Quitting")
        # Now find the average cosine distance
        choices = list(combinations(list_types, 2))
        for vect in choices:
            u = np.array(profiles[vect[0]])
            v = np.array(profiles[vect[1]])
            connectivity_values.append(u@v)
            cosine_distances.append(cosine(u, v))
        avg_conn = sum(connectivity_values) / len(connectivity_values)
        avg_cos = sum(cosine_distances) / len(cosine_distances)
        return avg_conn, avg_cos

    def write_files(self):
        with open(self.ORIGINAL_FILE, 'w') as fp:
            fp.write(self.original_model)
        with open(self.EXTENDED_FILE, 'w') as fp:
            fp.write(self.extended_model)
