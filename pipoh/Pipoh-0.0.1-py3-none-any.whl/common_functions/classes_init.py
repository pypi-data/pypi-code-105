import os
import pandas as pd
import numpy as np

# Input parameters of the model are introduced.
# By default, some parameters are introduce to help the usability of the final user.


class Data:
    emerging_markets = str(os.getcwd() + '/pipoh/data_library/6_Emerging_Markets_8years.csv')
    emerging_markets_2 = str(os.getcwd() + '/pipoh/data_library/6_Emerging_Markets_8years.csv')

    def __init__(self):
        ...

    def library_data(input_data='emerging_markets'):
        return np.matrix(pd.read_csv(eval('Data.'+input_data), header=None))

    def import_data(input_data):
        import_data = np.matrix(pd.read_csv(input_data, header=None))
        return import_data


