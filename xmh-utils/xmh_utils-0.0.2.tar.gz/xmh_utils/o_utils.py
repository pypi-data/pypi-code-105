import datetime
import hashlib
import random
import re


def mun_to_str(num):
    """
    10000以内的数字转汉字
    """
    _MAPPING = (
        u'零', u'一', u'二', u'三', u'四', u'五', u'六', u'七', u'八', u'九', u'十', u'十一', u'十二', u'十三', u'十四', u'十五', u'十六',
        u'十七',
        u'十八', u'十九')
    _P0 = (u'', u'十', u'百', u'千',)
    assert (0 <= num and num < 10000)
    if num < 20:
        return _MAPPING[num]
    else:
        lst = []
        while num >= 10:
            lst.append(num % 10)
            num = num / 10
        lst.append(num)
        c = len(lst)  # 位数
        result = u''

        for idx, val in enumerate(lst):
            val = int(val)
            if val != 0:
                result += _P0[idx] + _MAPPING[val]
                if idx < c - 1 and lst[idx + 1] == 0:
                    result += u'零'
        return result[::-1]


def null_to_None(_str):
    """
    将文字的转换成对应的属性
    """
    if _str == "null":
        return None
    elif _str == "true":
        return True
    elif _str == "false":
        return False
    else:
        return None


def get_week_day(date, prefix="周"):
    """
    获取指定日期周几
    """
    week_day_dict = {
        0: f'{prefix}一',
        1: f'{prefix}二',
        2: f'{prefix}三',
        3: f'{prefix}四',
        4: f'{prefix}五',
        5: f'{prefix}六',
        6: f'{prefix}日',
    }
    day = date.weekday()
    return week_day_dict[day]


def check_mobile_phone(mobile_phone):
    """
    校验手机号
    """
    return re.match(r"^1[3456789]\d{9}$", mobile_phone)


def check_email(email):
    """
    校验邮箱格式
    """
    return re.match(r"^[A-Za-z0-9\u4e00-\u9fa5]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", email)


def clean_empty(d):
    """
    把所有为''的,转换成None
    """
    if not isinstance(d, (dict, list)):
        return d
    if isinstance(d, list):
        return [v for v in (clean_empty(v) for v in d)]
    return {k: v if v != '' else None for k, v in ((k, clean_empty(v)) for k, v in d.items())}


def get_file_path_md5(file_path):
    """
    获取文件md5
    """
    f = open(file_path, 'rb')
    md5_obj = hashlib.md5()
    while True:
        d = f.read(8096)
        if not d:
            break
        md5_obj.update(d)
    hash_code = md5_obj.hexdigest()
    f.close()
    md5 = str(hash_code).lower()
    return md5


def check_password_security_strength(password):
    """
        密码强度检查
    :param password:
    :return:
    """
    import string

    result = False
    score = 0
    msg = ''

    if len(password) < 8:
        result = False
        msg = '密码不能小于8个字符'
        return result, score, msg
    if len(password) > 20:
        result = False
        msg = '密码不能超过20个字符'
        return result, score, msg

    # 包含数字
    num_score = 0
    # 包含至少一个大写字母
    upper_case_score = 0
    # 包含至少一个小写字母
    lower_case_score = 0
    # 包含至少一个特殊符号 ~ ! @ # $ % ^ _ .
    symbol_list = ['~', '!', '@', '#', '$', '%', '^', '_', '.']
    symbol_score = 0

    for char in password:
        if char in string.digits:
            num_score = 1
        elif char in string.ascii_uppercase:
            upper_case_score = 1
        elif char in string.ascii_lowercase:
            lower_case_score = 1
        elif char in symbol_list:
            symbol_score = 1
        else:
            result = False
            msg = '密码包含不合法字符，请按照提示设置新密码'
            return result, score, msg

    score = num_score + upper_case_score + lower_case_score + symbol_score

    if score >= 2:
        result = True
        msg = '可用密码'
    else:
        result = False
        msg = '密码至少符合上述两项强度要求'

    return result, score, msg


def get_random_color():
    """
    获取随机色差
    """
    return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))


def repalce_blank(_str):
    """
    去除空格
    """
    return _str.replace(' ', '').replace('　', '')


def get_str_split(str):
    """
    逗号拼接的str转换成数组
    """
    if str == "":
        return []
    else:
        return str.split(",")


def get_every_day(start_date, end_date, format):
    """
    获取时间范围内根据指定格式返回
    """
    date_list = []
    while start_date <= end_date:
        date_str = start_date.strftime(format)
        date_list.append(date_str)
        start_date += datetime.timedelta(days=1)
    return date_list
