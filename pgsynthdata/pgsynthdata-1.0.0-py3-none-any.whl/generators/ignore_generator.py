from ..datagenerator import ColumnPgInfo, Constraints, Statistics, generator

"""
Generator for Comment 'PGSYNTHDATA[IGNORE]'
Does nothing and ignores this Row
"""


@generator(
    None,
    comment_identifier="IGNORE",
)
def ignore_generator(
    stats: Statistics, column_info: ColumnPgInfo, constraints: Constraints, rows_to_gen
):
    pass
