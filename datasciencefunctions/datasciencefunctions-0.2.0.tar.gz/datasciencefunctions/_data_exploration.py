import copy
import logging
import math

from ._utils import copy_docstring_from
from ._utils import _get_active_spark_session
from .utils import _ERR_INVALID_DF_TYPE
from .utils import experimental
from .utils import has_dependency
from .utils import requires

# external dependencies go here (i.e. those not in standard library)
if has_dependency("pandas"):
    import pandas as pd

if has_dependency("pyspark"):
    import pyspark
    # TODO: consolidate _SPARK_VERSION checking, probably use LooseVersion etc.

    if pyspark.__version__.startswith("2"):
        _SPARK_VERSION = 2
        logging.warning("Spark version 2 is not officially supported, some things might break.")
    elif pyspark.__version__.startswith("3"):
        _SPARK_VERSION = 3
    else:
        logging.warning(
            "Spark version different from 2 and 3 detected. Unexpected errors might occur."
        )
if has_dependency("numpy"):
    import numpy as np
# end of external dependencies


# IDEA: it would be cleaner to have None's as defaults and leave that to downstream funcs
def get_categorical_and_numeric_cols(
        df,
        skip_cols: list = None,
        threshold: int = 10,
        approx: bool = False,
        max_error: float = 0.05,
):
    """
    Automatically separates columns into categorical and numeric based on
    type and number of distinct values.

    .. Note:: intended for exploration purposes, for production use, please make sure to
       specify column types explicitly (based on previous exploration).

    :param df: dataframe to be analysed
    :type df: PySpark dataframe, Pandas dataframe or list with the Pandas
        dataframe as the first element
    :param skip_cols: list of column names to exclude from analysis
    :param threshold: columns with at most this number of distinct values are considered categorical
    :param approx: for Spark version, if True use
        pyspark.sql.functions.approx_count_distinct to count distinct values
    :param max_error: maximum error when approx == True

    :return: (cat_cols, num_cols) lists of names of categorical and numeric valued columns
    """
    # NOTE: docstring is copied into more specific functions, make sure to update it

    if (has_dependency("pyspark")
            and isinstance(df, pyspark.sql.dataframe.DataFrame)):
        return get_categorical_and_numeric_cols_spark(
            df, skip_cols, threshold, approx, max_error
        )
    elif (has_dependency("pandas")
          and isinstance(df, (list, tuple))
          and isinstance(df[0], pd.core.frame.DataFrame)):
        return get_categorical_and_numeric_cols_pandas(
            df, skip_cols, threshold, approx, max_error
        )
    elif has_dependency("pandas") and isinstance(df, pd.core.frame.DataFrame):
        return get_categorical_and_numeric_cols_pandas(
            df, skip_cols, threshold, approx, max_error
        )
    # TODO: elif numpy ndarray? does it make sense?
    else:
        raise ValueError(_ERR_INVALID_DF_TYPE)


@requires("pyspark")
@copy_docstring_from(get_categorical_and_numeric_cols)
def get_categorical_and_numeric_cols_spark(
        df,
        skip_cols: list = None,
        threshold: int = 10,
        approx: bool = False,
        max_error: float = 0.05,
):
    # NOTE: docstring copied from get_categorical_and_numeric_cols, make sure to update it
    import pyspark.sql.functions as F

    cols = df.columns

    # sanitize user input
    if skip_cols is None:
        skip_cols = []

    cols = [col for col in cols if col not in skip_cols]

    cat_cols = []
    num_cols = []

    if approx:
        agg_expressions = [F.approx_count_distinct(F.col(colname), rsd=max_error).alias(colname) for colname in cols]
    else:
        agg_expressions = [F.countDistinct(F.col(colname)).alias(colname) for colname in cols]

    dict_counts = df.groupBy().agg(*agg_expressions).toPandas().to_dict()
    counts = {key: value[0] for key, value in dict_counts.items()}  # extract first (only) row
    for col in cols:
        cnt = counts[col]

        if (cnt <= threshold):
            cat_cols.append(col)
        elif (df.select(col).dtypes[0][1] == 'string'):
            logging.info(
                f"Column '{col}' has type String but has more than '{threshold}' "
                + "unique values. This column was skipped."
            )
        else:
            num_cols.append(col)

    return (cat_cols, num_cols)


