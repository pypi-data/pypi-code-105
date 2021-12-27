import datetime

def configure_date_range(date_start, date_end):
    """
    Determine start/end dates based on user input.

    Args:
        date_end (string): iso 8601 date value
        date_start (string): iso 8601 date value

    Returns:
        A tuple of start, end dateimte values.
    """

    # convert time
    dt_end = datetime.datetime.strptime(date_end, "%Y-%m-%d")
    dt_start = datetime.datetime.strptime(date_start, "%Y-%m-%d") if date_start and date_end and date_start != date_end else dt_end - datetime.timedelta(3)

    return (dt_start, dt_end)

def parse_multi_parameters(value):
    """
    Parse a string of comma-delimetered values into a native python list.

    Args:
        value (string): comma-delimetered value 
    
    Returns:
        A list of strings where each is a discrete value in the set.
    """

    return value.split(",") if value else list()
