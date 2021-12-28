# https://github.com/pandas-profiling/pandas-profiling/blob/develop/src/pandas_profiling/controller/pandas_decorator.py
"""This file add the decorator on the DataFrame object."""

from collections.abc import Iterable

from pandas import DataFrame

def __assert_required_columns(df: DataFrame, *required):
    _missing = [col for col in required if col not in df]

    if _missing:
        raise KeyError(*_missing)

def __coulombic_efficiency(df: DataFrame):
    '''
        Calculate Coulombic Efficiency
        DataFrame should have cap_dchg, cap_chg Columns!
    '''
    __assert_required_columns(('cap_dchg', 'cap_chg'))

    return df['cap_dchg'] / df['cap_chg'] * 100

def __retention_from_1c_capacity(df: DataFrame):
    '''
        Calculate Retention from 1c Capacity
        DataFrame should have cap_dchg, cap_chg Columns!
    '''
    __assert_required_columns(('cap_dchg', 'c'))

    return df['cap_dchg'] / df['c'] * 100

def __retention_from_c_ref(df: DataFrame):
    '''
        Calculate Retention from c ref
        DataFrame should have cap_dchg, cap_chg Columns!
    '''
    __assert_required_columns(('cap_dchg', 'c_ref'))

    return df['cap_dchg'] / df['c_ref'] * 100

def __retention_normalized(df: DataFrame, cycle=3):
    '''
        Calculate Retention Normalized!
        DataFrame should have cap_dchg, cap_chg Columns!
    '''
    __assert_required_columns(df, 'test_id', 'cap_dchg', 'cycle') #Might want to check for test_capdchg
    
    # Retention Normalized computation
    def __retention_normalized_computation(row):
        try:
            _cycle = df[
                (df['test_id'] == row['test_id']) &
                (df['cycle'] == cycle)
            ]['cap_dchg'].iloc[-1]
            
        except IndexError:
            _cycle = df[
                (df['test_id'] == row['test_id'])
            ]['cap_dchg'].iloc[-1]
        
        
        return row['cap_dchg'] / _cycle * 100

    return df.apply(
        __retention_normalized_computation, 
        axis=1
    )

DataFrame.coulombic_efficiency = __coulombic_efficiency
DataFrame.retention_from_1c_capacity = __retention_from_1c_capacity
DataFrame.retention_from_c_ref = __retention_from_c_ref
DataFrame.retention_normalized = __retention_normalized
