from .utils import has_dependency, requires

import logging
import heapq


# external dependencies go here (i.e. those not in standard library)
if has_dependency("pandas"):
    import pandas as pd

if has_dependency("numpy"):
    import numpy as np

if has_dependency("scipy.optimize"):
    import scipy.optimize as opt
# end of external dependencies


@requires('numpy', 'scipy.optimize')
def feature_selection_merits_initial_guess(target_correlations, features_correlations, selected_features_ratio=0.2):
    """
    Heuristic to find a suitable initial guess for merits-based feature selection, returns
    frozenset that can be directly passed to starting_features in feature_selection_merits.

    IMPORTANT: always use stepwise algorithm in feature selection when using initial guess.
    the forward algorithm can only add features, so if there are some bad ones in this guess,
    it won't be able to remove them later on.

    It relaxes the original problem from ILP to real-valued optimization,
    solves it using scipy.minimize, and then converts it back to integer solution
    using simple threshold heuristic.

    The threshold is adjusted such that in the final set, exactly `selected_features_ratio` features
    are selected out of all features.

    :features_correlations: Pandas DataFrame with correlation coefficients (or other similarity).
        Expects symmetric matrix with positive values and 1 in diagonal entries. Both Index and
        Columns should be indexed by feature names.
    :target_correlations: Pandas DataFrame with one row named 'target' and columns
        indexed with feature names containing values as in :param feature_correlations
    :selected_features_ratio: number between 0 and 1, sets the proportion of selected features
        in the returned set. setting it to 1 will select all features.

    :return: frozenset of selected features
    """

    def negative_merit_squared(x, a, B):
        return -np.dot(x, a) ** 2 / (x.T @ B @ x + 1e-6)

    a = target_correlations.values.squeeze()
    B = features_correlations.values
    k = len(a)

    x0 = np.zeros(k)

    result = opt.minimize(negative_merit_squared, x0, (a, B), bounds=[(0, 1)] * k, options=dict(disp=True))

    threshold = np.quantile(result.x, 1 - selected_features_ratio)
    x0 = (result.x > threshold).astype(int)

    features = list(target_correlations.columns)
    return frozenset([feature for i, feature in enumerate(features) if x0[i]])


