import logging
import time
from typing import Callable, NamedTuple, Union, Any

import paho.mqtt.client as mqtt

'''
    pip install paho-mqtt
'''

class MQTTConfig(NamedTuple):
    HOST: str
    PORT: int = 1883    #使用SSL/TLS的默认端口是 8883
    USER: str = None
    PSW: str = None
    TOPIC: str = ''
    CLIENT_ID: str = ''
    KEEP_ALIVE: int = 60
    SHORT_CONNECT: bool = False #短连接模式

class MQTTAccessor:

    def __init__(self, config: MQTTConfig):
        self.config = config
        self.client = None
        self.callbacks = {}

    def __del__(self):
        self.close()

    def connack_string(self, connack_code: int):
        """Return the string associated with a CONNACK result."""
        if connack_code == 0:
            return "Connection Accepted."
        elif connack_code == 1:
            return "Connection Refused: unacceptable protocol version."
        elif connack_code == 2:
            return "Connection Refused: identifier rejected."
        elif connack_code == 3:
            return "Connection Refused: broker unavailable."
        elif connack_code == 4:
            return "Connection Refused: bad user name or password."
        elif connack_code == 5:
            return "Connection Refused: not authorised."
        else:
            return "Connection Refused: unknown reason."

    def on_connect(self, client, userdata, flags, rc):
        if int(str(rc)) == 0:
            self.set_call_result('debug_log', content=f"connect success")
        else:   #连接失败
            self.set_call_result('debug_log', content=f"connect fail({self.connack_string(rc)})")

    def on_message(self, client, userdata, message):
        self.set_call_result('receive_data', topic=message.topic, payload=message.payload)
        self.set_call_result('debug_log', content=f"recv message({message.topic} {message.payload})")

    def on_log(self, mqttc, userdata, level, string):
        pass

    def on_subscribe(self, client, userdata, mid, granted_qos):
        self.set_call_result('debug_log', content=f"subscribe({mid}) success")

    def on_disconnect(self, client, userdata, rc):
        self.set_call_result('debug_log', content=f"disconect({self.connack_string(rc)})")

    def on_publish(self, client, userdata, mid):
        self.set_call_result('debug_log', content=f"publish({mid}) success")

    def close(self):
        try:
            if self.client:
                self.client.loop_stop()
                self.client.disconnect()
        finally:
            self.client = None

    def get_client(self, client_mode='sub'):
        if self.client is None:
            if self.config.CLIENT_ID is None or len(self.config.CLIENT_ID) == 0:
                client = mqtt.Client(client_id='', clean_session = True)
            else:
                client = mqtt.Client(self.config.CLIENT_ID)
            if self.config.USER is not None and self.config.PSW is not None and len(self.config.USER) > 0:
                client.username_pw_set(self.config.USER, self.config.PSW)
            client.on_connect = self.on_connect
            client.on_message = self.on_message
            client.on_subscribe = self.on_subscribe
            client.on_disconnect = self.on_disconnect
            client.on_publish = self.on_publish
            client.on_log = self.on_log
            client.connect(self.config.HOST, self.config.PORT, self.config.KEEP_ALIVE)
            if client_mode == 'pub':
                client.loop_start()
            while not client.is_connected():    #等待连接
                time.sleep(0.1)
            self.client = client
        return self.client

    def publish_topic(self, topic: str, message: str, qos: int = 0) -> bool:
        client = self.get_client('pub')
        if client is not None:
            try:
                info = client.publish(topic, payload=message, qos=qos)
                info.wait_for_publish()
                if info.rc == mqtt.MQTT_ERR_SUCCESS:
                    return True
                raise Exception(f"publish fail({info})")
            finally:
                if self.config.SHORT_CONNECT is True or self.is_connected() is False:
                    self.close()

    def subscribe_topics(self, topics: Union[str, list], qos: int = 0, retry_interval: int=10, callback: Callable = None):
        self.callbacks['receive_data'] = callback
        while True:
            try:
                client = self.get_client()
                if client:
                    client.subscribe(topics, qos=qos)
                    client.loop_forever()
            except Exception:
                logging.error(f'topics={topics} exception', exc_info=True)
            finally:
                self.close()
            time.sleep(retry_interval)

    def is_connected(self) -> bool:
        if self.client and self.client.is_connected():
            return True
        return False

    def enable_logging(self, enable_log: bool, callback: Callable = None):
        if enable_log is True:
            self.callbacks['debug_log'] = callback
        else:
            self.callbacks['debug_log'] = None

    def set_call_result(self, call_method: str, **kwargs):
        if isinstance(self.callbacks, dict):
            call_method = self.callbacks.get(call_method)
            if isinstance(call_method, Callable):
                call_method(**kwargs)