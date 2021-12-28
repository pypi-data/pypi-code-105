# https://github.com/pandas-profiling/pandas-profiling/blob/develop/src/pandas_profiling/controller/pandas_decorator.py

"""This file add the decorator on the DataFrame object."""
from pandas import DataFrame

def coulombic_efficiency(self):
    if not all(col in self for col in ('cap_dchg', 'cap_chg')):
        return

    return self['cap_dchg'] / self['cap_chg'] * 100


DataFrame.coulombic_efficiency = coulombic_efficiency