@requires("pandas")
@copy_docstring_from(get_categorical_and_numeric_cols)
def get_categorical_and_numeric_cols_pandas(
        df,
        skip_cols: list = None,
        threshold: int = 10,
        approx: bool = False,
        max_error: float = 0.05,
):
    # NOTE: docstring copied from get_categorical_and_numeric_cols, make sure to update it

    if isinstance(df, pd.core.frame.DataFrame):
        pass  # passed df already a Pandas dataframe
    elif (isinstance(df, (list, tuple))
          and isinstance(df[0], pd.core.frame.DataFrame)):
        df = df[0]
    # TODO: elif numpy ndarray? does it make sense?
    else:
        raise ValueError(
            "Expected df to be either Pandas DF or list/tuple containing Pandas DF as the"
            " first element"
        )

    # sanitize user input
    if skip_cols is None:
        skip_cols = []

    if approx:
        logging.info("Ignoring 'approx' parameter for Pandas data.")

    cols = [col for col in df.columns if col not in skip_cols]

    counts = {
        colname: df[colname].nunique()
        for colname in cols
    }

    cat_cols = [
        col for col in cols
        if counts[col] <= threshold or df[col].dtypes == "object"
    ]
    num_cols = [
        col for col in cols
        if counts[col] > threshold and df[col].dtypes != "object"
    ]
    # TODO: uncomment the original warning about skipped string columns with too many
    # unique values?
    # for col in cols:
    #     cnt = counts[col]

    #     if (cnt <= threshold):
    #         cat_cols.append(col)
    #     elif (df[col].dtypes == "object"):
    #         print("Column '{0}' has type String but has more than '{1}' unique values. This column was skipped."
    #               .format(col, str(threshold)))
    #     else:
    #         num_cols.append(col)

    return (cat_cols, num_cols)


