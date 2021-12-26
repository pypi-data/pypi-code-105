import sys
import binascii
import hashlib
import hmac
import socket
import threading
import time

from PyQt5.QtCore import pyqtSignal, QObject

from client.common.utils import *
from client.common.variables import *
from client.common.errors import ServerError

sys.path.append('../../')

# Логер и объект блокировки для работы с сокетом.
client_logger = logging.getLogger('client')
socket_lock = threading.Lock()


# Класс - Транспорт, отвечает за взаимодействие с сервером
class ClientTransport(threading.Thread, QObject):
    # Сигналы новое сообщение и потеря соединения
    new_message = pyqtSignal(dict)
    message_205 = pyqtSignal()
    connection_lost = pyqtSignal()

    def __init__(self, port, ip_address, database, username, passwd, keys):
        # Вызываем конструктор предков
        threading.Thread.__init__(self)
        QObject.__init__(self)

        # Класс База данных - работа с базой
        self.database = database
        # Имя пользователя
        self.username = username
        # Сокет для работы с сервером
        self.transport = None
        self.keys = keys
        self.password = passwd
        # Устанавливаем соединение:
        self.connection_init(port, ip_address)
        # Обновляем таблицы известных пользователей и контактов
        try:
            self.user_list_update()
            self.contacts_list_update()
        except OSError as err:
            if err.errno:
                client_logger.critical(f'Потеряно соединение с сервером.')
                raise ServerError('Потеряно соединение с сервером!')
            client_logger.error('вышло время во время соединения при '
                                'обновлении списков пользователей.')
        except json.JSONDecodeError:
            client_logger.critical(f'Потеряно соединение с сервером.')
            raise ServerError('Потеряно соединение с сервером!')
            # Флаг продолжения работы транспорта.
        self.running = True

    def connection_init(self, port, ip):
        '''Метод отвечающий за установку соединения с сервером'''
        # Инициализация сокета и сообщение серверу о нашем появлении
        self.transport = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Таймаут необходим для освобождения сокета.
        self.transport.settimeout(5)

        # Соединяемся, 5 попыток соединения, флаг успеха ставим в True,
        # если удалось
        connected = False
        for i in range(5):
            client_logger.info(f'Попытка подключения №{i + 1}')
            try:
                self.transport.connect((ip, port))
            except (OSError, ConnectionRefusedError):
                pass
            else:
                connected = True
                client_logger.debug("Соединение установлено.")
                break
            time.sleep(1)

        # Если соединится не удалось - исключение
        if not connected:
            client_logger.critical('Не удалось установить соединение'
                                   ' с сервером')
            raise ServerError('Не удалось установить соединение '
                              'с сервером')

        client_logger.debug('Starting auth dialog.')

        # Запускаем процедуру авторизации
        # Получаем хэш пароля
        passwd_bytes = self.password.encode('utf-8')
        salt = self.username.lower().encode('utf-8')
        passwd_hash = hashlib.pbkdf2_hmac('sha512', passwd_bytes,
                                          salt, 10000)
        passwd_hash_string = binascii.hexlify(passwd_hash)

        client_logger.debug(f'Password hash ready:'
                            f' {passwd_hash_string}')

        # Получаем публичный ключ и декодируем его из байтов
        pubkey = self.keys.publickey().export_key().decode('ascii')

        # Авторизируемся на сервере
        with socket_lock:
            presense = {
                ACTION: PRESENCE,
                TIME: time.time(),
                USER: {
                    ACCOUNT_NAME: self.username,
                    PUBLIC_KEY: pubkey
                }
            }
            client_logger.debug(f"Сообщение о присутствии = {presense}")
            # Отправляем серверу приветственное сообщение.
            try:
                send_message(self.transport, presense)
                ans = get_message(self.transport)
                client_logger.debug(f'Server response = {ans}.')
                # Если сервер вернул ошибку, бросаем исключение.
                if REPLY in ans:
                    if ans[REPLY] == 400:
                        raise ServerError(ans[ERROR])
                    elif ans[REPLY] == 511:
                        # Если всё нормально, то продолжаем процедуру
                        # авторизации.
                        ans_data = ans[DATA]
                        hash = hmac.new(passwd_hash_string,
                                        ans_data.encode('utf-8'), 'MD5')
                        digest = hash.digest()
                        my_ans = REPLY_511
                        my_ans[DATA] = binascii.b2a_base64(
                            digest).decode('ascii')
                        send_message(self.transport, my_ans)
                        self.process_server_ans(get_message(self.transport))
            except (OSError, json.JSONDecodeError) as err:
                client_logger.debug(f'Connection error.', exc_info=err)
                raise ServerError('Сбой соединения в процессе авторизации.')

    # Функция обрабатывающяя сообщения от сервера. Ничего не возращает.
    # Генерирует исключение при ошибке.
    def process_server_ans(self, message):
        client_logger.debug(f'Разбор сообщения от сервера: {message}')

        # Если это подтверждение чего-либо
        if REPLY in message:
            if message[REPLY] == 200:
                return
            elif message[REPLY] == 400:
                raise ServerError(f'{message[ERROR]}')
            elif message[REPLY] == 205:
                self.user_list_update()
                self.contacts_list_update()
                self.message_205.emit()
            else:
                client_logger.error(f'Принят неизвестный код подтверждения'
                                    f' {message[REPLY]}')

        # Если это сообщение от пользователя добавляем в базу,
        # даём сигнал о новом сообщении
        elif ACTION in message and message[ACTION] == MESSAGE and \
                SENDER in message and DESTINATION in message \
                and MESSAGE_TEXT in message and \
                message[DESTINATION] == self.username:
            client_logger.debug(f'Получено сообщение от пользователя '
                                f'{message[SENDER]}:{message[MESSAGE_TEXT]}')

            self.new_message.emit(message)

    def contacts_list_update(self):
        '''Метод обновляющий с сервера список контактов.'''
        self.database.contacts_clear()
        client_logger.debug(f'Запрос контакт листа для пользователся '
                            f'{self.name}')
        req = {
            ACTION: GET_CONTACTS,
            TIME: time.time(),
            USER: self.username
        }
        client_logger.debug(f'Сформирован запрос {req}')
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        client_logger.debug(f'Получен ответ {ans}')
        if REPLY in ans and ans[REPLY] == 202:
            for contact in ans[LIST_INFO]:
                self.database.add_contact(contact)
        else:
            client_logger.error('Не удалось обновить список контактов.')

    def user_list_update(self):
        '''Метод обновления таблицы известных пользователей.'''
        client_logger.debug(f'Запрос списка известных пользователей '
                            f'{self.username}')
        req = {
            ACTION: USERS_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if REPLY in ans and ans[REPLY] == 202:
            self.database.add_users(ans[LIST_INFO])
        else:
            client_logger.error('Не удалось обновить список '
                                'известных пользователей.')

    def key_request(self, user):
        '''Метод, запрашивающий с сервера публичный ключ пользователя.'''
        client_logger.debug(f'Запрос публичного ключа для {user}')
        req = {
            ACTION: PUBLIC_KEY_REQUEST,
            TIME: time.time(),
            ACCOUNT_NAME: user
        }
        with socket_lock:
            send_message(self.transport, req)
            ans = get_message(self.transport)
        if REPLY in ans and ans[REPLY] == 511:
            return ans[DATA]
        else:
            client_logger.error(f'Не удалось получить ключ собеседника{user}.')

    def add_contact(self, contact):
        client_logger.debug(f'Создание контакта {contact}')
        req = {
            ACTION: ADD_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.process_server_ans(get_message(self.transport))

    def remove_contact(self, contact):
        '''Метод удаления клиента на сервере.'''
        client_logger.debug(f'Удаление контакта {contact}')
        req = {
            ACTION: REMOVE_CONTACT,
            TIME: time.time(),
            USER: self.username,
            ACCOUNT_NAME: contact
        }
        with socket_lock:
            send_message(self.transport, req)
            self.process_server_ans(get_message(self.transport))

    def transport_shutdown(self):
        '''Метод закрытия соединения, отправляет сообщение о выходе.'''
        self.running = False
        message = {
            ACTION: EXIT,
            TIME: time.time(),
            ACCOUNT_NAME: self.username
        }
        with socket_lock:
            try:
                send_message(self.transport, message)
            except OSError:
                pass
        client_logger.debug('Транспорт завершает работу.')
        time.sleep(0.5)

    def send_message(self, to, message):
        '''Метод отправки сообщения на сервер.'''
        message_dict = {
            ACTION: MESSAGE,
            SENDER: self.username,
            DESTINATION: to,
            TIME: time.time(),
            MESSAGE_TEXT: message
        }
        client_logger.debug(f'Сформирован словарь сообщения: {message_dict}')

        # Необходимо дождаться освобождения сокета для отправки сообщения
        with socket_lock:
            send_message(self.transport, message_dict)
            self.process_server_ans(get_message(self.transport))
            client_logger.info(f'Отправлено сообщение для пользователя {to}')

    def run(self):
        '''Метод, содержащий основной цикл работы транспортного потока.'''
        client_logger.debug('Запущен процесс - приёмник сообщений с сервера.')
        while self.running:
            # Отдыхаем секунду и снова пробуем захватить сокет.
            # если не сделать здесь задержку, то отправка может достаточно
            # долго ждать освобождения сокета.
            time.sleep(1)
            message = None
            with socket_lock:
                try:
                    self.transport.settimeout(0.5)
                    message = get_message(self.transport)
                except OSError as err:
                    if err.errno:
                        client_logger.critical(f'Потеряно соединение '
                                               f'с сервером.')
                        self.running = False
                        self.connection_lost.emit()
                # Проблемы с соединением
                except (ConnectionError, ConnectionAbortedError,
                        ConnectionResetError,
                        json.JSONDecodeError, TypeError):
                    client_logger.debug(f'Потеряно соединение с сервером.')
                    self.running = False
                    self.connection_lost.emit()
                finally:
                    self.transport.settimeout(5)

                # Если сообщение получено, то вызываем функцию обработчик:
                if message:
                    client_logger.debug(f'Принято сообщение с сервера:'
                                        f' {message}')
                    self.process_server_ans(message)
