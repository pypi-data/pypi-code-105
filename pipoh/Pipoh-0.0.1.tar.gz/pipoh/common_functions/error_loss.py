from pipoh.common_functions.rolling_windows_validation import rolling_windows_validation
import numpy as np
#from main import STRATEGY_SELECTED


def errorLoss (lambda_value, upperBound):
    STRATEGY_SELECTED.lamb = lambda_value
    STRATEGY_SELECTED.upper_bound = upperBound
    rolling_windows_validation(STRATEGY_SELECTED)
    value = np.std(STRATEGY_SELECTED.returns) / STRATEGY_SELECTED.returns.mean()
    return value


"""
def error_loss(lamb, upperBound):
    optimizer_parameters_strategy.lamb = lamb
    optimizer_parameters_strategy.upperBound = upperBound
    returns = rolling_windows_validation(strategy_selected, dataValidation, optimizer_parameters_strategy)
    value = np.std(returns) / returns.mean()
    return value
"""