@experimental  # noqa C901
@requires("pandas", "matplotlib", "numpy")  # noqa C901
def plot_feature_hist_with_binary_target(  # noqa C901
        df,
        target_col: str,
        cat_cols: list = None,
        num_cols: list = None,
        num_binning_method=None,
        figsize: tuple = (20, 10),
        fig_hspace: float = 0.35,
        use_cache: bool = True,
        autoscale_y: bool = False,
        category_sample_threshold: int = None,
):
    """
    Displays the distribution of binary target variable over various feature domains.

    Features are processed separately and rendered as individual plots as part of a single
    figure. Numerical features are bucketized based on specified method/strategy (see
    example below and documentation of histogram_bin_splits for more information).

    On each plot, left y-axis shows the total number of samples in a given category/bin
    and on the right y-axis, there is the percentage of samples with target==1. Left
    y-axis scaling is independent while right y-axis (target percentage) scale is shared
    accross all plots for clarity.

    :param df: Spark or Pandas DataFrame
    :param target_col: name of column containing targets (must contain only values 0
        and 1)
    :param cat_cols: list of categorical features to plot
    :param num_cols: list of numerical features to first bucketize and then plot
    :param num_binning_method: how to treat numerical columns. Allows for different
        values of granularity for both convenience and customization. Example below.
    :param figsize: figure size defined in a tuple (default: (20, 8))
    :param fig_hspace: adjust when you need to change spacing between plots. It expresses
        spacing as a fraction of the figsize height.
    :param use_cache: set True to cache the input dataframe (only for spark)
    :param autoscale_y: if True, scale target percentage y-axis based on data (shared
        across all plots). Default False
    :param category_sample_threshold: threshold for number of samples in a category to be
        displayed (not used for num_cols, only for cat_cols). Default is None (no
        threshold is applied)
    :return: figure containing the plots

    Example of different options for specifying 'num_binning_method':

    .. code-block:: python

        num_binning_method=None  # uses default for num_cols

        num_binning_method='freedman-diaconis'  # uses freedman-diaconis for num_cols

        num_binning_method={
            # specifies method per-column (with or without additional args)
            # remaining num_cols use default
            'col1': 'freedman-diaconis',
            'col2': 'equidistant',
            'col3': {'how': 'equidistant', 'num_bins': 10},
            'col4': {'how': 'custom', 'bin_splits': [-5, -0.7, 1.9, 4]},
        }
    """

    # TODO: 'autoscale_y' param... should we allow both ends (lower, upper) to be
    # autoscaleable??

    # TODO: 'figure_kwargs' for extra kwargs??

    import matplotlib.pyplot as plt

    cat_cols = list(cat_cols) if cat_cols is not None else []
    num_cols = list(num_cols) if num_cols is not None else []

    # TODO: move this into separate helper function for parsing num_binning_method arg
    # num_binning_method resolution
    if num_binning_method is None:
        num_binning_method = {col: {} for col in num_cols}
    if isinstance(num_binning_method, str):
        num_binning_method = {col: {'how': num_binning_method} for col in num_cols}
    elif isinstance(num_binning_method, dict):
        num_binning_method = copy.deepcopy(num_binning_method)

        for col in num_cols:
            if col in num_binning_method:
                if isinstance(num_binning_method[col], str):
                    num_binning_method[col] = {'how': num_binning_method[col]}
            else:
                num_binning_method[col] = {}

    feature_cols = cat_cols + num_cols
    num_graphs = len(feature_cols)

    for col in feature_cols:
        if col in cat_cols and col in num_cols:
            raise ValueError(f'Column {col} is present in both cat_cols and num_cols.')

        if col not in df.columns:
            raise ValueError(f'Column {col} is present in cat_cols or num_cols but is not '
                             'present in the dataframe columns: {df.columns}')

    fig, axes = plt.subplots(
        num_graphs, 1, figsize=(figsize[0], num_graphs * (figsize[1]))
    )
    fig.subplots_adjust(hspace=fig_hspace)

    if num_graphs == 1:
        axes = [axes]

    framework = 'pandas' if _is_pandas(df) else 'spark'

    if use_cache and framework == 'spark':
        df = df.cache()

    ymax = 0

    twinx_axes = dict()
    for idx, col in enumerate(feature_cols):
        if col in num_cols:
            bin_splits, quantiles = histogram_bin_splits(df, col, **num_binning_method[col])
            aux = bucketize_column(df, col, bin_splits)

            if framework == 'pandas':
                aux = aux.groupby([f"{col}_bin_id", f"{col}_bin_desc"])
            else:
                aux = aux.groupby(f"{col}_bin_id", f"{col}_bin_desc")

            col_feature = f"{col}_bin_desc"
            col_sort = f"{col}_bin_id"
        else:
            aux = df.groupby(col)
            col_feature = col
            col_sort = col

        statistics = _get_target_dist_statistics(aux, target_col, col_sort)

        if category_sample_threshold is not None:
            statistics = statistics[statistics.SUM > category_sample_threshold]

        ymax = max(ymax, statistics['PCNT_TARGET'].max())

        _, _, twinx = target_dependency_histogram(
            statistics,
            col_feature,
            "SUM",
            "PCNT_TARGET",
            title=col,
            ax=axes[idx],
        )
        twinx_axes[col] = twinx

    if not autoscale_y:
        ymax = 1.0

    for twinx_ax in twinx_axes.values():
        ticks = [tick for tick in np.linspace(0, ymax, 11)]
        tick_labels = [str(round(tick, 2)) for tick in ticks]
        twinx_ax.set_yticks(ticks)
        twinx_ax.set_yticklabels(tick_labels)

    return fig


