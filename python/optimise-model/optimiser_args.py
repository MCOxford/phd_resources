from argparse import ArgumentParser
from pathlib import Path


# Options to pass to smbo.py
class OptimiserArgs(ArgumentParser):

    def __init__(self, *args, **kwargs):

        if not 'description' in kwargs:
            kwargs['description'] = """Code that applies parameter
      optimisation to PRISM models given a quantitative property."""

        super().__init__(*args, **kwargs)

        self.add_argument('-e', '--evaluations',
                          dest="evaluations",
                          type=int,
                          required=False,
                          help="how many trial evaluations do you want this session?",
                          metavar="INTEGER",
                          default=500)
        self.add_argument('-s', '--split',
                          dest="is_split",
                          action="store_true",
                          help="""Perform model checking on splitworld models
                  instead of honest.""")
        self.add_argument('-db', '--database',
                          dest="db",
                          type=str,
                          required=False,
                          help="""Which database to write data into. Default is
                  to write to test_db.sqlite""",
                          metavar="FILE",
                          default="build/test_db.sqlite")
        self.add_argument('-mulinit', '--multipleinitialstates',
                          dest="mul_init",
                          action="store_true",
                          help="""Model check over multiple initial state.
                  Default is to have only one dependent on chosen
                  parameters.""")
        self.add_argument('-p', '--propertyno',
                          dest="prop_no",
                          type=int,
                          required=False,
                          help="""Which property to evaluate. Default is to
                  use the first listed property in the .props file.""",
                          metavar="INTEGER",
                          default=1),
        self.add_argument('-symm', '--symmreduction',
                          dest="symm",
                          action="store_true",
                          help="""Automatically apply symmetry reduction on
                  models.""")
        self.add_argument('-hopt', '--hyperopt',
                          dest="hyperopt",
                          action="store_true",
                          help="""Use the hyperopt optimiser.""")
        self.add_argument('-props', '--propfile',
                          dest="props_file",
                          type=str,
                          required=True,
                          help="""Which .props file to use.""",
                          metavar="FILE")
        self.add_argument('-out', '--output',
                          dest="std_out",
                          type=str,
                          required=False,
                          help="Where to write suggested parameters.",
                          metavar="FILE",
                          default='build/output.txt')
        self.add_argument('-t', '--trials',
                          dest="trials",
                          type=str,
                          required=True,
                          help="""Load a file containing trial data from
                  previous experiments""",
                          metavar="FILE")

    def validate_namespace(self, namespace):

        if namespace.evaluations < 1:
            error_msg_format = "invalid evaluation number: {e}"
            error_msg = error_msg_format.format(e=namespace.evaluations)
            self.error(error_msg)
        if not namespace.db.endswith(".sqlite"):
            error_msg_format = "Database file needs to be in .sqlite format: {f}"
            error_msg = error_msg_format.format(f=namespace.db)
            self.error(error_msg)
        config = Path(namespace.props_file)
        if not config.is_file():
            error_msg_format = "File not found: {f}"
            error_msg = error_msg_format.format(f=namespace.props_file)
            self.error(error_msg)

    def parse_args(self, *args, **kwargs):
        namespace = super().parse_args(*args, **kwargs)
        self.validate_namespace(namespace)
        return namespace


"""
Arguments to pass to stability_test.py. Allows the user to randomise
over two probabilities by passing a client type and server number. Both are
required. it client type t and server number j is passed where 1<=j<=4,
p_t5 will also be randomised.
"""
class StabilityOptimiserArgs(OptimiserArgs):

    def __init__(self, *args, **kwargs):

        if not 'description' in kwargs:
            kwargs['description'] = """Code that applies parameter
      optimisation to PRISM models given a quantitative property."""

        super().__init__(*args, **kwargs)
        
        self.add_argument('-ft', '--fix-type',
                  type=int,
                  dest="fix_type",
                  required=False,
                  help="Fix a client type. Default is 1.",
                  metavar="INTEGER",
                  default=1)
        self.add_argument('-fp', '--fix-prob',
                  type=int,
                  dest="fix_prob",
                  required=False,
                  help="Fix a server type. Default is 1.",
                  metavar="INTEGER",
                  default=1)
