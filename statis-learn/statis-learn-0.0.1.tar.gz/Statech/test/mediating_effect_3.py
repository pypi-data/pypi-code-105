import cmath
import itertools
import math

import numpy as np
import pandas as pd
from Statech.linear_model import MediatingEffect


def main(data):
    reg = MediatingEffect()
    reg.fit(data[['X1', 'X2', 'X3']], data['Y'], data[['M1', 'M2']], data[['Control1', 'Control2']])
    reg.score(data[['X1', 'X2', 'X3']], data['Y'], data[['M1', 'M2']], data[['Control1', 'Control2']])


if __name__ == '__main__':
    data =pd.read_excel('../data/am.xlsx')
    main(data)
