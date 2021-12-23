import matplotlib
from matplotlib import pyplot as plt
import numpy as np
from scikitplot.metrics import plot_silhouette

from AqDsKit.plots.commons.tools import plan_plot_grid, ax_walker
from AqDsKit.plots.sklearn.general import plot_cv_scores_over_hyperparams, train_different_hyperparam

""" 
Visually Choose the best n_clusters for the clustering model (silhouette analysis and elbow method) 
"""

def plot_elbow_curve(
        clf,
        X,
        cluster_ranges: list = None,
        n_jobs: int = -1,
        title = 'Elbow Plot',
        ax: matplotlib.axes.Axes = None,
        figsize: tuple = None,
        title_fontsize: str = "large",
        text_fontsize: str = "medium"
    ):
    """Plots elbow curve of different values of K for KMeans clustering.

    Args:
        clf: Clusterer instance that implements ``fit``,``fit_predict``, and
            ``score`` methods (or have labels_ attribute), and an ``n_clusters`` or ``n_components`` hyperparameter.
            e.g. :class:`sklearn.cluster.KMeans` instance, GaussianMixture instance

        X (array-like, shape (n_samples, n_features)):
            Data to cluster, where n_samples is the number of samples and
            n_features is the number of features.

        cluster_ranges (None or :obj:`list` of int, optional): List of
            n_clusters for which to plot the explained variances. Defaults to
            ``range(1, 12, 2)``.

        n_jobs (int, optional): Number of jobs to run in parallel. Defaults to -1.

        title (string, optional): Title of the generated plot. Defaults to "Elbow Plot"

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

    Example:
        >>> kmeans = KMeans(random_state=1)
        >>> plot_elbow_curve(kmeans, cluster_ranges=range(1, 30))
        <matplotlib.axes._subplots.AxesSubplot object at 0x7fe967d64490>
        >>> plt.show()
    """

    if cluster_ranges is None:
        cluster_ranges = range(1, 12, 2)
    else:
        cluster_ranges = sorted(cluster_ranges)


    scoring_grid = {'Sum of Squared Errors' : None}

    if hasattr(clf, 'n_clusters'):
        param_grid = {'n_clusters' : cluster_ranges}

    elif hasattr(clf, 'n_components'):
        param_grid = {'n_components' : cluster_ranges}

    else:
        raise TypeError('"n_clusters" or "n_components" attribute not in classifier. '
                        'Cannot plot elbow method.')

    plot_cv_scores_over_hyperparams(
        clf, X, y = None, param_grid = param_grid, scoring_grid = scoring_grid,
        absolute_score = True, n_jobs = n_jobs, title = title,
        ax = ax, figsize = figsize,
        title_fontsize = title_fontsize, text_fontsize = text_fontsize
    )


def plot_silhouettes(
        clf,
        X,
        cluster_ranges: list = None,
        n_jobs: int = -1,
        title = 'Silhouette Analysis',
        metric = 'euclidean',
        copy: bool = True,
        figsize: tuple = None,
        cmap = 'tab20b',
        title_fontsize = "large",
        text_fontsize = "medium"
    ):
    """
    Args:
        clf: Clusterer instance that implements ``fit``,``fit_predict``, and
            ``score`` methods (or have labels_ attribute), and an ``n_clusters`` or ``n_components`` hyperparameter.
            e.g. :class:`sklearn.cluster.KMeans` instance, GaussianMixture instance

        X (array-like, shape (n_samples, n_features)):
            Data to cluster, where n_samples is the number of samples and
            n_features is the number of features.

        cluster_ranges (array-like, shape (n_samples,)):
            Cluster label for each sample.

        n_jobs (int, optional): Number of jobs to run in parallel. Defaults to -1.

        title (string, optional): Title of the generated plot. Defaults to
            "Silhouette Analysis"

        metric (string or callable, optional): The metric to use when
            calculating distance between instances in a feature array.
            If metric is a string, it must be one of the options allowed by
            sklearn.metrics.pairwise.pairwise_distances. If X is
            the distance array itself, use "precomputed" as the metric.

        copy (boolean, optional): Determines whether ``fit`` is used on
            **clf** or on a copy of **clf**.

        figsize (2-tuple, optional): Tuple denoting figure size of the plot
            e.g. (6, 6). Defaults to ``None``.

        cmap (string or :class:`matplotlib.colors.Colormap` instance, optional):
            Colormap used for plotting the projection. View Matplotlib Colormap
            documentation for available options.
            https://matplotlib.org/users/colormaps.html

        title_fontsize (string or int, optional): Matplotlib-style fontsizes.
            Use e.g. "small", "medium", "large" or integer-values. Defaults to
            "large".

        text_fontsize (string or int, optional): Matplotlib-style fontsizes.
            Use e.g. "small", "medium", "large" or integer-values. Defaults to
            "medium".
    """
    if cluster_ranges is None:
        cluster_ranges = range(1, 12, 2)
    else:
        cluster_ranges = sorted(cluster_ranges)

    if hasattr(clf, 'n_clusters'):
        clfs, times = train_different_hyperparam(clf, X, y = None, param_name ='n_clusters',
                                                 param_ranges = cluster_ranges, n_jobs = n_jobs)

    elif hasattr(clf, 'n_components'):
        clfs, times = train_different_hyperparam(clf, X, y = None, param_name ='n_components',
                                                 param_ranges = cluster_ranges, n_jobs = n_jobs)

    else:
        raise TypeError('"n_clusters" or "n_components" attribute not in classifier. '
                        'Cannot plot multiple silhouettes')


    rows, cols = plan_plot_grid(len(cluster_ranges))

    fig, axes = plt.subplots(rows, cols, figsize=figsize)
    walker = ax_walker(len(cluster_ranges), axes)
    fig.suptitle(title)

    for ax, k, clf in zip(walker, cluster_ranges, clfs):
        if hasattr(clf, 'labels_'):
            cluster_labels = clf.labels_  # cluster must have labels_ after training
        else:
            cluster_labels = clf.predict(X)

        plot_silhouette(X, cluster_labels, title = f'$k={k}$',
                    metric = metric, copy = copy, ax = ax,
                    cmap = cmap, title_fontsize = title_fontsize,
                    text_fontsize = text_fontsize)