from typing import List

from confluent_kafka import TIMESTAMP_NOT_AVAILABLE

from src.ml_pipe_core.service import Service
from src.ml_pipe_core.logger import init_logger
from src.ml_pipe_core.adapter.PetraAdapter import PetraAdapter
from src.ml_pipe_core.adapter.PetraSimulationAdapter import PetraSimulationAdapter
from optics_sim import OpticsSimulation
from src.ml_pipe_core.machine_topics import MACHINE_EVENTS, MACHINE_INPUT_TOPIC
from src.ml_pipe_core.message import Headers
from src.ml_pipe_core.config import KAFKA_SERVER_URL
from ml_pipe_core.simulation.update_message_types import SetMachineMessage, UpdateMessage
from src.ml_pipe_core.event_utls.consumer_decorator import consume

_logger = init_logger(__name__)


class MachineService(Service):
    def __init__(self, name, adapter: PetraAdapter, optic_sim: OpticsSimulation = None):
        super().__init__(name)
        self.machine_adapter = adapter
        self.optic_sim = optic_sim

    def _are_keys_in_dict(self, keys: List[str], dict):
        for key in keys:
            if key not in dict:
                return False
        return True

    @consume([MACHINE_INPUT_TOPIC], KAFKA_SERVER_URL)
    def machine_input_handler(self, msg, **kwargs):
        timestamp_type, timestamp = msg.timestamp()
        if timestamp_type == TIMESTAMP_NOT_AVAILABLE:
            _logger.debug(f"[{self.name}] receive a message without a timestamp")
            return
        headers = Headers.from_kafka_headers(msg.headers())
        received_package_id = headers.package_id
        _logger.debug(f'[{self.name}] call machine_input_handler receive headers: {str(headers)} group_id: {",".join([t.group_id for t in self.thread_pool])}')
        # if headers.is_message_for(self.type) or headers.is_message_for(self.name):

        message = SetMachineMessage.deserialize([msg])
        data = message.data
        # set
        # TODO: Send error message to user!
        if "hcor" in data:
            if not self._are_keys_in_dict(['names', 'values'], data["hcor"]):
                _logger.error(f"Machine Service received invalid message. Message: {data}")
                return
            self.machine_adapter.set_hcors(names=data["hcor"]["names"], strengths=data["hcor"]["values"])
        if "vcor" in data:
            if not self._are_keys_in_dict(['names', 'values'], data["vcor"]):
                _logger.error(f"Machine Service received invalid message. Message: {data}")
                return
            self.machine_adapter.set_vcors(names=data["vcor"]["names"], strengths=data["vcor"]["values"])
        if "machineparams" in data:
            if not self._are_keys_in_dict(['names', 'values'], data["machineparams"]):
                _logger.error(f"Machine Service received invalid message. Message: {data}")
                return
            self.machine_adapter.set_machine_params(names=data["machineparams"]["names"], values=data["machineparams"]["values"])
        if "twiss" in data:
            if not self._are_keys_in_dict(['names', 'mat'], data["twiss"]):
                _logger.error(f"Machine Service received invalid message. Message: {data}")
                return
            self.machine_adapter.set_twiss(names=data["twiss"]["names"], mat=data["twiss"]["mat"])
        # simulate
        if self.optic_sim is not None:
            self.optic_sim.simulate()

        # updated event
        self.updated_event(package_id=received_package_id,
                           msg=UpdateMessage(source=headers.msg_type, updated=list(data.keys())))
        _logger.debug(f"[{self.name}] end machine_input_handler")

    def updated_event(self, package_id, msg):
        self.producer.sync_produce(MACHINE_EVENTS, msg.serialize(), Headers(package_id=package_id, source=self.type))
