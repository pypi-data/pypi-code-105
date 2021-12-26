import json

from server.common.decorators import log
from server.common.errors import IncorrectDataRecivedError
from server.common.variables import MAX_MESSAGE_LENGTH, ENCODING


@log
def get_message(client):
    """
    Утилита приёма и декодирования сообщения принимает байты выдаёт словарь,
    если приняточто-то другое отдаёт ошибку значения
    """
    encoded_reply = client.recv(MAX_MESSAGE_LENGTH)  # берем из сокета байты
    if isinstance(encoded_reply, bytes):
        json_reply = encoded_reply.decode(ENCODING)  # делаем декодирование
        reply = json.loads(json_reply)  # получаем словарь
        if isinstance(reply, dict):  # проверка явл ли словарем
            return reply
        else:
            raise IncorrectDataRecivedError

    else:
        raise IncorrectDataRecivedError


@log
def send_message(sock, message):
    """
    Утилита кодирования и отправки сообщения
    принимает словарь и отправляет его
    """
    if not isinstance(message, dict):
        raise NonDictInputError
    json_message = json.dumps(message)  # из словаря message делаем json-строку
    encoded_message = json_message.encode(ENCODING)  # делаем байты
    sock.send(encoded_message)  # байты кладем в сокет
