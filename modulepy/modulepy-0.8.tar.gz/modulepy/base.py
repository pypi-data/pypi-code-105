from multiprocessing import Queue, Event, Process
from threading import Thread
from multiprocessing.synchronize import Event as EventType
from dataclasses import dataclass
from time import sleep


@dataclass
class ModuleVersion:
    major: int
    minor: int
    patch: int

    def __str__(self):
        return f"{self.major}.{self.minor}.{self.patch}"


@dataclass
class ModuleInformation:
    name: str
    version: ModuleVersion

    def __str__(self):
        return f"{self.name} {self.version}"


@dataclass
class SharedData:
    origin: ModuleInformation
    data: dict


class ModuleBase(object):
    do_run: EventType = Event()
    information = ModuleInformation("ModuleBase", ModuleVersion(1, 0, 0))
    dependencies: list[ModuleInformation] = []

    input_queue: Queue = Queue()
    output_queue: Queue = Queue()

    error: str = None

    def __init__(self):
        self.name = str(self.information)
        self.do_run.set()

    def __call__(self, *args, **kwargs):
        return eval(f"{self.__class__.__name__}()")

    def on_start(self):
        pass

    def on_stop(self):
        pass

    def on_exception(self, exception: Exception):
        self.error = str(exception)
        print(f"Caught exception: {exception}")
        self.stop()

    def work(self):
        sleep(0.1)

    def process_input_data(self, data: SharedData):
        pass

    def process_input_queue(self):
        if self.input_queue is None:
            return
        while not self.input_queue.empty():
            data = self.input_queue.get()
            self.process_input_data(data)

    def loop(self):
        while self.do_run.is_set():
            self.process_input_queue()
            try:
                self.work()
            except Exception as e:
                self.on_exception(e)

    def _run(self):
        self.on_start()
        self.loop()
        self.on_stop()

    def run(self):
        self._run()

    def stop(self):
        print(f"{self.name} is stopping")
        self.do_run.clear()

    def enqueue(self, data: dict):
        if self.output_queue is not None:
            self.output_queue.put(SharedData(self.information, data))


class ProcessModule(ModuleBase, Process):
    daemon = True

    def __init__(self):
        Process.__init__(self)
        ModuleBase.__init__(self)

    def run(self) -> None:
        self._run()


class ThreadModule(ModuleBase, Thread):
    daemon = True

    def __init__(self):
        Thread.__init__(self)
        ModuleBase.__init__(self)

    def run(self):
        self._run()
