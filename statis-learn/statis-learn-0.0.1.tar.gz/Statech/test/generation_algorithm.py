import numpy as np
from Statech.generation_alogrithm_model import GA

from Statech.generation_alogrithm_model import ranking, selection, mutation, crossover

if __name__ == "__main__":
    np.random.seed(1)
    demo_func = lambda x: x[0] ** 2 + (x[1] - 0.05) ** 2 + (x[2] - 0.5) ** 2
    ga = GA(fit_func=demo_func, n_feature=3, n_pop=100, n_gen=500, prob_mut=0.001,
            lb=[-1, -10, -5], ub=[2, 10, 2], precision=[1e-7, 1e-7, 1])

    ga.register(operator_name='selection', operator=selection.selection_roulette_1)
    ga.register(operator_name='ranking', operator=ranking.ranking). \
        register(operator_name='crossover', operator=crossover.crossover_2point). \
        register(operator_name='mutation', operator=mutation.mutation)

    best_x, best_y = ga.run()
    print('best_x:', best_x, '\n', 'best_y:', best_y)
