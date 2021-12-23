try:
    from accpac import *
except ImportError:
    pass

from remote_actions import get_logger, _error
from remote_actions.services.adobe_sign import AdobeSignClient
from remote_actions.pollers.errors import (
        PollerStartupError,
        PollerWorkflowInstanceDeletedError, )
from remote_actions.handlers.adobe_sign import AdobeSignAgreementHandler

class AdobeSignPoller():
    """The Adobe Sign poller retrieves signed agreements and applies them.

    :param org_: the sage company to poll for.
    :type org_: str
    """

    def __init__(self, org_, clean=True):
        self.log = get_logger("AdobeSignPoller")
        self.errors = []
        self.successes = []
        self.org = org_

        try:
            self.client = AdobeSignClient()
            self.client.setup_token()
        except Exception as e:
            raise PollerStartupError("Failed to start Adobe Sign client: {}".format(e))

        self.log.info("adobe sign poller started for org {} with clean {}".format(
                org_, clean))

    @property
    def configured(self):
        return bool(self.client.config.get("access_token"))

    def _flush_error_stack_to_log(self, agreement):
        """Flush the error stack to the log to debug errors in Sage."""
        errors = ErrorStack()
        self.log.debug("[{}] - flushing {} messages from error stack.".format(
                agreement.get('id', "none"), errors.count()))
        for i in range(0, errors.count()):
            func = self.log.debug
            priority = errors.getPriority(i)
            if priority == PRI_MESSAGE:
                func = self.log.info
            elif priority == PRI_WARNING:
                func = self.log.warn
            elif priority == PRI_MESSAGE:
                func = self.log.error
            func("[{}] - {}.".format(agreement['id'], errors.getText(i)))
        errors.clear()

    def in_progress_agreements(self):
        """Get all agreements that are not completed.

        :returns: list of agreement IDs
        :rtype: str[]
        """
        agreement_ids = []
        cs0120 = openView("CS0120")
        query = "SELECT AGREEID FROM ADBSIGNA WHERE STATUS = 'IN PROGRESS'"
        cs0120.browse(query)
        while(cs0120.fetch() == 0):
            agreement_ids.append(cs0120.get("AGREEID"))
        cs0120.close()
        return agreement_ids

    def poll(self):
        """Poll adobe sign and process signed agreements.

        :returns: a list of agreements successfully processed and a list of agreements
                  that encountered errors.
        :rtype: (list, list)
        """
        self.log.debug("starting for in progress agreements {}".format(self.in_progress_agreements()))
        for agreement_id in self.in_progress_agreements():
            agreement_details = self.client.agreement_details(agreement_id)
            try:
                # Create a new instance, validate and apply the action
                handler = AdobeSignAgreementHandler(agreement_details)
                handler.validate()
                result = handler.apply()
                if result is not None:
                    # Track stats and log/notify
                    self.successes.append((agreement_id, True, ))
            except PollerWorkflowInstanceDeletedError:
                self.log.debug("Cleaning up agreement {}".format(agreement_id))
                handler.cleanup()
            except Exception as e:
                # Log the error and track the form in errors.
                self.errors.append((agreement_id, e, ))
                _error("[{}] - error while applying: {}".format(
                        agreement_id, e))
                # Flush Sage errors to the log for debugging
                self._flush_error_stack_to_log(agreement_details)

        return (self.successes, self.errors)
