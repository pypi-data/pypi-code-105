#!/usr/bin/python
# -*- coding: UTF-8 -*-
import time
import pika
import traceback
from . import py_logging
import logging
from pika.exceptions import ConnectionClosed, ChannelClosed


class MQConnection(object):
    def __init__(self, kwargs):
        self.kwargs = kwargs
        self.connection = None
        self.channel = None

    def reconnect(self):
        if self.connection and not self.connection.is_closed:
            self.connection.close()
        credentials = pika.PlainCredentials(self.kwargs.get('username', 'guest'), self.kwargs.get('passwd', 'guest'))
        parameters = pika.ConnectionParameters(host=self.kwargs.get('hostname', 'localhost'),
                                               port=int(self.kwargs.get('port', 5672)),
                                               virtual_host=self.kwargs.get('virtual_host', '/'),
                                               credentials=credentials,
                                               connection_attempts=int(self.kwargs.get('connection_attempts', 3)),
                                               retry_delay=int(self.kwargs.get('retry_delay', 10)),
                                               blocked_connection_timeout=int(self.kwargs.get('blocked_connection_timeout', 5)),
                                               heartbeat=int(self.kwargs.get('heartbeat', 300))
                                               )
        self.connection = pika.BlockingConnection(parameters)
        self.channel = self.connection.channel()

        if isinstance(self, MQConsume):
            # self.channel.basic_qos(prefetch_count=10)
            # self.channel.basic_consume(queue=self.tbname, on_message_callback=self.consumer_callback, auto_ack=False)
            self.channel.basic_consume(queue=self.queue, on_message_callback=self.consumer_callback, auto_ack=True)
            self.channel.start_consuming()


class MQPublish(MQConnection):
    def __init__(self, kwargs):
        super(MQPublish, self).__init__(kwargs)
        self.reconnect()

    def _to_queue(self, ex, key, data, serializer=None, count=3):
        for i in range(count):
            try:
                if serializer:
                    data = serializer(data)
                self.channel.basic_publish(exchange=ex, routing_key=key, body=data,
                                           properties=pika.BasicProperties(delivery_mode=2))
                return True
            except Exception as e:
                logging.getLogger('main_logger').error('{} {}'.
                                                       format(str(e), traceback.format_exc().replace('\n', '').replace('\r', '')))
                self.reconnect()
                time.sleep(3)
        return False


class MQConsume(MQConnection):
    def __init__(self, kwargs):
        super(MQConsume, self).__init__(kwargs)

    def consumer_callback(self, ch, method, header, body):
        # delivery_tag = method.delivery_tag

        # 开启子线程，确保消息被ack
        # t = threading.Thread(target=self.do_ack, args=(self.connection, ch, delivery_tag))
        # t.start()

        self._do(data=body)
    # def do_ack(self, conn, ch, delivery_tag):
    #     cb = functools.partial(self.ack_message, ch, delivery_tag)
    #     conn.add_callback_threadsafe(cb)

    # def ack_message(self, ch, deliver_tag):
    #     if ch.is_open:
    #         ch.basic_ack(deliver_tag)
    #     else:
    #         channel已经关闭，重连确认
    #         self.reconnect()
    #         self.channel.basic_ack(deliver_tag)

    def _do(self, data):
        # 真正消费的函数
        pass

    def start_consume(self, queue, count=3):
        self.queue = queue
        for i in range(count):
            try:
                self.reconnect()
            except pika.exceptions.StreamLostError:
                logging.getLogger('main_logger').warning('no message, mq positive closed {}'.
                                                         format(traceback.format_exc().replace('\n', '').replace('\r', '')))
                time.sleep(3)
            except ConnectionClosed as e:
                logging.getLogger('main_logger').error('connection closed {}'.
                                                       format(traceback.format_exc().replace('\n', '').replace('\r', '')))
                time.sleep(3)
            except ChannelClosed as e:
                logging.getLogger('main_logger').error('channel closed {}'.
                                                       format(traceback.format_exc().replace('\n', '').replace('\r', '')))
                time.sleep(3)
            except Exception as e:
                logging.getLogger('main_logger').error('{} {}'.
                                                       format(str(e), traceback.format_exc().replace('\n', '').replace('\r', '')))
                time.sleep(3)

    def _from_queue(self, qname, count=3):
        # 消费入口函数
        self.start_consume(qname, count)