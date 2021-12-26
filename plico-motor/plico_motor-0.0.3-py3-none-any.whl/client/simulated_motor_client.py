from plico_motor.client.abstract_motor_client import AbstractMotorClient
from plico.utils.decorator import override, returns
from plico_motor.types.motor_status import MotorStatus
from plico.utils.snapshotable import Snapshotable


class SimulatedMotorClient(AbstractMotorClient):

    def __init__(self):
        self._name = 'mySimulatedMotor'
        self._position = 0
        self._was_homed = False
        self._step_per_si_units = 123456
        self._type = MotorStatus.TYPE_LINEAR
        self._is_moving = False
        self._last_cmd = 0

    @override
    def position(self):
        return self._position

    @override
    def move_to(self, position_in_steps):
        self._position = position_in_steps
        self._last_cmd = self._position

    @override
    def move_by(self, position_in_steps):
        self._position += position_in_steps
        self._last_cmd = self._position

    @override
    def home(self):
        self._position = 0
        self._was_homed = True
        self._last_cmd = 0

    @override
    def snapshot(self, prefix):
        status = self.status()
        return Snapshotable.prepend(prefix, status.as_dict())

    @override
    @returns(MotorStatus)
    def status(self):
        status = MotorStatus(
            self._name,
            self._position,
            self._was_been_homed,
            self._step_per_si_units,
            self._was_homed,
            self._type,
            self._is_moving,
            self._last_cmd
            )
        return status

