import abc
from six import with_metaclass
from plico.utils.decorator import returnsNone, returns, returnsForExample
from plico_motor.types.motor_status import MotorStatus


class AbstractMotorClient(with_metaclass(abc.ABCMeta, object)):

    @abc.abstractmethod
    @returns(int)
    def position(self):
        assert False

    @abc.abstractmethod
    @returnsNone
    def move_to(self, position_in_steps):
        assert False

    @abc.abstractmethod
    @returnsNone
    def move_by(self, position_in_steps):
        assert False

    @abc.abstractmethod
    @returnsForExample({'MY_MOTOR.POS: 42'})
    def snapshot(self, prefix='MY_MOTOR'):
        assert False

    @abc.abstractmethod
    @returnsNone
    def home(self):
        assert False

    @abc.abstractmethod
    @returns(MotorStatus)
    def status(self):
        assert False

# def _proposed_interface():
#     x = plico_motor.client('ip', axis=0, port=port)
#     x.home()
#     x.home(limit=x.NEG)
#     curr_pos = x.position()
#     x.move_by(-23)
#     x.move_to(123)
#
#     # status. A given field can be MotorClient.NOT_AVAILABLE if the motor is
#     # not providing the info.
#     status = x.status()
#     assert status.has_been_homed
#     steps_per_m = status.steps_per_m
#     max_speed = status.max_speed
#     curr_pos = status.position
#     is_moving = status.is_moving
#     should_be_in = status.last_commanded_position
#
#     # snapshot is like status in a dictionary form ready for FITS headers
#     dicto = x.snapshot('MYAXIS1')
#     assert dicto['MYAXIS1.POS'] == 123
#     # and so on for each status' fields
#
#     # boh... nice to have. Need to modify config file on server side.
#     x.move_to('A')
#     x.save_current_position_as('A')
#     x.list_positions()
#
#     # boh... Is this needed in the client? Static conf should be enough.
#     x.set_max_speed(100)

