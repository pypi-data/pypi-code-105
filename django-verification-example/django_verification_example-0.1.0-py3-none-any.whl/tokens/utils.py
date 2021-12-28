from datetime import timedelta

from django.conf import settings


def get_default_token_lifetime():
    """
    Возвращает длительность жизни по умолчанию для всех создаваемых
    токенов.

    Предполагается, что возвращаемое значение всегда будет объектом timedelta.
    """
    return getattr(settings, "DEFAULT_TOKEN_LIFETIME", timedelta(hours=1))


def get_numeric_code_length():
    """
    Возвращает необходимую длину для цифрового кода, определенную в настройках.

    На случай, если соответствующая опция не обнаружена, в качестве возвращаемого
    по умолчанию значения используется число 6, в связи с тем, что в современных
    системах для SMS чаще всего используются шестизначные цифровые коды.
    """
    return getattr(settings, "NUMERIC_CODE_LENGTH", 6)