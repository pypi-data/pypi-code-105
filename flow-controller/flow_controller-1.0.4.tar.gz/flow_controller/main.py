import threading
from flow_controller.keyboard import key_press
from keyboard import is_pressed
import time
from datetime import datetime


class ControlFlow:
    def __init__(self):
        pass

    def __bool__(self):
        pass

    def is_active(self):
        pass




class Pause(ControlFlow):
    def __init__(self, trigger):
        super().__init__()
        self.trigger = trigger
        self.trigger.start()

    def __bool__(self):
        self.handle()
        return self.trigger.val

    @classmethod
    def from_keys(cls, action_key, quit_key):
        trigger = key_press(action_key, quit_key)
        return cls(trigger)

    def is_active(self):
        return self.trigger.quit_thread.is_alive()

    def handle(self):
        if not self.trigger.quit_thread.is_alive():
            self.trigger.stop()
            self.trigger.join()


class Timer(ControlFlow):
    def __init__(self, start_time, end_time, enddate=None):
        super().__init__()
        self.start_time = start_time
        self.end_time = end_time
        self.enddate = enddate

    def __bool__(self):
        now = self.get_time()
        if self.start_time < self.end_time:
            return self.start_time < now < self.end_time
        return (self.start_time < now) or (now < self.end_time)

    def get_time(self):
        now = datetime.now()
        return now.hour + now.minute / 60 + now.second / 3600

    def is_active(self):
        return True if self.enddate is None else datetime.now() < self.enddate


class Composite(ControlFlow):
    def __init__(self, composite):
        super().__init__()
        self.composite = composite

    def __bool__(self):
        return any(i if not hasattr(i, '__iter__') else all(i) for i in self.composite)

    def is_active(self):
        return any(i.is_active() if not hasattr(i, '__iter__') else all([j.is_active() for j in i]) for i in self.composite)


if __name__ == '__main__':
    """
    Small showcase, cuz no way I am writing documentation.
    """


    p = Pause(key_press('q', 'z'))

    start = time.time()
    while p.is_active():
        if time.time() - start > 1:
            start = time.time()
