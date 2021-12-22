#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Использовать модуль осторожно!
При подгрузке модуля устанавливает в качестве обработчика сигнала SIGINT собственный обработчик,
    который ничего не делает самостоятельно, а только изменяет значение переменной graceful_exit,
    которую в свою очередь можно использовать для "щадящего" завершения программы.
SIGINT - interrupt signa (Ctrl-C) с терминала, код сигнала - 2
Linux-command: kill -2 process_pid

Usage:
    from snuff-utils.graceful_exit import graceful_exit
    if graceful_exit: break # end loop
    if graceful_exit: sys.exit(0) # exit program
"""

import signal
import logging

logger = logging.getLogger()


class GracefulExit():
    """
    Класс, экземпляр которого используется в качестве флага прерывания
    """
    exit = False

    def __bool__(self):
        return self.exit


graceful_exit = GracefulExit()


def graceful_exit_handler(signum, frame):
    """
    Обработчик сигнала, обеспечивает "щадящее" завершение программы.
    Изменяет значение глобальной переменной graceful_exit на True.
    Используя эту переменную, можно инициировать выход подобным образом:
     if graceful_exit: break # выход из цикла
     if graceful_exit: sys.exit(0) # завершение программы
    :param signum: Номер сигнала
    :param frame:
    :return: None
    """
    global graceful_exit
    graceful_exit.exit = True
    logger.info('An interrupt signal has been received. '
                'The signal will be processed according to the logic of the application.')


# Устанавливаем обработчик завершения цикла при сигнале
# Осторожно! Импорт модуля выполнит эту команду, установив тем самым обработчик для сигнала SIGINT
signal.signal(signal.SIGINT, graceful_exit_handler)
