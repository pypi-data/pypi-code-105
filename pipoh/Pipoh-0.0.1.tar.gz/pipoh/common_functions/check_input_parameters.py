
def check_input_parameters_py_strategy(strategy, data_input, solver):

    strategies_implemeted = ['ew', 'wubc', 'wlbc']
    # assert to check that input data is introduced
    assert strategy.lower() in strategies_implemeted, 'Strategy not recognized'

    # assert to check that input data is introduced
    assert len(data_input) > 5, 'Needed a path for reading the input data information'



    # Check that the strategy has a correct solver
    strategies_not_use_solver = ['ew']
    if solver == None:
        assert strategy.lower() in strategies_not_use_solver, str(strategy+' strategy requires a solver')
    if solver != None:
        strategies_use_bayesian = ['wubc', 'wlbc']
        if solver.lower() == 'bayesian':
            assert strategy.lower() in strategies_use_bayesian, str(strategy+' strategy do not use a solver ' + solver)
        strategies_use_grid_search = ['wubc', 'wlbc']
        if solver.lower() == 'grid_search':
            assert strategy.lower() in strategies_use_grid_search, str(
                strategy + ' strategy do not use a solver ' + solver)

    # Solvers
    solvers_implemented = ['bayesian', 'grid_search']
    if solver != None:
        assert solver.lower() in solvers_implemented, 'Strategy not recognized'



    return 'Parameters introduced successfully'