import threading
import time
import ctypes
from keyboard import is_pressed


def action_check(target_key, cls):
    while 1:
        if not cls.is_alive() or not cls.quit_thread.is_alive():
            return

        if is_pressed(target_key):
            cls.val = not cls.val
            print(f'Val value has been switched to {cls.val}')
            time.sleep(3)

def quit_check(target_key, cls):
    while cls.is_alive():
        if is_pressed(target_key):
            return False

class key_press(threading.Thread):
    def __init__(self, action_key, quit_key):
        super().__init__()
        self.action_key = action_key
        self.quit_key = quit_key
        self.val = True
        self.action_thread = threading.Thread(target=action_check, args=(self.action_key, self))
        self.quit_thread = threading.Thread(target=quit_check, args=(self.quit_key, self))

    def run(self):
        self.action_thread.start()
        self.quit_thread.start()

    def get_id(self):

        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            if thread is self:
                return id

    def stop(self):
        thread_id = self.get_id()
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
                                                         ctypes.py_object(SystemExit))
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')