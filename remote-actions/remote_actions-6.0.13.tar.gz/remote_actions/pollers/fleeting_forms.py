try:
    from accpac import *
except ImportError:
    pass

from remote_actions import get_logger, _error
from remote_actions.services.fleeting_forms import FormClient
from remote_actions.pollers.errors import (
        PollerStartupError,
        PollerAPIError,
        PollerWorkflowInstanceDeletedError,
        PollerFormInError,
        PollerDeleteError, )
from remote_actions.handlers import get_handlers
from remote_actions.handlers.workflow_approval import (
        WorkflowApprovalFormHandler, )

class FleetingFormPoller():
    """The fleeting form poller retrieves completed forms and applies them.

    :param org_: the sage company to poll for.
    :type org_: str
    :param clean: delete forms after applying their actions?
    :type clean: bool
    """


    def __init__(self, org_, clean=True):
        self.log = get_logger("FleetingFormPoller")
        self.errors = []
        self.successes = []
        self.org = org_
        self.clean = clean
        self.__form_list = []

        self.handlers = get_handlers()

        try:
            self.client = FormClient()
        except Exception as e:
            raise PollerStartupError("Failed to start client: {}".format(e))

        self.log.info("form poller started for org {} with clean {}".format(
                org_, clean))

    @property
    def configured(self):
        return bool(self.client.token)


    def _flush_error_stack_to_log(self, form):
        """Flush the error stack to the log to debug errors in Sage."""
        errors = ErrorStack()
        self.log.debug("[{}] - flushing {} messages from error stack.".format(
                form['code'], errors.count()))
        for i in range(0, errors.count()):
            func = self.log.debug
            priority = errors.getPriority(i)
            if priority == PRI_MESSAGE:
                func = self.log.info
            elif priority == PRI_WARNING:
                func = self.log.warn
            elif priority == PRI_MESSAGE:
                func = self.log.error
            func("[{}] - {}.".format(form['code'], errors.getText(i)))
        errors.clear()

    @property
    def form_list(self):
        """A list of all forms in this namespace from cache or API."""
        if not self.__form_list:
            try:
                self.__form_list = self.client.list()
            except Exception as e:
                raise PollerAPIError("Failed to list actions: {}".format(e))
        return self.__form_list

    def form_list_filtered_by(self, form_filter={}, app_filter={}):
        """Yields forms from form_list matching form and app attrs.

        :param form_filter: the form attributes to filter for.
        :type form_filter: dict
        :param app_filer: the app attributes to filter for.
        :type app_filter: dict
        :yields: dict()
        """
        for form in self.form_list:
            if form_filter.items() <= form.items():
                if app_filter.items() <= form.get('app', {}).items():
                    yield(form)

    def poll(self):
        """Poll fleetingforms and process completed actions.

        :returns: a list of forms successfully processed and a list of forms
                  that encountered errors.
        :rtype: (list, list)
        """
        app_filter = {'org': self.org}
        # Filter our complete forms for this org.
        for form in self.form_list_filtered_by({'status': 'completed'},
                                               app_filter):
            try:
                # Get a handler for this form type.
                handler_class = self.handlers[form['app']['type']]

                # Create a new instance, validate and apply the action
                handler = handler_class(form)
                handler.validate()
                handler.apply()

                # Track stats and log/notify
                self.successes.append((form, True, ))
                # _alert("[{}] - successfully applied.".format(form['code']))
            except PollerWorkflowInstanceDeletedError:
                self.log.debug("Cleaning up form {}".format(form))
                handler.cleanup()
            except Exception as e:
                # Log the error and track the form in errors.
                self.errors.append((form, e, ))
                _error("[{}] - error while applying: {}".format(
                        form['code'], e))
                # Flush Sage errors to the log for debugging
                self._flush_error_stack_to_log(form)

        # Find all forms in error for this org and log.
        # Deletion of the form deferred until cleanup.
        for form in self.form_list_filtered_by({'status': 'error'},
                                               app_filter):
            if app_filter.items() <= form['app'].items():
                raise PollerFormInError(
                        "[{}] - is in an error state.".format(
                            form.get('code', 'unset')))

        # After processing completed forms and those in error,
        # clean up all processed forms from the service.
        if self.clean:
            self.cleanup()

        return (self.successes, self.errors)

    def cleanup(self):
        """Delete all successfully processed forms from the service.

        :returns: None
        """
        processed = self.successes + self.errors
        self.log.debug('[clean] - cleaning up {} forms.'.format(len(processed)))
        for (form, status) in processed:
            try:
                self.client.delete(form['id'])
                self.log.info("[{}] - deleted action {}.".format(
                        form['code'], form['id']))
            except Exception as e:
                self.errors.append((form,
                        PollerDeleteError(
                        "Failed to delete the entry {}: {}".format(
                                form.get('code', 'unset'), e)),
                        ))

        # Clear the cache of forms for this org.
        self.__form_list.clear()

