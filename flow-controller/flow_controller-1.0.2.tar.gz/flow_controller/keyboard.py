from pynput.keyboard import Key, Listener
import threading
import time
import ctypes


def action_wrapper(target_key, cls):
    def on_action(key):
        if key == target_key:
            cls.val = not cls.val
            print(f'Val value has been switched to {cls.val}')
    return on_action

def quit_wrapper(target_key):
    def on_action(key):
        if key == target_key:
            return False
    return on_action

class key_press(threading.Thread):
    def __init__(self, action_key, quit_key):
        super().__init__()
        self.action_key = action_key
        self.quit_key = quit_key
        self.val = True
        self.active = True

    def run(self):
        with Listener(on_press=action_wrapper(self.action_key, self),
                      on_release=quit_wrapper(self.quit_key)) as listener:
            listener.join()
        self.active = False

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

