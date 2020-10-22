from json import loads
from subprocess import call

# Maximum memory allocated for each model type
CUDDMEM = 40

# symm values
SYMM_START = 0
SYMM_END = 5


class PRISMData(object):

    def __init__(self, options, prism_file, space, log_file, result_file):
        self.mul_init = options.mul_init
        self.prop_no = options.prop_no
        self.symm = options.symm
        self.props_file = options.props_file
        self.prism_file = prism_file
        self.log_file = log_file
        self.result_file = result_file
        self.client_count = loads(space['client_count'])
        self.client_init = loads(space['client_init'])
        if self.symm:
            self.symm_start, self.symm_end = self.symm_values()

    # find -symm values for symmetry reduction. Note that this would
    # not be used in general to find the correct -symm values as this
    # is specific only to our network.
    def symm_values(self):
        symm_start = SYMM_START
        symm_end = SYMM_END

        if self.mul_init:
            ind_max = self.client_count.index(max(self.client_count))
            symm_start += sum(self.client_count[0:ind_max])
            symm_end += sum(
                self.client_count[len(self.client_count):ind_max:-1])
            return str(symm_start), str(symm_end)
        else:
            list_diff = list()
            for i in range(len(self.client_count)):
                list_diff.append(self.client_count[i] - self.client_init[i])
            ind_max = list_diff.index(max(list_diff))
            if ind_max == self.client_init.index(max(self.client_init)):
                symm_start += sum(self.client_count[0:ind_max]) + 1
            else:
                symm_start += sum(self.client_count[0:ind_max])
            symm_end += sum(
                self.client_count[len(self.client_count):ind_max:-1])
            return str(symm_start), str(symm_end)

    # Perform model checking given -prop number and prism file. Writes to
    # log_file and outputs result to results_file
    def perform_verification(self):
        result = None
        with open(self.log_file, 'wb') as f:
            # If prism not in bin/, run ./prism instead
            terminal_call = ["prism", self.prism_file, self.props_file, "-prop",
                             str(self.prop_no), ]

            if self.symm:
                terminal_call.extend(
                    ["-symm", self.symm_start, self.symm_end, ])
            if type(CUDDMEM) != int:
                raise TypeError("CUDDMEM not an integer")
            maxmem = str(CUDDMEM) + 'g'
            terminal_call.extend(["-cuddmaxmem", maxmem, "-s", ])
            terminal_call.extend(["-exportresults", self.result_file])
            try:
                call(terminal_call, stdout=f)
            except:
                print('Invalid terminal command.')

    def extract_result(self):
        with open(self.result_file, 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    continue
                line = line.strip()
                # stop loop if EOF is reached
                if not line:
                    break
                if line == "Infinity":
                    result = float("inf")
                    raise ValueError("Infinity result found.")
                result = loads(line)
                if not isinstance(result, list):
                    result = [result]

        return result
