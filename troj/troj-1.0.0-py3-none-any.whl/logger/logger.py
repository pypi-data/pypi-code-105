from collections import defaultdict


class Logger():
    def __init__(self, *args):
        self.logger_dict = defaultdict(list)
    
    """
    Return the logger 

    :return : the logger dict  
    """
    def get_logger(self):
        return self.logger_dict

    """
    Log a dictionary

    :param in_dict: a dictionary to be added to the logger
    """
    def log(self, in_dict):
        for key in in_dict.keys():
            self.logger_dict[key].append(in_dict[key])

    def log_to_dataframe(self, dataframe, index, log_dict):
        """
        Logs data to dataframe.

        :param dataframe: Dataframe to log to.
        :param index: The indices to log to.
        :param log_dict: A dictionary where the keys are column names, and the values are lists containing the values for the
        rows.
        :return: updated dataframe.
        """
        for key in list(log_dict.keys()):
            if key not in dataframe.columns:
                if type(log_dict[key]) == list:
                    dataframe[key] = [[] for i in range(len(dataframe))]
                else:
                    dataframe[key] = ""
                dataframe[key].astype("object")
            if type(log_dict[key]) == list and type(log_dict[key][0]) == list:
                for idx in range(len(list(index))):
                    if type(log_dict[key][idx]) == list:
                        for val in log_dict[key][idx]:
                            dataframe.loc[index[idx], key].append(val)
            else:
                dataframe.loc[index, key] = log_dict[key]
        return dataframe
        