def _get_target_dist_statistics(df, label_col_name, col_sort):
    # TODO: change this - assumption we have Pandas and that non-Pandas means Spark
    if _is_pandas(df):
        return _get_target_dist_statistics_pandas(df, label_col_name, col_sort)
    else:
        return _get_target_dist_statistics_spark(df, label_col_name, col_sort)


def _get_target_dist_statistics_spark(df, label_col_name, col_sort):
    import pyspark.sql.functions as F
    return (
        df
        .agg(F.count("*").alias("SUM"), F.sum(label_col_name).alias("1"))
        .withColumn("PCNT_TARGET", F.col("1") / F.col("SUM"))
        .orderBy(col_sort)
    ).toPandas()


def _get_target_dist_statistics_pandas(df, label_col_name, col_sort):
    df = (
        df
        .agg({label_col_name: ['count', 'sum']})
        .reset_index(drop=False)
    )
    df['SUM'] = df[(label_col_name, 'count')]
    df['PCNT_TARGET'] = df[(label_col_name, 'sum')] / df['SUM']
    df = df.sort_values(col_sort)
    return df


@requires("matplotlib", "seaborn")
def target_dependency_histogram(
        pd_df,
        col_name_x: str,
        col_name_y1: str,
        col_name_y2: str,
        title: str = None,
        subtitle: str = None,
        ax=None,
        figsize: tuple = (20, 8),
):
    """
    Creates bar plot and line plot for columns x, y1, and y2, and returns the Figure
    (is None when ax parameter is provided) and axes.

    Uses seaborn and matplotlib to create the plot.

    :param pd_df: pandas Dataframe
    :param col_name_x: name of column x that represents labels of x-axis (category labels)
    :param col_name_y1: name of column y1 that represents values of y-axis of BarPlot (category sample counts)
    :param col_name_y2: name of column y2 that represents values of y-axis of LinePlot (target percentage in category)
    :param title: sets plot title, default is an empty string
    :param subtitle: sets plot subtitle, default is an empty string
    :param ax: optional parameter for plotting the histogram onto an existing Figure. This
        results in the first return value being set to None.
    :return: fig, ax, ax.twinx() - the plot components. fig == None when ax != None.
    """

    import seaborn as sns
    import matplotlib.pyplot as plt

    if not ax:
        fig, ax = plt.subplots(1, 1, figsize=figsize)
    else:
        fig = None

    title = title or ""
    subtitle = subtitle or ""

    ax.set_title("\n".join([title, subtitle]), fontsize=14)

    bar_chart = sns.barplot(
        x=col_name_x,
        y=col_name_y1,
        data=pd_df,
        ax=ax,
        order=pd_df[col_name_x].values,
    )

    ax_twin = ax.twinx()

    sns.lineplot(
        x=range(len(pd_df)),
        y=col_name_y2,
        data=pd_df,
        ax=ax_twin,
        color="black",
        sort=False,
    )

    bar_chart.set_xticklabels(
        bar_chart.get_xticklabels(),
        rotation=45,
        horizontalalignment="right",
    )

    return fig, ax, ax_twin


