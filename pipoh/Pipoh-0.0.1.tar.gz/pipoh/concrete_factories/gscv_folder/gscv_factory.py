from pipoh.concrete_factories.gscv_folder.gscv_strategies.gscv_wlbc import gscvWLBC

from pipoh.concrete_factories.gscv_folder.gscv_interface import InterfaceGSCV
from pipoh.strategies.class_wlbc import fnc_WLBC

class gscvWLBC(fnc_WLBC, InterfaceGSCV):

    def __init__(self):
        super(gscvWLBC, self).__init__()

    def solve_optimization_problem(self):
        return super(gscvWLBC, self).solve_optimization_problem()


class gscvFactory:

    @staticmethod
    def get_specific_strategy(strategy_selected, params=None):
        try:
            if strategy_selected == 'GridSearchCVWLBC':
                return gscvWLBC()
            raise Exception('Strategy Not Found')
        except Exception as _e:
            print(_e)
        return None