@requires('numpy', 'pandas')  # noqa: C901
# flake8: noqa: C901
def feature_selection_merits(
        features_correlations,
        target_correlations,
        max_iter: int = None,
        starting_features: frozenset = None,
        frozen_features: frozenset = None,
        algorithm: str = "stepwise",
        best_n: int = 1,
):
    """
    Search for best subset of features based on their ``merit``.
    See https://en.wikipedia.org/wiki/Feature_selection#Correlation_feature_selection
    This function implements feature selection algorithm outlined in link above. For a given set
    of features, we can define their ``merit`` based on their similarity with target and with
    each other. The most common use-case is to use absolute value of correlation but in principle
    other measures of similarity can be used (symmetric matrix with values in [0, 1] is expected).
    Definition of merit favors set of features with high correspondence (correlation) with target
    but low among themselves, therefore lower number of more meaningful features is preferred
    as the algorithm penalizes additional features which do not add any new information.
    There are several strategies for searching the space of all subsets and they can be specified
    using the parameter ``algorithm``. The simplest is greedy forward algorithm (option
    ``forward``) which at each step adds one feature that increases the merit of the subset the
    most.
    Another option is ``stepwise`` (default option) which looks at ``best_n`` subsets from
    before and tries adding or removing one other feature. This provides robustness since
    features can also be removed later while keeping the number of tried combinations relatively
    low (in each step only ``best_n`` times the number of features subsets are evaluated).
    It is possible to specify starting position with ``starting_features`` and ``frozen_features``.
    The difference is that features from ``starting_features`` can be removed if the
    algorithm supports removal while features from ``frozen_features`` cannot be removed.
    For large sets of features (in the order of thousands), this can take a while, use function
    ``feature_selection_merits_initial_guess()`` for a heuristic starting point

    :features_correlations: Pandas DataFrame with correlation coefficients (or other similarity).
        Expects symmetric matrix with positive values and 1 in diagonal entries. Both Index and
        Columns should be indexed by feature names.
    :target_correlations: Pandas DataFrame with one row named 'target' and columns
        indexed with feature names containing values as in :param feature_correlations
    :starting_features: List or set of features describing starting point
        of the algorithm. Default value is empty set. Use ``feature_selection_merits_initial_guess``
        to get a suitable starting point from heuristic (in that case make sure to use 'stepwise')
    :frozen_features: List or set of features, which you want to mandate to have
        in the selected feature set
    :algorithm: one of ``stepwise``, ``forward``
    :max_iter: maximum number of iteration, default is ``number of features / 3``
    :best_n: number "best candidates" kept in each step (best_n linearly increases runtime, best_n=3
        will have 3x the runtime of best_n=1),
        best_n=1 is good default, use more when you can afford it
    :return: feature set, history (in order) where feature set is a frozenset containing
        the best set of features in the last iteration and history is a Pandas Dataframe
        with columns
    .. code-block:: text
        iteration     index of iteration, 0 is the initial step.
        rank          order of the feature set candidates in each step ranked
                      0, ..., best_n ranked by the squared merit with 0 as the highest merit
        merit_sq      squared merit of the feature set
        features      list of selected features in the subset
        num_features  number of features in the subset
    :rtype: (frozenset, pd.DataFrame)
    """
    # NOTE: might be a good idea to split logic into helper functions

    features = features_correlations.columns
    k = len(features)

    def mask_to_frozenset(x):
        return frozenset([feature for i, feature in enumerate(features) if x[i]])

    def frozenset_to_mask(s):
        return [1.0 if feature in s else 0.0 for feature in features]

    # treating of user inputs
    starting_features = starting_features if starting_features is not None else frozenset()
    frozen_features = frozen_features if frozen_features is not None else frozenset()

    starting_features = frozenset_to_mask(frozenset(starting_features).union(frozenset(frozen_features)))
    frozen_features = frozenset_to_mask(frozen_features)

    B = features_correlations.abs().values
    a = target_correlations.abs().values

    if algorithm not in ["stepwise", "forward"]:
        algorithm = "stepwise"
        logging.warning("Unknown algorithm type, defaulting to stepwise algorithm.")

    # if the maximum iteration is not set, lets set it to third of all features
    if max_iter is None:
        max_iter = int(k / 3)

    # starting point setting
    starting_set = np.max([starting_features, frozen_features], axis=0)

    x = starting_set
    old_max_merit_sq = ((x @ a.T) ** 2 / (x.T @ B @ x + 1e-6))[0]
    new_max_merit_sq = old_max_merit_sq

    # history initialization
    results_history = list()
    results_history.extend(
        [
            {
                "iteration": 0,
                "rank": k,
                "features": mask_to_frozenset(starting_set),
                "merit_sq": new_max_merit_sq,
                "num_features": len(mask_to_frozenset(starting_set)),
            }
            for k in range(best_n)
        ]
    )

    # dictionary for storing of merits of subsets
    subsets_merits = {tuple(starting_set): old_max_merit_sq}
    best_n_sets = [starting_set]

    # lets do max_iter iterations
    for iter_idx in range(max_iter):

        local_subsets_merits = dict()

        # if the algorithm is 'forward, we need to forget previous steps'
        if algorithm == "forward":
            subsets_merits = dict()

        # for each iteration, lets have a best/list of best trackers and lets branch our list in the extend of the tracker
        for leading_subset in best_n_sets:
            subsets_to_compute = []

            for i, feature_value in enumerate(leading_subset):
                # if the feature is in frozen features, skip the loop and continue with next one
                # for forward algorithm, we just want to add new features
                if frozen_features[i] or (algorithm == "forward" and feature_value):
                    continue

                step_subset = list(leading_subset)
                step_subset[i] = 1 - step_subset[i]

                step_subset_tuple = tuple(step_subset)

                if step_subset_tuple in subsets_merits:
                    local_subsets_merits[step_subset_tuple] = subsets_merits[step_subset_tuple]
                else:
                    subsets_to_compute.append(step_subset_tuple)

            if subsets_to_compute:
                X = np.stack(subsets_to_compute)

                merits = ((X @ a.T) ** 2)[:, 0] / (np.diag(X @ B @ X.T) + 1e-6)

                for i, subset_tuple in enumerate(subsets_to_compute):
                    local_subsets_merits[subset_tuple] = merits[i]
                    subsets_merits[subset_tuple] = merits[i]

        # EVALUATION
        # get best set and its merit_sq
        if len(subsets_merits) > 0:
            best_n_sets = heapq.nlargest(
                best_n, subsets_merits, key=subsets_merits.get
            )  # low prio - space for optimization, have subsets_merits as a heap
            max_set = best_n_sets[0]
            new_max_merit_sq = subsets_merits[max_set]
        else:
            best_n_sets = []
            max_set = frozenset()
            new_max_merit_sq = 0

        subsets_merits.update(local_subsets_merits)

        # evaluation of run, perhaps stopping it earlier
        if (
                algorithm == "stepwise" and new_max_merit_sq > old_max_merit_sq
        ):  # we can add minimum required improvement here or early_stopping (patience)
            # updating new maximum
            old_max_merit_sq = new_max_merit_sq
            # extending the history with the new n largest
            results_history.extend(
                [
                    {
                        "iteration": iter_idx + 1,
                        "rank": order,
                        "features": mask_to_frozenset(best_n_sets[order]),
                        "merit_sq": subsets_merits[best_n_sets[order]],
                        "num_features": len(mask_to_frozenset(best_n_sets[order])),
                    }
                    for order, leading_set in enumerate(best_n_sets)
                ]
            )
        elif algorithm == "forward" and len(subsets_merits) > 0:
            # for forward algorithm, we just go blindly forward for given number of steps
            results_history.extend(
                [
                    {
                        "iteration": iter_idx + 1,
                        "rank": order,
                        "features": mask_to_frozenset(best_n_sets[order]),
                        "merit_sq": subsets_merits[best_n_sets[order]],
                        "num_features": len(mask_to_frozenset(best_n_sets[order])),
                    }
                    for order, leading_set in enumerate(best_n_sets)
                ]
            )
            # if we reached all variables, we want to stop
            if sum(best_n_sets[0]) == len(best_n_sets[0]):
                break
        else:
            break

    return mask_to_frozenset(best_n_sets[0]), pd.DataFrame.from_records(
        results_history
    )
