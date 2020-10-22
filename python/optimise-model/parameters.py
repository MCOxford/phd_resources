from hyperopt import hp
from utilities import normalise

class BaseParameters(object):
    # Gossiping rate for each type. control variable.
    connect_rate = ['[0.5,0.5,0.5]']

    """
    interval probabilities for different client types. Modify as you see fit.
    Each key (i.e. the client type) must be numbered from 0 to N-1. Each value
    (i.e. the probability intervals) must be of the form
    {'s_1' : [l_1, u_1], ... , 's_{M}' : [l_{M}, u_{M}]}
    """
    # ---------------------------------------------------------------------
    """distributions = {
        '0': {
            's_1': [0.01, 0.1],
            's_2': [0.2, 0.4],
            's_3': [0.2, 0.3],
            's_4': [0.3, 0.4],
            's_5': [0, 0.29]
        },
        '1': {
            's_1': [0.01, 0.1],
            's_2': [0.2, 0.39],
            's_3': [0.4, 0.5],
            's_4': [0.2, 0.3],
            's_5': [0, 0.19]
        },
        '2': {
            's_1': [0.01, 0.1],
            's_2': [0.2, 0.4],
            's_3': [0.15, 0.25],
            's_4': [0.15, 0.25],
            's_5': [0, 0.49]
        },
    }"""
    distributions = {
        '0': {
            's_1': [0.3, 0.4],
            's_2': [0.04, 0.3],
            's_3': [0.02, 0.2],
            's_4': [0.02, 0.3],
            's_5': [0.07, 0.15]
        },
        '1': {
            's_1': [0.2, 0.25],
            's_2': [0.2, 0.25],
            's_3': [0.05, 0.1],
            's_4': [0.05, 0.25],
            's_5': [0.3, 0.35]
        },
        '2': {
            's_1': [0.02, 0.1],
            's_2': [0.05, 0.3],
            's_3': [0.03, 0.3],
            's_4': [0.1, 0.3],
            's_5': [0.2, 0.4]
        },
    }
    # ---------------------------------------------------------------------

    # variables we want to vary
    client_count = ['[1,1,3]', '[1,2,2]', '[1,3,1]',
                    '[2,1,2]', '[2,2,1]', '[3,1,1]']

    """Surrogate parameters. By design, optimisers choose within the half-open
    interval [0,1)"""
    type_one = {
        "p_1_1": {"L": 0, "H": 1},
        "p_1_2": {"L": 0, "H": 1},
        "p_1_3": {"L": 0, "H": 1},
        "p_1_4": {"L": 0, "H": 1},
    }
    type_two = {
        "p_2_1": {"L": 0, "H": 1},
        "p_2_2": {"L": 0, "H": 1},
        "p_2_3": {"L": 0, "H": 1},
        "p_2_4": {"L": 0, "H": 1},
    }
    type_three = {
        "p_3_1": {"L": 0, "H": 1},
        "p_3_2": {"L": 0, "H": 1},
        "p_3_3": {"L": 0, "H": 1},
        "p_3_4": {"L": 0, "H": 1},
    }

    def __init__(self, mul_init):
        if mul_init:
            """use dummy parameters instead - output strings will not be used in
            .prism files"""
            self.client_init_states = ['[1,0,0]']
            self.server_init_states = ['[1,0,0,0,0]']
        else:
            self.client_init_states = ['[1,0,0]', '[0,1,0]', '[0,0,1]']
            self.server_init_states = ['[1,0,0,0,0]', '[0,1,0,0,0]',
                                       '[0,0,1,0,0]', '[0,0,0,1,0]',
                                       '[0,0,0,0,1]']


class BenderoptParameters(BaseParameters):

    def __init__(self, mul_init):
        super().__init__(mul_init)
        self.types = [self.type_one, self.type_two, self.type_three]
        self.optimization_problem_parameters = self.set_parameters()

    def set_parameters(self):
        problem_parameters = [
            {
                "name": "client_count",
                "category": "categorical",
                "search_space": {
                    "values": self.client_count
                }
            },
            {
                "name": "client_init",
                "category": "categorical",
                "search_space": {
                    "values": self.client_init_states
                }
            },
            {
                "name": "server_init",
                "category": "categorical",
                "search_space": {
                    "values": self.server_init_states
                }
            },
            {
                "name": "connect_rates",
                "category": "categorical",
                "search_space": {
                    "values": self.connect_rate
                }
            },
        ]
        for client_type in self.types:
            for p in client_type:
                new_parameter = {
                    "name": p,
                    "category": "uniform",
                    "search_space": {
                        "low": client_type[p]["L"],
                        "high": client_type[p]["H"]
                    }
                }
                problem_parameters.append(new_parameter)
        return problem_parameters

    def __str__(self):
        return str(self.optimization_problem_parameters)