@requires("numpy")
def histogram_bin_splits(df, colname, how: str = "freedman-diaconis", num_bins: int = 20, bin_splits=None):
    """
    Calculate bin splits of numerical column and return it along with quantiles.

    There are several methods for how the splits should be calculated. For consistency
    with other functions, there is 'custom' which only takes existing bin splits and
    checks the sequence monotonicity.

    For other options, 0.05 and 0.95 quantiles are used for the minimum and maximum bin
    edges respectively (excluding infinities) to increase robustness to outliers.
    'equidistant' simply distributes edges to get num_bins buckets of same width.

    'freedman-diaconis' uses heuristic based on "inter-quantile range" to determine
    optimal bin width. :param num_bins is ignored for this method. More information can be
    found on `wiki page <https://en.wikipedia.org/wiki/Freedman%E2%80%93Diaconis_rule>`_.

    Quantiles are returned as a dictionary for information purposes. Specific quantiles
    are implementation detail and subject to change (e.g. might change from 0.05
    to 0.1 quantile).

    :param df: Spark or Pandas DataFrame
    :param colname: name of column to calculate bin splits for
    :param how: method for calculating bin splits, one of "custom", "equidistant", and
        "freedman-diaconis"
    :param num_bins: number of bins to create (ignored in some methods)
    :param bin_splits: existing bin splits, only for "custom" method, ignored otherwise
    :return: bin_splits, quantiles
    """

    # TODO: document -inf and +inf behaviour. Think about adding it to custom with kwarg?
    # IDEA: add centers at some point... (instead of edges)

    # TODO: remove import, it's already imported at the top
    import numpy as np

    quantile_q = [0.05, 0.25, 0.5, 0.75, 0.95]

    # TODO: change this - assumption we have Pandas and that non-Pandas means Spark
    if _is_pandas(df):
        quantile_values = df[colname].quantile(quantile_q).values.tolist()
        nrows = len(df)
    else:
        quantile_values = df.approxQuantile(colname, quantile_q, 0.01)
        nrows = df.count()

    quantiles = {
        q: val for (q, val)
        in zip(quantile_q, quantile_values)
    }

    if how == "freedman-diaconis":
        iqr = quantiles[0.75] - quantiles[0.25]  # inter-quantile range
        bin_width = 2 * iqr / (nrows ** (1 / 3))  # Freedman-Diaconis rule

        split_start = quantiles[0.05]
        split_end = quantiles[0.95] + bin_width / 2

        if bin_width == 0:
            n_bins = 1
        else:
            n_bins = int(math.ceil((split_end - split_start) / bin_width)) + 1

        bin_splits = (
                [-float("inf")]
                + np.linspace(
                    split_start,
                    split_end,
                    n_bins
                ).tolist()
                + [+float("inf")]
        )

    elif how == "equidistant":
        bin_width = (quantiles[0.95] - quantiles[0.05]) / (num_bins - 1)
        bin_splits = (
                [-float("inf")]
                + np.linspace(
                    quantiles[0.05],
                    quantiles[0.95] + bin_width / 2,
                    max(0, num_bins - 1),
                ).tolist()
                + [+float("inf")]
        )
    elif how == "custom":
        for i in range(len(bin_splits) - 1):
            if bin_splits[i] >= bin_splits[i + 1]:
                raise ValueError(f'bin_splits have to be an increasing numeric sequence but is: {bin_splits}')
    else:
        raise ValueError(f"Argument 'how' got an invalid value '{how}'")

    return bin_splits, quantiles


def _get_bin_desc_helper(bin_splits):
    """
    A helper function that turns a list of bin splits
    into a list of string, human readable labels of bins.

    Used in `bucketize_column()`.

    > _get_bin_desc_helper(bin_splits=[-inf, 3, 7, inf])
    ["(-inf, 3)", "(3, 7)", "(7, inf)"]
    """

    if len(bin_splits) > 3:
        mean_width = (
                sum(
                    split_right - split_left for (split_left, split_right)
                    in zip(bin_splits[1:-2], bin_splits[2:-1])
                )
                / (len(bin_splits) - 3)
        )
    else:
        mean_width = 0.5  # pozdravy z Bulharska

    precision = -round(math.log10(mean_width)) + 2
    bin_desc = [
        f"({round(bin_splits[_i], precision)}, {round(bin_splits[_i + 1], precision)})"
        for _i in range(len(bin_splits) - 1)
    ]

    return bin_desc


