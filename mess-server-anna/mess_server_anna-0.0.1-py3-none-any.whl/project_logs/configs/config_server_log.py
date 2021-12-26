import logging.handlers
import os
import sys
from logging import INFO, DEBUG

sys.path.append('../')

# создаём формировщик логов (formatter):
server_formatter = logging.Formatter('%(asctime)s %(levelname)s %(filename)s %(message)s')

# Подготовка имени файла для логирования
path = os.getcwd()
path = os.path.join(path, '../logs/server.log')

# создаём потоки вывода логов
stream_handler = logging.StreamHandler(sys.stderr)
stream_handler.setFormatter(server_formatter)
stream_handler.setLevel(logging.ERROR)
log_file = logging.handlers.TimedRotatingFileHandler(path, encoding='utf8', interval=1, when='midnight')
log_file.setFormatter(server_formatter)

# создаём регистратор и настраиваем его
logger = logging.getLogger('server')
logger.addHandler(stream_handler)
logger.addHandler(log_file)
logger.setLevel(DEBUG)

# отладка
if __name__ == '__main__':
    logger.critical('Критическая ошибка')
    logger.error('Ошибка')
    logger.debug('Отладочная информация')
    logger.info('Информационное сообщение')