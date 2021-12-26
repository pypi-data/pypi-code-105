from pipoh.concrete_factories.gscv_folder.gscv_interface import InterfaceGSCV
from pipoh.strategies.class_wlbc import fnc_WLBC

class gscvWLBC(fnc_WLBC, InterfaceGSCV):

    def __init__(self):
        super(gscvWLBC, self).__init__()

    def solve_optimization_problem(self):
        return super(gscvWLBC, self).solve_optimization_problem()