def bucketize_column(df, colname, bin_splits):
    """
    Bucketize given column and add it as new columns '{colname}_bin_id' and '{colname}_bin_desc.'

    Bucketize column specified by colname to bins with edges from bin_splits and add
    this information as new columns of the original dataframe.

    :param df: Spark or Pandas DataFrame
    :param colname: column to bucketize
    :param bin_splits: split points from which bin intervals will be created
    :return: df with added columns {colname}_bin_id, {colname}_bin_desc
    """

    # TODO: add option "inplace" (or "in_place"), otherwise we're either wasting RAM or
    # modifying the original dataframe (only Pandas is affected)

    # TODO: change this - assumption we have Pandas and that non-Pandas means Spark
    if _is_pandas(df):
        return _bucketize_column_pandas(df, colname, bin_splits)
    else:
        return _bucketize_column_spark(df, colname, bin_splits)


@requires("pyspark")
@copy_docstring_from(bucketize_column)
def _bucketize_column_spark(df, colname, bin_splits):

    from pyspark.ml.feature import Bucketizer

    bucketizer = Bucketizer(
        splits=bin_splits,
        inputCol=colname,
        outputCol=f"{colname}_bin_id",
        handleInvalid="skip",
    )

    df_bucketized = bucketizer.transform(df)

    bin_desc = _get_bin_desc_helper(bin_splits)

    spark = _get_active_spark_session()

    df_bin_desc = spark.createDataFrame(
        zip(range(len(bin_desc)), bin_desc),
        schema=f"{colname}_bin_id INT, {colname}_bin_desc string",
    )

    df_bucketized = df_bucketized.join(
        df_bin_desc,
        on=f"{colname}_bin_id",
        how="left",
    )

    return df_bucketized


@requires("pandas")
@copy_docstring_from(bucketize_column)
def _bucketize_column_pandas(df, colname, bin_splits):
    df_bucketized = df.dropna(subset=[colname])

    outcol = f"{colname}_bin_id"
    values = df_bucketized[colname].values
    df_bucketized.loc[:, outcol] = -1

    for category, (start, end) in enumerate(zip(bin_splits[:-1], bin_splits[1:])):
        mask = (start < values) & (values <= end)
        df_bucketized.loc[mask, outcol] = category

    bin_desc = _get_bin_desc_helper(bin_splits)

    df_bin_desc = pd.DataFrame(
        {
            f'{colname}_bin_id': range(len(bin_desc)),
            f'{colname}_bin_desc': bin_desc
        })

    df_bucketized = df_bucketized.merge(
        df_bin_desc,
        on=f"{colname}_bin_id",
        how="left",
    )

    return df_bucketized


def _is_pandas(df):
    return isinstance(df, (pd.DataFrame, pd.core.groupby.DataFrameGroupBy))


