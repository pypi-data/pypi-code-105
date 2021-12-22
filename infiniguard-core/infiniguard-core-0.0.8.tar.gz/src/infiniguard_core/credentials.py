import os
import json
import secrets
import string
import base64
from infiniguard_core.consts import SHARED_HOME

IGUARD_CREDENTIALS_STORE_PATH = f'{SHARED_HOME}/credstore'

IBOX_CREDENTIALS_KEY = 'ibox'
IDRAC_CREDENTIALS_KEY = 'idrac'
IGUARD_TENANT_NAME_KEY = 'tenant'


class CredentialsStoreException(Exception):
    pass


class CredentialsKeyNotFoundInStore(CredentialsStoreException):
    pass


class InvalidCredentials(CredentialsStoreException):
    pass


def generate_secret(chars, length=24):
    return ''.join(secrets.choice(chars) for _ in range(length))


def generate_credentials(username_chars=string.ascii_lowercase + string.digits,
                         password_chars=string.ascii_letters + string.digits + r"!@#$%^&*()~+-"):
    return generate_secret(username_chars, length=8), generate_secret(password_chars)


def _mask(text):
    return base64.b64encode(text.encode()).decode()


def _unmask(text):
    return base64.b64decode(text.encode()).decode()


def _load_store():
    try:
        with open(IGUARD_CREDENTIALS_STORE_PATH) as f:
            return json.load(f)
    except FileNotFoundError:
        return {}


def _save_store(store):
    os.makedirs(os.path.dirname(IGUARD_CREDENTIALS_STORE_PATH), exist_ok=True)
    with open(IGUARD_CREDENTIALS_STORE_PATH, 'w') as f:
        json.dump(store, f, indent=4)
    os.chmod(IGUARD_CREDENTIALS_STORE_PATH, 0o640)


def load_credentials(key):
    try:
        credentials = _load_store()[key]
    except KeyError:
        raise CredentialsKeyNotFoundInStore(f'Key "{key}" not found in credentials store.')
    return _unmask(credentials['username']), _unmask(credentials['password'])


def save_credentials(key, credentials):
    username, password = credentials
    if username is None or username == '':
        raise InvalidCredentials('Invalid username - None or empty')

    if password is None or password == '':
        raise InvalidCredentials('Invalid password - None or empty')

    store = _load_store()
    store[key] = {'username': _mask(username), 'password': _mask(password)}
    _save_store(store)
