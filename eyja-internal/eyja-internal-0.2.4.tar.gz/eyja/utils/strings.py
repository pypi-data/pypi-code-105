import random
import string


def random_string(prefix = None, length=0):
    result = prefix if prefix else ''

    letters = string.ascii_lowercase + string.digits
    return f'{result}{"".join(random.choice(letters) for i in range(length-len(result)))}'
