################################################################################
# NOTE: this module is being deprecated, do not add new functionality
################################################################################

from .utils import requires


@requires("pyspark")
def url_to_adform_format(df,
                         input_col_name: str,
                         output_col_name: str
                         ):
    """
    Process domains to comply with AdForm format and crop it to domain/category.

    Process and crop the domains in :param input_col_name so that they are in
    compliance with AdForm format (no special characters, maximum length of
    100 characters) and also prepared for grouping (scheme removed, in
    lowercase) and cropped to domain/category.

    Examples
    --------

    .. code-block:: text

      INPUT DOMAIN:   https://www.sportcentral.cz/sportoviste/stolni-tenis/pardubice
      OUTPUT DOMAIN:  www.sportcentral.cz/sportoviste

      INPUT DOMAIN:   https://www.centrum.cz/?utm_source=mail.centrum.cz&utm_medium=referral
      OUTPUT DOMAIN:  www.centrum.cz

    :param df: dataframe containing the input_col_name column to be processed
    :type df: PySpark dataframe
    :param input_col_name: name of the column containing input URLs
    :param output_col_name: name of the column containing processed URLs

    :return df: the dataframe passed as parameter with a new output_col_name
        column containing the domains in the AdForm format
    :rtype: PySpark dataframe
    """

    import pyspark.sql.functions as F

    return (
        df
        .withColumn(output_col_name, F.lower(F.col(input_col_name)))
        # remove scheme (https/http) from domain
        .withColumn(
            output_col_name,
            F.regexp_replace(output_col_name, "^((https?|ftp)://)?", ""),
        )
        # removes "www" - should not be used, use on your own risk (if you don't know why,
        # ask Nikola Valesova or Michal Halenka)
        # .withColumn(
        #     output_col_name,
        #     F.regexp_replace(output_col_name, "^(ww+[^\.]*\.)?", "")
        # )
        # remove "." if it is the first character in domain
        .withColumn(output_col_name, F.regexp_replace(output_col_name, r"^\.", ""))
        # remove forbidden and all following characters from domain
        .withColumn(
            output_col_name,
            F.regexp_replace(
                output_col_name,
                '["' + r"~\!@#\$%\^&\*\(\)=+\\|\?<>\:'\[\]\{\} ,].*$",
                ""
            )
        )
        # crop to domain and category (+ a dot is not allowed after the first forward
        # slash)
        .withColumn(
            output_col_name,
            F.regexp_extract(output_col_name, "^[^/]+(/[^/.]+)?", 0),
        )
        # remove "m" indicating mobile phone
        .withColumn(output_col_name, F.regexp_replace(output_col_name, r"^m\.", ""))
        .withColumn(output_col_name, F.regexp_replace(output_col_name, r"\.m\.", "."))

        # crop domain to the first 100 characters
        .withColumn(
            output_col_name,
            F.when(
                F.length(F.col(output_col_name)) > 99,
                F.col(output_col_name).substr(0, 99),
            )
            .otherwise(F.col(output_col_name))
        )
        # remove trailing special char
        .withColumn(
            output_col_name,
            F.regexp_replace(output_col_name, r"[\.\-\/]$", ""),
        )
    )
