import numpy as np
from sklearn.base import BaseEstimator
from sklearn.model_selection import GridSearchCV

from pipoh.common_functions.rolling_windows_validation import rolling_windows_validation

class custom_gridsearch_cv(BaseEstimator):

    def __init__(self,  STRATEGY_SELECTED ):
        self.STRATEGY_SELECTED = STRATEGY_SELECTED
        """try:
            for x, y in self.param_grid.items():
                if x != 'f' and x != 'hp':
                    exec('self.{}=y'.format(x, x))
        except:
            pass"""
        return

    def fit(self, X, STRATEGY_SELECTED):
        STRATEGY_SELECTED.intermediate_data = X
        rolling_windows_validation(STRATEGY_SELECTED)
        value = np.std(STRATEGY_SELECTED.returns) / STRATEGY_SELECTED.returns.mean()
        return value

    """def get_params(self, deep=True):
        return {"n_nodes": self.n_nodes,
                "n_jobs": self.n_jobs}"""

    def set_params(self, **parameters):
        for parameter, value in parameters.items():
            setattr(self, parameter, value)
        return self

"""### Fit the c parameter ###
X = np.random.normal(0, 1, (100,5))
y = X[:,1] * X[:,2] + np.random.normal(0, .1, 100)

gs = GridSearchCV(custom_gridsearch_cv(n_nodes=20), cv=5, param_grid={"c":np.linspace(0.0001,1,10)}, scoring = 'accuracy')
output = gs.fit(X)
output.best_params_"""






























class InitialConfiguration(custom_gridsearch_cv):
    def initial_configuration(self, strategy, params):
        if strategy == 'WUBC':
            #optim_param = {'lambda_value': ('cont', [0, 1]), 'upperBound': ('cont', [0, 1])}
            optim_param = params
        if strategy == 'WLBC':
            param_hip = {'lambda_value': ('cont', [0, 1]), 'lowerBound': ('cont', [0, 1])}
        if strategy == 'CustomStrategy':
            for x, y in params.items():
                if x!='f' and x!='hp':
                    exec('self.{}=params["{}"]'.format(x, x))
            #self.validation_windows=params['validation_windows']
            param_hip = params['hp']
            self.optim_param = params['hp']
        if strategy != 'CustomStrategy':
            param_hip = params
            self.optim_param = params
        try:
            for x, y in self.values.items():
                if x != 'f' and x != 'hp':
                    exec('self.{}=y'.format(x, x))
        except:
            pass




        gs = GridSearchCV(custom_gridsearch_cv( STRATEGY_SELECTED = self), cv=5, param_grid={'lambda_value': np.linspace(0.0001,1,1), 'upperBound': np.linspace(0.0001,1,1)}, scoring = 'accuracy')
        output = gs.fit(self.data[0:-self.validation_windows:, :], STRATEGY_SELECTED=self)
        output.best_params_

        # Extract the best parameters
        # obj.lambda_value = results.best[[0]]
        # obj.upperBound = results.best[[1]]
        #self.values = results.getResult()

        for x, y in output.best_params_.items():
            exec('self.{}={}'.format(x,y))
        # obj.lambda_value = results.getResult()
        # obj.upperBound = 0.3128
        return 'SUCCESS'







