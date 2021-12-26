from pipoh.concrete_factories.bayesian_folder.bayesian_strategies.bayesian_custom import BayesianCustomStrategy
from pipoh.concrete_factories.bayesian_folder.bayesian_strategies.bayesian_ew import BayesianEW
from pipoh.concrete_factories.bayesian_folder.bayesian_strategies.bayesian_wlbc import BayesianWLBC
from pipoh.concrete_factories.bayesian_folder.bayesian_strategies.bayesian_wubc import BayesianWUBC


class BayesianFactory:
    """The Factory Class"""

    @staticmethod
    def get_specific_strategy(strategy_selected, params=None):
        """A static method to get a chair"""
        try:
            if strategy_selected == 'BayesianEW':
                return BayesianEW()
            if strategy_selected == 'BayesianWUBC':
                return BayesianWUBC()
            if strategy_selected == 'BayesianWLBC':
                return BayesianWLBC()
            if strategy_selected == 'BayesianCustomStrategy':
                return BayesianCustomStrategy(params)
            raise Exception('Strategy Not Found')
        except Exception as _e:
            print(_e)
        return None
