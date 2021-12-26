import numpy as np


def rolling_windows_validation(STRATEGY_SELECTED):
    # Save number of elements and number of assets
    (numData, N) = STRATEGY_SELECTED.data.shape

    # Initialize the weights matrix
    W = np.zeros((STRATEGY_SELECTED.validation_windows, N))

    for i in range(1, STRATEGY_SELECTED.validation_windows):
        STRATEGY_SELECTED.intermediate_data = STRATEGY_SELECTED.data[i:numData-STRATEGY_SELECTED.validation_windows + i,:]
        # Comprobación de que el array no sea cero.
        assert np.count_nonzero(np.isnan(STRATEGY_SELECTED.intermediate_data)) == 0
        W[[i]] = np.transpose(STRATEGY_SELECTED.solve_optimization_problem())

    a = W
    b = (STRATEGY_SELECTED.data[STRATEGY_SELECTED.data.shape[0] - STRATEGY_SELECTED.validation_windows:, :])
    STRATEGY_SELECTED.returns = np.multiply(a, b).sum(axis=1, dtype='float')
    STRATEGY_SELECTED.weights = W

    return 'Successfully executed'
