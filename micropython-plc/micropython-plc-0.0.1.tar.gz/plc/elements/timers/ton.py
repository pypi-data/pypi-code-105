from utime import ticks_ms
import _thread

from plc import PLCBase
from plc.elements.timers import PLCTimer

class PLCTimerOn(PLCTimer):
    def __init__(self, input, delay, name=None):
        super().__init__(name)

        input.add_event_on_change(self.__on_input_change)
        self._input = input

        self._enabled = PLCBase("{}:EN".format(self.name))
        self._active = PLCBase("{}:TT".format(self.name))

        self._start_time = None
        self._amount = 0
        self.delay = delay


    def __on_input_change(self, input, value, dir):
        if value:
            self._start()
        else:
            self._stop()


    def _start(self):
        if self._active._value:
            return

        self._enabled._value = True


    def _stop(self):
        self._enabled._value = False
        self._active._value = False
        self._value = False
        self._amount = 0


    def loop(self):
        if not self._enabled._value:
            return

        if self._value:
            return

        if not self._active._value:
            self._start_time = ticks_ms()
            self._active._value = True
            print("Loop enabled at {} AM:{} DL:{}".format(self._start_time, self._amount, self.delay))

        self._amount = ticks_ms() - self._start_time

        if self._amount >= self.delay:
            self._value = True
            self._active._value = False
            print("Loop thread stopped after {}ms".format(ticks_ms() - self._start_time))
                

    @property
    def accum(self):
        return self._amount


    @property
    def activated(self):
        return self._active


    @property
    def delay(self):
        return self._delay


    @delay.setter
    def delay(self, delay):
        if not delay:
            raise ValueError()
        
        self._delay = delay

    @property
    def enabled(self):
        return self._enabled
