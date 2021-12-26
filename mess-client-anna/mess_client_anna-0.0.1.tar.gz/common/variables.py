import logging

# Порт по умолчанию для сетевого ваимодействия
DEFAULT_PORT = 7777

# IP адрес по умолчанию для подключения клиента
DEFAULT_IP_ADDRESS = '127.0.0.1'

# Максимальная очередь подключений
MAX_NUMBER_CONNECTIONS = 5

# Максимальная длинна сообщения в байтах
MAX_MESSAGE_LENGTH = 1024

# Кодировка проекта
ENCODING = 'utf-8'

# Текущий уровень логирования
LOGGING_LEVEL = logging.DEBUG

# База данных для хранения данных сервера:
SERVER_DATABASE = 'sqlite:///server_base.db3'

# База данных для хранения данных сервера:
SERVER_CONFIG = 'server.ini'

# Прококол JIM основные ключи:
ACTION = 'action'
TIME = 'time'
USER = 'user'
ACCOUNT_NAME = 'account_name'
SENDER = 'from'
DESTINATION = 'to'
DATA = 'bin'
PUBLIC_KEY = 'pubkey'

# Прочие ключи, используемые в протоколе
PRESENCE = 'presence'
REPLY = 'reply'
ERROR = 'error'
MESSAGE = 'message'
MESSAGE_TEXT = 'message_text'
EXIT = 'exit'
GET_CONTACTS = 'get_contacts'
LIST_INFO = 'data_list'
REMOVE_CONTACT = 'remove'
ADD_CONTACT = 'add'
USERS_REQUEST = 'get_users'
PUBLIC_KEY_REQUEST = 'pubkey_need'

# Словари - ответы:

REPLY_200 = {REPLY: 200}

REPLY_202 = {REPLY: 202,
             LIST_INFO: None
             }
REPLY_400 = {
    REPLY: 400,
    ERROR: None
}
# 205
REPLY_205 = {
    REPLY: 205
}

# 511
REPLY_511 = {
    REPLY: 511,
    DATA: None
}