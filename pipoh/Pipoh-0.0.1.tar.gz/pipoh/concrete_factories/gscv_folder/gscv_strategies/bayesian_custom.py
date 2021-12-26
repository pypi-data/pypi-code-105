from pipoh.concrete_factories.bayesian_folder.bayesian_interface import InterfaceBayesian


class BayesianCustomStrategy(InterfaceBayesian):
    #En el init poner los parametros que quiera
    def __init__(self, params):
        self.f = params.get('f')
        self.args = params.get('args')

    def get_dimensions(self):
        return 'ok'

    def get_all_parameters(self):
        return "ok"

    def get_hyper_parameters(self):
        return "Hyper parameters selection done"

    def solve_optimization_problem(self):
        try:
            for x, y in self.values.items():
                if x != 'f' and x != 'hp':
                    exec('self.{}=y'.format(x, x))
        except:
            pass
        self.f(self)
        return 1