@experimental  # noqa: C901, TODO: simplify this
@requires("pyspark")  # noqa: C901, TODO: simplify this
def profile_dataframe(df,  # noqa: C901, TODO: simplify this
                      use_cache: bool = True,
                      spark=None,
                      ):
    """
    Run basic analysis of given dataframe. Current information collected for each column
    is (in order):

        * ROWS_TOTAL,
        * ROWS_NOT_NULL,
        * NULL_RATE,
        * AVG,
        * MIN,
        * MAX,
        * 25_PERCENTILE,
        * 50_PERCENTILE,
        * 75_PERCENTILE,

    :param df: Spark Dataframe that should be analysed
    :type df: PySpark dataframe
    :param use_cache: use Spark's `cache` to keep the dataframe to memory
    :param spark: SparkSession instance, required for Spark 2, can be infered for Spark 3
            if not provided

    :return: dataframe with one row for each analyzed column
    :rtype: PySpark dataframe
    """
    import pyspark.sql.functions as F

    if spark is None:
        if _SPARK_VERSION == 2:
            raise ValueError("Spark version 2 detected but SparkSession not provided.")
        elif _SPARK_VERSION == 3:
            logging.info("SparkSession not provided, infering with getActiveSession")
            from pyspark.sql import SparkSession
            spark = SparkSession.getActiveSession()
        else:
            raise ValueError("SparkSession not provided and Spark version not infered.")

    # TODO: make this into a PySpark plan (not using collect) so that it runs inside one
    #       whole-stage codegen

    def __get_dtype(df, column_name: str):
        return [dtype for name, dtype in df.dtypes if name == column_name][0]

    # TODO:
    #  * `skip_comparison_aggregations` param --> only calculate `avg` and quantiles for
    #    columns whose type permits comparison (i.e. where it makes sense and doesn't
    #    throw an error)
    #  * remove __column_*_agg functions, they are unnecessary (just call __get_row
    #    directly doing column transformations where appropriate
    def __get_row(df, column_name: str):
        return df.agg(
            F.count(column_name).alias("count_not_null"),
            F.avg(column_name).alias("avg"),
            F.min(column_name).alias("min"),
            F.max(column_name).alias("max"),
            F.expr(f"percentile({column_name}, 0.25)").alias("25_PERCENTILE"),
            F.expr(f"percentile({column_name}, 0.50)").alias("50_PERCENTILE"),
            F.expr(f"percentile({column_name}, 0.75)").alias("75_PERCENTILE"),
        ).collect()[0]

    def __column_numeric_agg(df, column_name: str):
        row = __get_row(df, column_name)
        return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

    def __column_string_agg(df, column_name: str):
        row = __get_row(df, column_name)
        return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

    def __column_boolean_agg(df, column_name: str):
        df = df.withColumn(column_name, F.col(column_name).cast("integer"))
        row = __get_row(df, column_name)
        return row[0], row[1], row[2], row[3], row[4], row[5], row[6]

    def __column_other_agg(df, column_name: str):
        row = df.agg(
            F.count(column_name).alias("count_not_null"),
            # F.avg(column_name).alias("avg"), #not for date timestamp
            F.min(column_name).alias("min"),
            F.max(column_name).alias("max"),
        ).collect()[0]
        return row[0], row[1], row[2]

    # Start of the function
    if use_cache:
        df.cache()

    rows_total = df.count()
    df_schema = [
        "COLUMN_NAME",
        "COLUMN_TYPE",
        "ROWS_TOTAL",
        "ROWS_NOT_NULL",
        "AVG",
        "MIN",
        "MAX",
        "25_PERCENTILE",
        "50_PERCENTILE",
        "75_PERCENTILE",
    ]

    df_profile = None
    padding = math.ceil(math.log10(len(df.columns) + 1))
    for counter, column in enumerate(df.columns):

        logging.info(
            f"{str(counter).rjust(padding)}/{len(df.columns)}: "
            + f"Processing column '{column}'"
        )
        col_dtype = __get_dtype(df, column)
        if col_dtype.startswith(("decimal", "int", "float", "long", "bigint", "double")):
            (
                count_not_null,
                avg,
                min,
                max,
                percentile25,
                percentile50,
                percentile75,
            ) = __column_numeric_agg(df, column)
        elif col_dtype.startswith("string"):
            (
                count_not_null,
                avg,
                min,
                max,
                percentile25,
                percentile50,
                percentile75,
            ) = __column_string_agg(df, column)
        elif col_dtype.startswith("boolean"):
            (
                count_not_null,
                avg,
                min,
                max,
                percentile25,
                percentile50,
                percentile75,
            ) = __column_boolean_agg(df, column)
        else:
            count_not_null, min, max = __column_other_agg(df, column)
            avg = "None"
            percentile25 = "None"
            percentile50 = "None"
            percentile75 = "None"

        values = [
            (
                [
                    f"{column}",
                    f"{col_dtype}",
                    f"{rows_total}",
                    f"{count_not_null}",
                    f"{avg}",
                    f"{min}",
                    f"{max}",
                    f"{percentile25}",
                    f"{percentile50}",
                    f"{percentile75}",
                ]
            )
        ]

        df_profile_tmp = spark.createDataFrame(values, schema=df_schema)

        df_profile = (
            df_profile.union(df_profile_tmp)
            if df_profile is not None else df_profile_tmp
        )

    df_null_rate = df_profile.withColumn(
        "NULL_RATE",
        F.round(
            F.when(
                (F.col("ROWS_TOTAL") - F.col("ROWS_NOT_NULL")) == 0, 0,
            )  # all filled values
            .when(
                F.col("ROWS_NOT_NULL") == F.col("ROWS_TOTAL"), 1
            )  # all values null
            .when(
                F.col("ROWS_TOTAL") > 0,
                (F.col("ROWS_TOTAL") - F.col("ROWS_NOT_NULL")) / F.col("ROWS_TOTAL"),
            )
            .otherwise(0),
            2,
        ),
    )

    return df_null_rate.select(
        "COLUMN_NAME",
        "COLUMN_TYPE",
        "ROWS_TOTAL",
        "ROWS_NOT_NULL",
        "NULL_RATE",
        "AVG",
        "MIN",
        "MAX",
        "25_PERCENTILE",
        "50_PERCENTILE",
        "75_PERCENTILE",
    )


