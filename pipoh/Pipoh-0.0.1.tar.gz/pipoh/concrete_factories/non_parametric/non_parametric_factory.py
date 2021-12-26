from pipoh.concrete_factories.non_parametric.non_parametric_strategies.ew import EW


class NonParametricFactory:

    @staticmethod
    def get_specific_strategy(strategy_selected, params=None):
        """A static method to get a chair"""
        try:
            if strategy_selected == 'EW':
                return EW()
            raise Exception('Strategy not found')
        except Exception as _e:
            print(_e)
        return None
