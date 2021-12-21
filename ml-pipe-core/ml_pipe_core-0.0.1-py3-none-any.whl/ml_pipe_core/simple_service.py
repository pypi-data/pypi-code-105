import json
from abc import abstractmethod

from confluent_kafka import TIMESTAMP_NOT_AVAILABLE

from .logger import init_logger
from .config import KAFKA_SERVER_URL
from .machine_topics import MACHINE_INPUT_TOPIC
from .service import Service
from .event_utls.consumer_decorator import consume
from .message import Headers, Message
from .simple_service_message import SimpleServiceMessage
from .topics import RECONFIG_TOPIC, SERVICE_INPUT_TOPIC
from .adapter.PetraAdapter import PetraAdapter
from .simulation.update_message_types import *
# from src.service_iface.topics import IS_ALIVE
# from src.utils.TimerThread import TimerThread
_logger = init_logger(__name__)


class SimpleService(Service):
    def __init__(self, name, machine_adapter: PetraAdapter):
        super().__init__(name)
        self.machine_adapter = machine_adapter
        self.current_package_id = None

    @abstractmethod
    def proposal(self, params) -> Message:
        pass

    def machine_events(self, msg_type, msg):
        _logger.warning("observe is not implemented by servie")

    def set_machine(self, data: SetMachineMessage):
        if self.current_package_id is not None:
            self.producer.sync_produce(MACHINE_INPUT_TOPIC, data.serialize(), Headers(package_id=self.current_package_id, source=self.type, msg_type=self.type))
        else:
            _logger.error("Try to set machine with a message without package_id.")

    def reconfig_event(self, msg):
        """[summary]
        Function that can be overloaded by the concret service to reconfig without restarting
        :param msg: [description]
        :type msg: [type]
        """
        pass

    @consume([SERVICE_INPUT_TOPIC, RECONFIG_TOPIC], KAFKA_SERVER_URL)
    def service_input_handler(self, msg, **kwargs):
        timestamp_type, timestamp = msg.timestamp()
        if timestamp_type == TIMESTAMP_NOT_AVAILABLE:
            _logger.debug(f"[{self.name}] receive a message without a timestamp")
            return
        headers = Headers.from_kafka_headers(msg.headers())
        self.current_package_id = headers.package_id
        #self.machine_adapter.active_package_id = headers.package_id
        _logger.debug(f'[{self.name}] call service_input_handler receive headers: {str(headers)} group_id: {",".join([t.group_id for t in self.thread_pool])}')
        _logger.debug(f"Received message from topic '{msg.topic()}'")
        if headers.is_message_for(self.type) or headers.is_message_for(self.name):

            if msg.topic() == SERVICE_INPUT_TOPIC:
                data = SimpleServiceMessage.deserialize([msg])
                self.proposal(data.params)
            elif msg.topic() == RECONFIG_TOPIC:
                _logger.debug(f"reconfig message received")
                self.reconfig_event(json.loads(msg.value().decode('utf-8')))

        _logger.debug(f'[{self.name}] end service_input_handler')
