try:
    from accpac import *
except ImportError:
    pass

from remote_actions import get_logger
from remote_actions.handlers import FormHandler
from remote_actions.pollers.errors import (
        PollerWorkflowSaveError,
        PollerValidationError, )

class WorkflowApprovalFormHandler(FormHandler):
    """Handle a workflow approval form.

    This handler validates that a workflow approval form has
    all the required fields and progresses to the next step based
    on the user action.

    :param form: the form to handle.
    :type form: dict
    """

    type = 'workflow_approval'

    def __init__(self, form):
        super(WorkflowApprovalFormHandler, self).__init__(form)
        self.log = get_logger("WorkflowApprovalFormHandler")
        self.app = None
        self.wiid = None
        self.steps = None
        self.stepname = None
        self.result_action = None
        self._validated = False

    def cleanup(self):
        pass

    def validate(self):
        """Validate a completed workflow approval self.form.

        Sets:
          - self.stepname: next workflow step
          - self.wiid: workflow instance id
          - self.app: app parameters for this form

        :returns: validated form
        :rtype: dict
        :raises: PollerValidationError
        """

        self.app = self.form.get('app', {})
        self.wiid = self.app.get('wiid')

        # forms must have a valid workflow instance id
        if not self.wiid:
            raise PollerValidationError(
                    "action {} has no workflow ID set.".format(
                        self.form.get('code', 'unset')))

        # and a mapping of form actions to steps.
        self.steps = self.app.get('steps', {})
        if not self.steps:
            raise PollerValidationError(
                    "action {} has no steps set.".format(
                        self.form.get('code', 'unset')))

        # an action must have been performed and recorded (i.e. Approve)
        self.result_action = self.form.get('result', {}).pop('action', None)
        if not self.result_action:
            raise PollerValidationError(
                    "No form actions for remote action {}".format(
                        self.form.get('code', 'unset')))

        # there must be a step to progress to for that action.
        self.stepname = self.steps.get(self.result_action)
        if not self.stepname:
            raise PollerValidationError(
                    "action {} has no stepname for {}.".format(
                            self.form.get('code', 'unset'),
                            self.result_action))

        # all is well.
        self._validated = True
        return self.form

    def apply(self):
        """Apply a workflow validation form.

        Applies a workflow validation form by setting the result
        values in the workflow instance values and progressing the
        workflow to the next step.

        :returns: True
        :raises: PollerError
        """
        if not self._validated:
            raise PollerValidationError(".validate() must be called on the "
                                        "form before .apply().")
        # Validate sets self.app, self.wiid, self.stepname
        wi = WorkflowInstance()
        _r = wi.loadInstance(self.wiid)

        if _r != 0:
            raise PollerValidationError(
                    "failed to load Workflow Instance {}".format(self.wiid))

        # Copy all keys from the result into the workflow values.
        result = self.form.get('result', {})
        self.log.debug("[{}] - result: {}.".format(self.form['code'], result))
        for (key, value) in result.items():
            wi.setValue(key, value)

        # If the RUNUSER result key is set, use it to change the
        # user executing the action.
        runuser = result.get("RUNUSER", user)
        wi.viworkih.put("RUNUSER", runuser)
        upd = wi.viworkih.update()
        if upd != 0:
            self.log.error("[{}] - error setting RUNUSER field to {} in "
                         "workflow header. .update() returned '{}'.".format(
                self.form['code'], runuser, upd))

        # Progress the workflow to the next step.
        self.log.info('[{}] - progressing WIID {} to STEP {} as USER {}.'.format(
                self.form['code'], self.wiid, self.stepname, runuser))
        r = wi.progressTo(self.stepname)
        if r != 0:
            raise PollerWorkflowSaveError(
                    "Failed to progress to STEP {} for WIID {}".format(
                            self.stepname, self.wiid))

        # First call succeeds only if the workflow has no params
        if wi.save() == 0:
            return True
        elif wi.parameters != None:
            # Secondcall succeeds for workflows with params
            if wi.save == 0:
                return True

        # In any other case, the save has truly failed.
        raise PollerWorkflowSaveError(
                "Failed to save WIID {} after progress to STEP {}".format(
                         self.wiid, self.stepname,))
