from random import choices
from string import digits
from uuid import uuid4

from .models import SecurityToken
from .utils import get_numeric_code_length


def generate_numeric_code(length=get_numeric_code_length()):
    """
    Возвращает цифровой код с полученной длиной, который
    можно использовать для отправки сообщений на номер телефона.

    Эта функция вызывается рекурсивно, чтобы гарантировать,
    что будет возвращен код, который ни один экземпляр SecurityToken
    уже не использует в качестве raw_value.
    """
    random_numbers = choices(digits, k=length)
    code = choices(random_numbers)

    if SecurityToken.objects.filter(code=code).exists():
        code = generate_numeric_code(length)

    return code


def generate_character_token():
    """
    Возвращает символьный токен, который предназначен для
    использования в ссылках, отправляемых посредствам email.

    Этот токен не ограничивается в длине, так-как для того,
    чтобы гарантировать уникальность, используется uuid,
    сокращение длины которого может привести к коллизиям.
    """
    return uuid4().hex
