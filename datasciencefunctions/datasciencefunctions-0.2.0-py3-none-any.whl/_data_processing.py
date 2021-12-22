from .utils import _ERR_INVALID_DF_TYPE
from .utils import _ERR_SPLIT_COL_AND_NOT_COL_BASED

import logging

from ._utils import copy_docstring_from
# from ._utils import experimental
from ._utils import has_dependency
from ._utils import requires

from copy import deepcopy


# external dependencies go here (i.e. those not in standard library)
if has_dependency("sklearn"):
    # don't use "from" imports, would just clash with Spark
    import sklearn
    import sklearn.compose
    import sklearn.impute
    import sklearn.pipeline
    import sklearn.preprocessing

if has_dependency("pandas"):
    import pandas as pd

if has_dependency("pyspark"):
    import pyspark
    import pyspark.ml
    import pyspark.ml.feature
    import pyspark.sql.functions
# end of external dependencies


def fit_transformation_pipeline(train_data,
                                cat_cols: list = None,
                                num_cols: list = None,
                                skip_cols: list = None,
                                scaling: str = None,
                                ):
    """
    Constructs and fits transformation pipeline on training dataset.

    In case of Spark, prepares encoder, vector assembler and (optionally)
    scaler on a given dataframe. Scaling type (including no scaling) is
    determined by :param scaling. Equivalently for sklearn.

    :param train_data: training data
    :type train_data: PySpark dataframe, Pandas dataframe or list with the Pandas
        dataframe as the first element
    :param cat_cols: a list of column names of categorical features
    :param num_cols: a list of column names of numeric features
    :param skip_cols: names of columns to be excluded from the pipeline
    :param scaling: scaling type to be used: "noscale" (or None), "standard",
        "minmax" for Spark; sklearn uses StandardScaler currently
    :return: fitted pipeline object
    """
    # NOTE: docstring is copied into more specific functions, make sure to update it

    # TODO: !!! do not use handle invalid "skip", not for
    # production use, (probably) pass a dict with imputing strategies for
    # individual columns; if some columns not specified, write it as warning

    if (has_dependency("pyspark")
            and isinstance(train_data, pyspark.sql.dataframe.DataFrame)):
        return fit_transformation_pipeline_spark(
            train_data,
            cat_cols=cat_cols,
            num_cols=num_cols,
            skip_cols=skip_cols,
            scaling=scaling,
        )
    elif (has_dependency("pandas")
            and isinstance(train_data, (list, tuple))
            and isinstance(train_data[0], pd.core.frame.DataFrame)):
        return fit_transformation_pipeline_sklearn(
            train_data[0],
            cat_cols=cat_cols,
            num_cols=num_cols,
            skip_cols=skip_cols,
            scaling=scaling,
        )
    elif has_dependency("pandas") and isinstance(train_data, pd.core.frame.DataFrame):
        return fit_transformation_pipeline_sklearn(
            train_data,
            cat_cols=cat_cols,
            num_cols=num_cols,
            skip_cols=skip_cols,
            scaling=scaling,
        )
    # TODO: elif numpy ndarray? does it make sense?
    else:
        raise ValueError(_ERR_INVALID_DF_TYPE)


