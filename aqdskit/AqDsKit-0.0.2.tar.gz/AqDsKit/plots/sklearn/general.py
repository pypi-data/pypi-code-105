import matplotlib
import numpy as np
from cycler import cycler
from matplotlib import pyplot as plt
from sklearn.metrics import check_scoring

from AqDsKit.models.sklearn.hyperparam import train_different_hyperparam, cv_score_different_hyperparam
from AqDsKit.plots.commons.basics import plot_multiple_ys_against_x
from AqDsKit.plots.commons.tools import plan_plot_grid, ax_walker

""" plotting 
"""


def plot_cv_scores_over_hyperparams(
        clf,
        X,
        y = None,
        param_grid: dict = None,
        scoring_grid: dict = None,
        absolute_score: bool = False,
        cv: int = 5,
        n_jobs: int = -1,
        title: str = 'Score Over Hyperparameter',
        ax: matplotlib.axes.Axes = None,
        figsize: tuple = None,
        title_fontsize: str = "large",
        text_fontsize: str = "medium"
    ):
    """Plots score(s) of a model over for specified hyperparameter(s)

    Args:
        clf: Clusterer instance that implements ``fit``,``fit_predict``, and
            ``score`` methods (or have labels_ attribute), and an ``n_clusters`` or ``n_components`` hyperparameter.
            e.g. :class:`sklearn.cluster.KMeans` instance, GaussianMixture instance

        X (array-like, shape (n_samples, n_features)):
            Data to cluster, where n_samples is the number of samples and
            n_features is the number of features.

        y: y_train to give the label info, None for unsupervised learning

        param_grid: a dictionary of {param_name, param_ranges}, you can add multiple params to test, and will create one plot per param
            param_name: name of the hyperparameter
            param_ranges: (None or :obj:`list` of int, optional): List of
                param values for which to train the model and plot the corresponding score

        scoring_grid: dictionary of {score_name : scoring_func}, you can add multiple score metrics
            score_name: name of the score to be displayed on the plot
            scoring_func: if given, use this scoring func to calculate score, otherwise plese parse None and it will use model.score()
                            scoring_func can be either str (sklearn pre-defined scorer) or callable (custom scorer func)

        absolute_score: whether the score need to be a positive number (sometimes scores are negative, e.g. score of K-means)

        cv: number of cross validation circles; set to -1 or None if you want to skip CV and only do on training set

        n_jobs (int, optional): Number of jobs to run in parallel. Defaults to -1.

        title (string, optional): Title of the generated plot

        ax (:class:`matplotlib.axes.Axes`, optional): The axes upon which to
            plot the curve. If None, the plot is drawn on a new set of axes.

        figsize (2-tuple, optional): Tuple denoting figure size of the plot
            e.g. (6, 6). Defaults to ``None``.

        title_fontsize (string or int, optional): Matplotlib-style fontsizes.
            Use e.g. "small", "medium", "large" or integer-values. Defaults to
            "large".

        text_fontsize (string or int, optional): Matplotlib-style fontsizes.
            Use e.g. "small", "medium", "large" or integer-values. Defaults to
            "medium".

    Returns:
        ax (:class:`matplotlib.axes.Axes`): The axes on which the plot was
            drawn.
    """

    # if scoring_grid is not passed, use single default score method (set scoring_func to None):
    if scoring_grid is None:
        scoring_grid = {'score' : None}

    if param_grid is None:
        raise ValueError("Must specify at least one param to plot via param_grid attribute: param_grid = {param_name : param_ranges}")

    param_scorings = {} # save {param_name : {score_name: scores} } for each scoring metric and each param_name

    for param_name, param_ranges in param_grid.items():
        scorings = {} # save {score_name: scores} for each scoring metric

        if cv == -1 or cv is None:
            # skip cross validation and build score only on the training set (full X provided)
            clfs, times = train_different_hyperparam(clf, X, y, param_name = param_name, param_ranges = param_ranges,
                                                     n_jobs = n_jobs)

            for score_name, scoring_func in scoring_grid.items():
                # if scoring_func is None:
                #     scores = [clf.score(X, y) for clf in clfs]
                # else:

                scoring_func = check_scoring(clf, scoring_func) #  scoring_func can be str or callable (custom scorer func)
                scores = [scoring_func(clf, X, y) for clf in clfs]  # for K-means, score = -inertia

                if absolute_score:
                    scores = np.absolute(scores)

                scorings[score_name] = scores
        else:
            # otherwise use cross validation
            # will not train during the model build
            for score_name, scoring_func in scoring_grid.items():
                # parallel run cv_score process as it will take a lot of time
                scores, times = cv_score_different_hyperparam(clf, X, y, param_name = param_name, param_ranges = param_ranges,
                                                              scoring_func = scoring_func, cv = cv, n_jobs = n_jobs)
                #scores = [cross_val_score(clf, X, y, scoring = scoring_func, cv = cv, n_jobs = n_jobs).mean() for clf in clfs]
                if absolute_score:
                    scores = np.absolute(scores)

                scorings[score_name] = scores

        param_scorings[param_name] = scorings

    # decide the size/layout of the plot
    n_plots = len(param_grid)
    rows, cols = plan_plot_grid(n_plots)

    if ax is None:
        fig, axes = plt.subplots(rows, cols, figsize = figsize)
    else:
        axes = ax

    walker = ax_walker(n_plots, axes)
    plt.rc('axes', prop_cycle = (cycler('color', ['#7969aa', '#678659', '#9d9962', '#b35252', '#a26fa6'])))

    for ax, (param_name, scorings) in zip(walker, param_scorings.items()):

        sub_title = f"{title}\n({param_name})"
        param_ranges = param_grid[param_name]

        plot_multiple_ys_against_x(
            ax, x = param_ranges, ys_dict = scorings, ys_dict_r = None,
            x_label = param_name, y_label = 'Score',
            title = sub_title, title_fontsize = title_fontsize, text_fontsize = text_fontsize,
        )


    fig.tight_layout()

    return axes


