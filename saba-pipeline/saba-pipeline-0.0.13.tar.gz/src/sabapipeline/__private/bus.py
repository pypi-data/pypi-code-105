from .utilities import *
from .concepts import EventHandler, Event
from .elements import EventListener, InternalPipelineElement


class EventBus(EventHandler):
    def __init__(self):
        self.listeners: Dict[Type, List[EventListener]] = dict()

    def add_listener(self, listener: EventListener, type_to_listen: Type) -> None:
        if type_to_listen not in self.listeners:
            self.listeners[type_to_listen] = [listener]
        else:
            self.listeners[type_to_listen].append(listener)

    def handle_event(self, event_to_handle: Event):
        event_type: Type = type(event_to_handle)
        for listed_type in self.listeners:
            if issubclass(event_type, listed_type):
                for event_listener in self.listeners[listed_type]:
                    event_listener.logger.log(event_listener.input_flow_log_level,
                                              f'<<< {event_to_handle.__class__.__name__} ({event_to_handle.__str__()})')
                    event_listener.process_event(event_to_handle)


class InputLoggerEventBus(EventHandler):
    def __init__(self, raiser: InternalPipelineElement, bus: EventBus):
        self.raiser = raiser
        self.bus = bus

    def handle_event(self, event_to_handle: Event):
        self.raiser.logger.log(self.raiser.output_flow_log_level,
                               f'>>> {event_to_handle.__class__.__name__} ({event_to_handle.__str__()})')
        self.bus.handle_event(event_to_handle)
