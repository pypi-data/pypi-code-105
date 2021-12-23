from importlib import import_module
from remote_actions import get_logger, HANDLER_VIEW_NAME
from extools.view import exview

def get_handlers():
    """Get all handlers registered in this company.

    :returns: { "form_type": handler_class }
    :rtype: dict
    """
    log = get_logger('handlers')
    handlers = {}
    with exview(HANDLER_VIEW_NAME) as handler_list:
        for handler in handler_list.all():
            try:
                package, klass = handler.classpath.rsplit(".", 1)
                module = import_module(package)
                handlers[handler.type] = getattr(module, klass)
                log.debug("loaded handler type {}.".format(handler.type))
            except ImportError as e:
                log.error("failed to load handler: {}".format(e))
    return handlers

class FormHandler():
    """Abstract parent for all form handlers.

    To handle a new type of form, define a new handler and register
    it in the VIRAHNDL table.

    Form handlers are automatically dispatched based on the form.app.type
    value.
    """
    type = None

    def __init__(self, form):
        if not self.type:
            raise NotImplementedError("Handlers must have a type.")
        self.form = form

    def validate(self):
        raise NotImplementedError(
                "Validate must be implemented in a subclass.")

    def apply(self):
        raise NotImplementedError(
                "Apply must be implemented in a subclass.")