@requires("pyspark")
@copy_docstring_from(fit_transformation_pipeline)
def fit_transformation_pipeline_spark(train_data,
                                      cat_cols: list = None,
                                      num_cols: list = None,
                                      skip_cols: list = None,
                                      scaling: str = None,
                                      ):
    # NOTE: docstring copied from fit_transformation_pipeline, make sure to update it

    # make aliases, lazy programmer is good programmer
    import pyspark.sql.functions as F
    from pyspark.ml import Pipeline
    from pyspark.ml.feature import MinMaxScaler
    from pyspark.ml.feature import OneHotEncoder
    from pyspark.ml.feature import StandardScaler
    from pyspark.ml.feature import StringIndexer
    from pyspark.ml.feature import VectorAssembler

    # TODO:
    # * sanitization
    #   * fail if intersection of cat_cols and num_cols is not empty
    # * ...

    if skip_cols is None:
        skip_cols = []

    cat_cols = sorted(cat_cols) if cat_cols else []
    num_cols = sorted(num_cols) if num_cols else []

    # remove skip_cols from consideration
    cat_cols = [col for col in cat_cols if col not in skip_cols]
    num_cols = [col for col in num_cols if col not in skip_cols]

    # TODO: handle and test what happens when at least one of cat_cols, num_cols is empty

    for colname in cat_cols:
        # TODO: single select instead of withColumn (performance)
        train_data = train_data.withColumn(colname, F.col(colname).cast("string"))

    # string indexer for categorical features
    # Note: inputCols only in Spark 3, but can be a lot faster than chaining
    # indexers inf individual columns as is necessary in Spark 2
    cat_cols_indexed = [f'{colname}_indexed' for colname in cat_cols]
    indexer = StringIndexer(inputCols=cat_cols,
                            outputCols=cat_cols_indexed,
                            # skip because "keep" leads to multicollinearity
                            # even when no invalid data (extra column is always created)
                            handleInvalid="skip",
                            )

    # dummy features
    cat_cols_encoded = [f"{colname}_encoded" for colname in cat_cols]
    encoder = OneHotEncoder(inputCols=cat_cols_indexed,
                            outputCols=cat_cols_encoded,
                            dropLast=True,
                            )

    # scaling and pipeline
    if (scaling is None) or (scaling == "noscale"):
        # feature vector
        assembler = VectorAssembler(inputCols=num_cols + cat_cols_encoded,
                                    outputCol="features",
                                    )
        if len(encoder.getInputCols()) > 0:
            pipeline = Pipeline().setStages([indexer, encoder, assembler])
        else:
            pipeline = Pipeline().setStages([assembler])
    else:
        # feature vector
        assembler = VectorAssembler(inputCols=num_cols + cat_cols_encoded,
                                    outputCol="raw_features",
                                    )
        if scaling == "standard":
            scaler = StandardScaler(
                inputCol="raw_features",
                outputCol="features",
            )
        elif scaling == "minmax":
            scaler = MinMaxScaler(
                inputCol="raw_features",
                outputCol="features",
            )
        else:
            raise ValueError("Unknown scaler type name.")

        if len(encoder.getInputCols()) > 0:
            pipeline = Pipeline().setStages([indexer, encoder, assembler, scaler])
        else:
            pipeline = Pipeline().setStages([assembler, scaler])

    fitted_pipeline = pipeline.fit(train_data)

    return fitted_pipeline


@requires("sklearn")
@copy_docstring_from(fit_transformation_pipeline)
def fit_transformation_pipeline_sklearn(train_data,
                                        cat_cols: list = None,
                                        num_cols: list = None,
                                        skip_cols: list = None,
                                        scaling: str = None,
                                        ):
    # NOTE: docstring copied from fit_transformation_pipeline, make sure to update it

    # make aliases to reduce typing fatique
    Pipeline = sklearn.pipeline.Pipeline
    SimpleImputer = sklearn.impute.SimpleImputer
    OneHotEncoder = sklearn.preprocessing.OneHotEncoder
    StandardScaler = sklearn.preprocessing.StandardScaler
    ColumnTransformer = sklearn.compose.ColumnTransformer

    # TODO:
    # * sanitization
    #   * fail if intersection of cat_cols and num_cols is not empty
    # * ...

    if skip_cols is None:
        skip_cols = []

    cat_cols = sorted(cat_cols) if cat_cols else []
    num_cols = sorted(num_cols) if num_cols else []

    # remove skip_cols from consideration
    cat_cols = [col for col in cat_cols if col not in skip_cols]
    num_cols = [col for col in num_cols if col not in skip_cols]

    # TODO: handle and test what happens when at least one of cat_cols, num_cols is empty

    # features = train_data.columns
    # num_cols = [col for col in train_data.select_dtypes(include=["int64", "float64"]).columns if col in features]
    # cat_cols = [col for col in train_data.select_dtypes(include=["int64", "object"]).columns if col in features]

    cat_pipeline = Pipeline([
        ("imputer_cat", SimpleImputer(strategy="constant", fill_value="")),
        ("onehot", OneHotEncoder(handle_unknown="ignore"))
    ])

    num_pipeline = Pipeline([
        ("imputer", SimpleImputer(strategy="median")),
        ("scaler", StandardScaler()),
    ])

    preprocessing = ColumnTransformer(remainder="drop",
                                      transformers=[
                                          # categorical variables
                                          ("cat", cat_pipeline, cat_cols),
                                          # numerical variables
                                          ("num", num_pipeline, num_cols),
                                      ])

    pipeline = Pipeline(steps=[
        ("preprocessing", preprocessing),
    ])

    fitted_pipeline = pipeline.fit(train_data)

    return fitted_pipeline