class HyperoptParameters(BaseParameters):
    def __init__(self, mul_init):
        super().__init__(mul_init)
        self.connect_rate = hp.choice('connect_rates', self.connect_rate)
        self.client_count = hp.choice('client_count', self.client_count)
        self.client_init_states = hp.choice(
            'client_init_states', self.client_init_states)
        self.server_init_states = hp.choice(
            'server_init_states', self.server_init_states)
        self.type_one = {
            "p_1_1": hp.uniform("p_1_1", 0, 1),
            "p_1_2": hp.uniform("p_1_2", 0, 1),
            "p_1_3": hp.uniform("p_1_3", 0, 1),
            "p_1_4": hp.uniform("p_1_4", 0, 1),
        }
        self.type_two = {
            "p_2_1": hp.uniform("p_2_1", 0, 1),
            "p_2_2": hp.uniform("p_2_2", 0, 1),
            "p_2_3": hp.uniform("p_2_3", 0, 1),
            "p_2_4": hp.uniform("p_2_4", 0, 1),
        }
        self.type_three = {
            "p_3_1": hp.uniform("p_3_1", 0, 1),
            "p_3_2": hp.uniform("p_3_2", 0, 1),
            "p_3_3": hp.uniform("p_3_3", 0, 1),
            "p_3_4": hp.uniform("p_3_4", 0, 1),
        }
        self.space = self.set_parameters()

    def set_parameters(self):
        return {
            'connect_rates': self.connect_rate,
            'client_count': self.client_count,
            'client_init': self.client_init_states,
            'server_init': self.server_init_states,
            'type_one': self.type_one,
            'type_two': self.type_two,
            'type_three': self.type_three,
        }

    def __str__(self):
        return str(self.space)


"""A class that inherits from HyperoptParameters where certain parameters are
fixed apart from p_i_j and p_i_5, where i and j are manually chosen"""
class HyperoptStability(HyperoptParameters):

    def __init__(self, opt_parameters, fix_type, fix_prob):
        if fix_type not in [1, 2, 3]:
            raise ValueError('fix_type not appropriate', fix_type)
        if fix_prob not in [1, 2, 3, 4]:
            raise ValueError('fix_prob not appropriate', fix_prob)
        self.fix_type = str(fix_type-1)
        self.fix_prob = 's_{i}'.format(i=fix_prob)
        self.prob_key_rand = "p_{i}_{j}".format(i=fix_type, j=fix_prob)
        print("Varying p_{i}_{j} and p_{i}_5...".format(i=fix_type, j=fix_prob))
        self.connect_rate = hp.choice('connect_rates',
                                      opt_parameters['connect_rates'])
        self.client_count = hp.choice('client_count',
                                      opt_parameters['client_count'])
        self.client_init_states = hp.choice(
            'client_init_states', opt_parameters['client_init_states'])
        self.server_init_states = hp.choice(
            'server_init_states', opt_parameters['server_init_states'])
        self.adjust_dist(opt_parameters)
        self.type_one = self.initialise_types(opt_parameters, fix_type, fix_prob, 1)
        self.type_two = self.initialise_types(opt_parameters, fix_type, fix_prob, 2)
        self.type_three = self.initialise_types(opt_parameters, fix_type, fix_prob, 3)
        self.space = self.set_parameters()

    def initialise_types(self, opt_parameters, fix_type, fix_prob, ctype):
        type_dict = {}
        for s in range(1, 5):
            prob_key = "p_{i}_{j}".format(i=ctype, j=s)
            if prob_key != self.prob_key_rand:
                type_dict[prob_key] = hp.choice(prob_key, ['0'])
            else:
                type_dict[prob_key] = hp.uniform(prob_key, 0, 1)
        return type_dict

    def adjust_dist(self, opt_parameters):
        for dist in self.distributions:
            if self.fix_type == dist:
                for s in self.distributions[dist]:
                    if s == self.fix_prob or s == 's_5':
                        continue
                    else:
                        self.distributions[dist][s] = [opt_parameters[dist][s]]*2
                        normalise(self.distributions[dist])
            else:
                for s in self.distributions[dist]:
                    self.distributions[dist][s] = [opt_parameters[dist][s]]*2