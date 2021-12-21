import pandas as pd
from textattack.datasets import Dataset
from textattack.datasets import HuggingFaceDataset


def dataframe_to_NLPDset(df, input_col_name, label_col_name):
    '''
    Takes in a dataframe and makes a textattack dataset.


    :param df: A dataframe.
    :param input_col_name: The name of the column containing the input values.
    :param label_col_name: The name of the column containing the labels.
    '''
    dset = []
    inputs = df[input_col_name].tolist()
    labels = df[label_col_name].tolist()
    for idx in range(len(inputs)):
        dpoint = (inputs[idx], labels[idx])
        dset.append(dpoint)
    dataset = Dataset(dset)
    return dataset

def MakeDataset(dset):
    return Dataset(dset)

def MakeHFDataset(*args, **kwargs):
    return HuggingFaceDataset(*args, **kwargs)