def apply_transformation_pipeline(fitted_transformation_pipeline,
                                  train_data,
                                  test_data,
                                  ):
    """
    Apply transformation pipeline to train and test data separately.

    Note that type of output data copies that of input data (i.e. for Spark
    DataFrame it will be Spark DataFrame).

    :param fitted_transformation_pipeline: Spark or sklearn pipeline to be
        applied (should already be fitted on training data beforehand)
    :param train_data: training data to apply pipeline to
    :param test_data: testing data to apply pipeline to

    :return: transformed training and testing data
    """

    # TODO: meditate on this subject, I will (also check pipeline type, we should?)
    # TODO: ...should check both inputs simultaneously...
    if (has_dependency("pyspark")
            and isinstance(train_data, pyspark.sql.dataframe.DataFrame)):
        train_data = fitted_transformation_pipeline.transform(train_data)
        test_data = fitted_transformation_pipeline.transform(test_data)
        return train_data, test_data
    # IDEA: isiterable would be better probably?
    elif (has_dependency("pandas")
            and isinstance(train_data, (list, tuple))
            and isinstance(train_data[0], pd.core.frame.DataFrame)):
        # create new tuples, do not overwrite existing, leads to surprising problems...
        train_data_result = [
            fitted_transformation_pipeline.transform(train_data[0]),
            deepcopy(train_data[1]),
        ]
        test_data_result = [
            fitted_transformation_pipeline.transform(test_data[0]),
            deepcopy(test_data[1]),
        ]
        return train_data_result, test_data_result
    else:
        raise ValueError(_ERR_INVALID_DF_TYPE)


def train_test_split(df,
                     ratio: float = 0.7,
                     split_type: str = "random_split",
                     random_seed: int = None,
                     split_col: str = None,
                     ):
    """
    Splits the dataset into a training and testing set.

    Two variants are implemented, see split_type:
      - random train-test split
      - column-based train-test split (precompute a column with custom split assignment beforehand)

    :param df: dataframe to be split
    :type df: PySpark or Pandas dataframe
    :param ratio: train/test size ratio for random splitting
    :param split_type:  method of splitting data. Either
        "random_split" for randomly splitting data, or
        "column_based" (currently available for PySpark DataFrame only)
        for split based on split_col argument
    :param random_seed: random seed to be used for splitting, pass None for
        random result
    :param split_col: column to be used when split_type == "column_based" (IntegerType()
        column, 1 - train, 0 - test)

    :return: training dataframe, testing dataframe
    """
    # NOTE: docstring is copied into more specific functions, make sure to update it

    if (has_dependency("pyspark")
            and isinstance(df, pyspark.sql.dataframe.DataFrame)):
        return train_test_split_spark(
            df, ratio, split_type, random_seed, split_col=split_col
        )
    elif has_dependency("pandas") and isinstance(df, pd.core.frame.DataFrame):
        return train_test_split_pandas(
            df, ratio, split_type, random_seed, split_col=split_col
        )
    else:
        raise ValueError(_ERR_INVALID_DF_TYPE)


@requires("pyspark")
@copy_docstring_from(train_test_split)
def train_test_split_spark(df,
                           ratio: float = 0.7,
                           split_type: str = "random_split",
                           random_seed: int = None,
                           split_col: str = None,
                           ):
    # NOTE: docstring copied from train_test_split, make sure to update it

    import pyspark.sql.functions as F

    # input sanitization
    if split_col and split_type != "column_based":
        logging.info(_ERR_SPLIT_COL_AND_NOT_COL_BASED)

    if split_type == "random_split":
        df_train, df_test = df.randomSplit([ratio, 1 - ratio], seed=random_seed)
    elif split_type == "column_based":
        df_train = df.where(F.col(split_col) == 1)
        df_test = df.where(F.col(split_col) == 0)
    else:
        # TODO: implement split based on column values (e.g. time split?)
        #       ...would require setup with callbacks
        raise NotImplementedError(
            "split type '{split_type}' not supported in train_test_split_spark"
        )

    # # TODO: skip this altogether?? (potentially expensive calculation...
    # logging.info(f"Number of datapoints in the train dataset: {df_train.count()}")
    # logging.info(
    #     "Number of datapoints in the training dataset with label==1: "
    #     + f"{df_train.filter(F.col('label') == 1).count()}"
    # )
    # logging.info(f"Number of datapoints in the test dataset: {df_test.count()}")
    # logging.info(
    #     "Number of datapoints in the test dataset with label==1: "
    #     + f"{df_test.filter(F.col('label') == 1).count()}"
    # )

    return df_train, df_test


