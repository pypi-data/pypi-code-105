try:
    from accpac import *
except ImportError:
    pass

from pprint import pformat

from remote_actions import get_logger, user_for_email
from remote_actions.services.adobe_sign import (
        AdobeSignClient, AGREEMENTS_VIEW, update_agreement_status)
from remote_actions.handlers import FormHandler
from remote_actions.pollers.errors import (
        PollerWorkflowSaveError,
        PollerValidationError,
        PollerWorkflowInstanceDeletedError,
        PollerStartupError, )

class AdobeSignAgreementHandler(FormHandler):
    """Handle an Adobe Sign Agreement.

    This handler validates that an agreement has been signed and progresses to
    the next step based on the user action.

    :param agreement: the agreement to handle.
    :type agreement: dict
    """

    type = 'adobe_sign_workflow'

    COMPLETE_STATUSES = ["SIGNED", "APPROVED"]
    REJECT_STATUSES = ["EXPIRED", "CANCELLED", "ARCHIVED"]

    def __init__(self, agreement):
        self.log = get_logger("AdobeSignAdreementHandler")
        self.log.info("starting handler for agreement:\n{}".format(
            pformat(agreement)))
        self.wiid = None
        self.stepname = None
        self._validated = False
        self.agreement = agreement
        try:
            self.client = AdobeSignClient()
        except RuntimeError as e:
            raise PollerStartupError(str(e))
        self.wiid = self.wiid_for_agreement(agreement.get("id"))
        self.steps = self.steps_for_agreement(agreement.get("id"))
        self.signers = [m['memberInfos'][0]['email']
                        for m in agreement.get('participantSetsInfo', [])]


    def cleanup(self):
        """Clean up the agreement for this handler.

        :returns: True if deleted, else False
        :rtype: bool
        """
        agreements = openView(AGREEMENTS_VIEW)
        agreements.put("AGREEID", self.agreement.get("id"))
        if agreements.read() != 0:
            return True
        d = agreements.delete()
        agreements.close()
        if d == 0:
            return True
        return False

    def wiid_for_agreement(self, agreement_id):
        """Get the workflow ID for a given Agreement.

        :param agreement_id: agreement ID.
        :type agreement_id: str
        :returns: workflow ID or None
        :rtype: int
        """
        agreements = openView(AGREEMENTS_VIEW)
        agreements.put("AGREEID", agreement_id)
        if agreements.read() != 0:
            return None
        wiid = agreements.get("WIID")
        agreements.close()
        return wiid

    def steps_for_agreement(self, agreement_id):
        """Get the next steps for an agreement.

        :param agreement_id: agreement ID.
        :type agreement_id: str
        :returns: approve, reject, error states or ()
        :rtype: ([str, ], str, str)
        """
        agreements = openView(AGREEMENTS_VIEW)
        agreements.put("AGREEID", agreement_id)
        if agreements.read() != 0:
            return tuple()
        signed = agreements.get("SIGNEDSTEP").split(',')
        rejected = agreements.get("REJECTSTEP")
        error = agreements.get("ERRORSTEP")
        agreements.close()
        return (signed, rejected, error)

    def next_step_for(self, status):
        """Get the next step in the worflow given the agreement status.

        :param status: agreement status.
        :type status: str
        :returns: stepname or "" if no next step.
        """
        self.log.debug("getting next_step_for {} from {}".format(
                status, self.steps))
        # TODO: enable advance on partial signing
        if status in self.COMPLETE_STATUSES:
            # Return the final step in the approved chain.
            return self.steps[0][-1]
        if status in self.REJECT_STATUSES:
            # Return the reject step
            return self.steps[1]
        else:
            # Check on the signing status.
            self.log.debug("checking partial signing status {}".format(
                self.signed_by()))
            if self.signed_by():
                last_signer = self.signed_by()[-1]
                step_index = self.signers.index(last_signer)
                self.log.debug("signer {}, index {} {}, next step {}".format(
                    last_signer, step_index, self.steps[0],
                    self.steps[0][step_index]))
                return self.steps[0][step_index]
        return ""

    def signed_by(self):
        """Get the list of signatures obtained for this document.

        :returns: stepname or "" if no next step.
        """
        events = self.client.agreement_events(self.agreement['id'])
        signed_by = [
            e['participantEmail']
            for e in events if e['type'] == "ACTION_COMPLETED"
        ]
        return signed_by

    def validate(self):
        """Validate a signed document.

        :returns: validated agreement details
        :rtype: dict
        :raises: PollerValidationError
        """
        # the agreement must have a valid id
        if not self.agreement.get('id'):
            raise PollerValidationError(
                    "agreement has no 'id' atribute.")

        # agreements must have a valid workflow instance id
        if not self.wiid:
            raise PollerValidationError(
                    "agreement {} has no workflow ID set.".format(
                        self.agreement.get("id")))

        # and a mapping of form actions to steps.
        if not self.steps:
            raise PollerValidationError(
                    "agreement {} has no steps set.".format(
                         self.agreement.get("id")))

        # all is well.
        self._validated = True
        return self.agreement

    def apply(self):
        """Apply an Agreement.

        Applies an agreement to its workflow by setting the result
        values in the workflow instance values and progressing the
        workflow to the next step.

        :returns: True if progressed, None on no action
        :raises: PollerError
        """
        if not self._validated:
            raise PollerValidationError(".validate() must be called on the "
                                        "form before .apply().")
        # Validate sets self.app, self.wiid, self.stepname
        wi = WorkflowInstance()
        _r = wi.loadInstance(self.wiid)
        if _r != 0:
            # Workflow instance no longer exists
            raise PollerWorkflowInstanceDeletedError(
                    "Workflow instance {} doesn't exist.".format(
                        self.wiid))

        # Copy all keys from the result into the workflow values.
        status = self.agreement.get('status', "")
        next_step = self.next_step_for(status)
        self.log.debug("[{}] - status: {} - next: {}.".format(
                self.agreement['id'], status, next_step))

        if not next_step:
            return None

        try:
            runuser_email = self.signed_by()[-1]
            runuser = user_for_email(runuser_email)
        except Exception as e:
            self.log.error("Failed to lookup runuser: {}".format(e))
            runuser = "ADMIN"

        # If the RUNUSER result key is set, use it to change the
        # user executing the action.
        # runuser = result.get("RUNUSER", user)
        wi.viworkih.put("RUNUSER", runuser)
        upd = wi.viworkih.update()

        if upd != 0:
            self.log.error("[{}] - error setting RUNUSER field to {} in "
                         "workflow header. .update() returned '{}'.".format(
                self.agreement.get("id"), runuser, upd))

        # Progress the workflow to the next step.
        self.log.info('[{}] - progressing WIID {} to STEP {} as USER {}.'.format(
                self.agreement['id'], self.wiid, next_step, runuser))
        r = wi.progressTo(next_step)
        if r != 0:
            raise PollerWorkflowSaveError(
                    "Failed to progress to STEP {} for WIID {}".format(
                            next_step, self.wiid))

        agreement_status = "IN PROGRESS"
        if self.agreement.get("status") in \
                self.COMPLETE_STATUSES + self.REJECT_STATUSES:
            agreement_status = self.agreement.get("status")

        # First call succeeds only if the workflow has no params
        if wi.save() == 0:
            self.log.debug("Workflow saved first time after progressing to STEP {}".format(next_step))
            update_agreement_status(self.agreement['id'], agreement_status)
            return True
        elif wi.parameters != None:
            # Second call succeeds for workflows with params
            if wi.save == 0:
                self.log.debug("Workflow saved second time after progressing to STEP {}".format(next_step))
                update_agreement_status(self.agreement['id'], agreement_status)
                return True

        # In any other case, the save has truly failed.
        raise PollerWorkflowSaveError(
                "Failed to save WIID {} after progress to STEP {}".format(
                         self.wiid, next_step,))
