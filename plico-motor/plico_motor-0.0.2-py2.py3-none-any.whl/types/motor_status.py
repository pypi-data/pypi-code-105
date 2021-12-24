from plico_motor.client.snapshot_entry import SnapshotEntry


class MotorStatus(object):

    TYPE_LINEAR = 'linear'
    TYPE_ROTATIVE = 'rotative'

    def __init__(self,
                 name,
                 position,
                 steps_per_SI_unit,
                 was_homed,
                 motor_type,
                 is_moving,
                 last_commanded_position
                 ):
        self.name = name
        self.position = position
        self.steps_per_SI_unit = steps_per_SI_unit
        self.was_homed = was_homed
        self.motor_type = motor_type
        self.is_moving = is_moving
        self.last_commanded_position = last_commanded_position

    def as_dict(self):
        dicto = {}
        dicto[SnapshotEntry.MOTOR_NAME] = self.name
        dicto[SnapshotEntry.POSITION] = self.position
        dicto[SnapshotEntry.STEPS_PER_SI_UNITS] = self.steps_per_SI_unit
        dicto[SnapshotEntry.WAS_HOMED] = self.was_homed
        dicto[SnapshotEntry.MOTOR_TYPE] = self.motor_type
        dicto[SnapshotEntry.IS_MOVING] = self.is_moving
        dicto[SnapshotEntry.LAST_COMMANDED_POSITION] = self.last_commanded_position
        return dicto