@requires("pandas")
@copy_docstring_from(train_test_split)
def train_test_split_pandas(df,
                            ratio: float = 0.7,
                            split_type: str = "random_split",
                            random_seed: int = None,
                            split_col: str = None,
                            ):
    # NOTE: docstring copied from train_test_split, make sure to update it

    # input sanitization
    if split_col and split_type != "column_based":
        logging.info(_ERR_SPLIT_COL_AND_NOT_COL_BASED)

    if split_type == "random_split":
        from sklearn.model_selection import train_test_split
        X = df.drop(["label"], axis=1)
        y = df["label"]

        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=1-ratio)

    elif split_type == "column_based":
        # TODO: implement this
        raise NotImplementedError(
            "split type '{split_type}' not supported in train_test_split_pandas"
        )
        raise NotImplementedError("Only 'random_split' is currently supported.")
    else:
        # TODO: implement split based on column values (e.g. time split?)
        raise NotImplementedError("Only 'random_split' is currently supported.")

    # logging.info(f"Number of datapoints in the train dataset: {X_train.shape[0]}")
    # logging.info(
    #     "Number of datapoints in the training dataset with label==1: "
    #     + f"{y_train.agg('sum')}"
    # )
    # logging.info(f"Number of datapoints in the test dataset: {X_test.shape[0]}")
    # logging.info(
    #     "Number of datapoints in the test dataset with label==1: "
    #     + f"{y_test.agg('sum')}"
    # )

    return [X_train, y_train], [X_test, y_test]


# TODO: pandas version?
@requires("pyspark")
def jlh(df_raw_text,
        data_col: str,
        doc_id_col: str,
        power_coef: float = 1,
        minDF: int = 3,
        ignore_duplicates: bool = True,
        ):
    """
    Calculate JLH score for input raw data containing documents (which will be  exploded into tokens).

    .. code-block:: text

        JLH = power_lift * diff

      where

        diff        =  foreground_pc - background_pc
        power_lift} = (foreground_pc / background_pc) ^ power_coef

    Terms "foreground" and "background" are similar to that of "term frequency" and "document frequency". For additional information
    see following article: https://opensourceconnections.com/blog/2016/09/09/better-recsys-elasticsearch/ .

    :param df_raw_text:       dataframe with raw data, expects column `label` with `1` or
        `0` designating "belongs to target class" and "doesn't belong to target class"
        respectively
    :type df_raw_text: PySpark dataframe
    :param data_col:          name of column containing raw data
    :param doc_id_col:        name of the document ID column
    :param power_coef:        exponent coefficient of (foreground_pc / background_pc ) in power_lift
    :param minDF:             minimum document frequency for including in calculation
    :param ignore_duplicates: treat all token occurences within one document as one?

    :return: PySpark dataframe with columns:

    .. code-block:: text

      token          column of tokens
      token_users    total number of documents where corresponding token occurs
      foreground_pc  percentage of term occurence in target documents
      background_pc  percentage of term occurence in all documents
      power_lift     (foreground_pc / background_pc) ^ power_coef
      diff           foreground_pc - background_pc
      JLH_score      power_lift * diff

    """
    from pyspark.sql.functions import explode, col, countDistinct, count

    if minDF < 0:
        raise ValueError("Invalid 'minDF' value. Expected >= 0, got '{}'".format(minDF))

    if power_coef <= 0:
        raise ValueError("Invalid 'power_coef' value. Expected >= 0, got '{}'".format(power_coef))

    df_dataset = (df_raw_text
                  .select(doc_id_col, data_col, "label")
                  .withColumn("token", explode(col(data_col)))
                  )

    if ignore_duplicates:
        count_all = df_dataset.groupBy().agg(countDistinct(doc_id_col)).collect()[0][0]
        count_target = df_dataset.filter(col("label") == 1).groupBy().agg(countDistinct(doc_id_col)).collect()[0][0]
    else:
        count_all = df_dataset.count()
        count_target = df_dataset.filter(col("label") == 1).count()

    df_background_set = (df_dataset
                         .groupBy("token")
                         .agg(count("*").alias("token_count"),
                              countDistinct(doc_id_col).alias("token_users")
                              )
                         .filter(col("token_users") > minDF)
                         .withColumn("background_pc",
                                     (col("token_users" if ignore_duplicates else "token_count") / count_all) * 100
                                     )
                         )

    df_foreground_set = (df_dataset
                         .filter(col("label") == 1)
                         .groupby("token")
                         .agg(countDistinct(doc_id_col).alias("token_users_target"),
                              count("*").alias("token_count_target")
                              )
                         .withColumn("foreground_pc",
                                     (col("token_users_target" if ignore_duplicates else "token_count_target") / count_target) * 100
                                     )
                         )

    df_jlh_set = (df_background_set
                  .join(df_foreground_set, "token", "inner")
                  .select("token", "token_users", "foreground_pc", "background_pc")
                  )

    df_jlh = (df_jlh_set
              .withColumn("power_lift", pow(col("foreground_pc") / col("background_pc"), power_coef))
              .withColumn("diff", col("foreground_pc") - col("background_pc"))
              .withColumn("JLH_score", col("power_lift") * col("diff"))
              )

    return df_jlh