@requires("pyspark")
def probability_calibration_table(
    df_predictions,
    thresholds: list = None,
    prediction_col: str = "prediction",
    label_col: str = "label",
    probability_col: str = "probability"
):
    """
    Calibration of classification model probabilities.

    Computes the actual probability (accuracy) vs. probability reported
    by a model, for each bin separated by list_thresholds.

    This is useful to be check whether probabilities returned by a model
    can be interpreted as actual probabilities. Some models e.g. overestimate
    the actual probability by a lot.

    Works for binary and multiclass classification.

    :param df_predictions: PySpark DataFrame with model predictions
    :param thresholds: list of thresholds between bins of reported and
        actual probabilities
    :param prediction_col: name of column with predicted label
    :param label_col: name of column with true label
    :param probability_col: name of column with predicted probability

    :return: DataFrame with reported vs. actual probabilities per bin
    """
    import pyspark.sql.functions as F
    import pyspark.sql.types as T
    from pyspark.sql import Window
    from functools import reduce

    if thresholds is None:
        thresholds = [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 0.95, 0.99, 0.999, 0.9999]

    df_calibration = (
        df_predictions
        .withColumn('is_correct', (F.col(label_col) == F.col(prediction_col)).cast(T.ByteType()))
        .withColumn(
            'confidence_lower',
            reduce(
                lambda cond, threshold: cond.when(F.col(probability_col) >= threshold, threshold),
                sorted(thresholds, reverse=True),
                F.when(F.lit(False), F.lit(42))  # Hack to initialize when expression
            ).otherwise(F.lit(0))
        )
        .groupBy('confidence_lower')
        .agg(
            F.count('*').alias('count'),
            F.avg('is_correct').alias('accuracy')
        )
        .withColumn('confidence_upper', F.lead('confidence_lower').over(Window.orderBy('confidence_lower')))
        .withColumn('confidence_label', F.concat(F.lit('< '), F.col('confidence_upper')))
        .na.fill(1, ['confidence_upper'])
        .withColumn('confidence_mean', (F.col('confidence_lower') + F.col('confidence_upper')) / 2)
        .withColumn(
            'confidence_label',
            F.when(F.col('confidence_label').isNotNull(), F.col('confidence_label'))
            .otherwise(F.concat(F.lit('>= '), F.col('confidence_lower')))
        )
        .orderBy('confidence_lower')
        .select('confidence_label', 'confidence_lower', 'confidence_upper', 'confidence_mean', 'accuracy', 'count')
    )

    return df_calibration
