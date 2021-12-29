from hashlib import md5


def str_transform(s: str):
    if not isinstance(s, str):
        return ''
    trans_str = md5(s.encode('utf-8')).hexdigest()
    return trans_str

