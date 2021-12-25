import re
def str2int(arg):
    return re.findall(r'-?\d+', arg)
