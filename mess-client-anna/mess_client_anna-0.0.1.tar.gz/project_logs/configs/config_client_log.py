import sys
import os
import logging
from logging import INFO

sys.path.append('../')

# создаём формировщик логов (formatter):
client_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.getcwd()
path = os.path.join(path, '../logs/client.log')

# создаём потоки вывода логов
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(client_formatter)
stream_handler.setLevel(logging.ERROR)
log_file = logging.FileHandler(path, encoding='utf8')
log_file.setFormatter(client_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('client')
logger.addHandler(stream_handler)
logger.addHandler(log_file)
logger.setLevel(logging.DEBUG)

# отладка
if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')
