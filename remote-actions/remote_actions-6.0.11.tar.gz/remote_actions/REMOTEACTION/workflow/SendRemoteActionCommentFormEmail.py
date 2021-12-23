## P1 Email template
## P1.FinderView=VI0008
## P1.FinderField=MSGID
## P1.FinderFields=MSGID,TEXTDESC,SUBJECT,COMMENTS,BODY
## P2 To
## P3 Form template
## P3.FinderView=VI0008
## P3.FinderField=MSGID
## P3.FinderFields=MSGID,TEXTDESC,SUBJECT,COMMENTS,BODY
## P4 Form button lists
"""
This workflow action sends a credit limit approval form link in
an email to one or more users.

The form has a title, content, a credit limit float field,
a long form comments box, and Approve/Reject buttons::

    Title

    Content

    Sage User: ____________________________
    Credit Limit: _________________________
    Comments: _____________________________

    Approve | Reject

The action takes the following parameters:

- Parameter1: Email Notification Template - sent to users to notify that
  that a form is available.
- Parameter2: To list of Sage Users or Extender User Groups
- Parameter3: Form Title and Content Template - template to render for form
  title (message subject) and content (message body)
- Parameter4:
  Approve=ApproveStepName,Reject=RejectStepName,Cancel=CancelStepName - steps
  to proceed to when approved/rejected/cancelled etc, comma separated.
"""
try:
    from accpac import *
except ImportError:
    pass

import base64

from remote_actions.services.fleeting_forms import (
        create_workflow_approval_form, )
from remote_actions import (
        resolve_users,
        render_title_and_content_for,
        parse_action_parameter,
        get_logger, )

VERSION = '6.0.11'

form_controls =  [
                    {
                      'name': 'RUNUSER',
                      'type': 'text',
                      'label': 'Sage User',
                      'required': True,
                      'disabled': True
                    },
                    {
                      'name': 'APPROVALCOMMENT',
                      'type': 'text',
                      'label': 'Comments',
                      'help_text': 'Enter your comment',
                      'required': True,
                    }
                ]

def workflow(e):
    """Execute the workflow step.

    This function is invoked by the workflow engine.  It is called
    with ``accpac.WorkflowArgs`` and must return ``0`` on success and
    ``1`` on failed.

    :param e: the workflow arguments for this action.
    :type e: ``accpac.WorkflowArgs``
    :returns: 0/1
    :rtype: int
    """

    wiid = e.wi.viworkih.get("WIID")
    if not wiid:
        error("Failed to get workflow ID.")
        return 1

    logger = get_logger("SendRemoteActionCommentFormEmail wiid({})".format(
                            wiid))


    # Parse the actions from P4 into a { label: nextstep, } data structure
    action_param = e.resolve(e.p4)
    try:
        actions = parse_action_parameter(action_param)
    except (IndexError, ValueError):
        showMessageBox("The actions (P4) must be a comma-separated list "
                       "of label=nextstep pairs, "
                       "eg. 'Approve=Approved+RTP,Reject=Rejected'" )
        logger.exception("P4 invalid {}".format(action_param))
        return 1

    # Create the form, setting the initial value for the credit limit.
    try:
        title, content = render_title_and_content_for(e.resolve(e.p3), e)
        form = create_workflow_approval_form(
                            e.wi.viworkih.get("WIID"),
                            form_controls,
                            title[:120],
                            content[:5000],
                            actions, )
    except Exception as exc:
        showMessageBox("Failed to create approval form: {}".format(exc))
        logger.exception("failed to create form: {}".format(exc))
        return 1

    # Get the url for the form.
    url = form.get('url')
    if not url:
        error("Unable to get approval form URL.")
        return 1

    # And set it in the workflow for troubleshooting and posterity
    e.wi.setValue("FORMURL", url)

    # Resolve all users, groups, and emails from P2
    users = resolve_users(e.resolve(e.p2))

    # For each user identified, send an email with a custom link that sets
    # RUNUSER.
    sent_emails = 0
    for (username, email_address) in users:
        email = Email()
        email.setTo(email_address)

        email_template = e.resolve(e.p1)
        if not email.load(email_template):
            error("Unable to load message template {}.".format(email_template))
            return 1

        # Build a custom URL for the user that defaults the runuser field.
        b64_username = base64.urlsafe_b64encode(username.encode())
        user_url = "{}?RUNUSER=b64:{}&".format(url, b64_username.decode())

        # And interpolate it into the template
        email.replace("FORMURL", user_url)

        # Do all the remaining interpolation for Workflow, View, and Globals
        # to build the subject and body.
        email.replace("", e.wi.getView())
        email.setSubject(ReplaceFields(e.resolve(email.subject)))
        if email.textBody != None:
            email.setText(ReplaceFields(e.resolve(email.textBody)))
        if email.htmlBody != None:
            email.setHtml(ReplaceFields(e.resolve(email.htmlBody)))

        logger.debug("sending email {} to {} with url {} for wiid {}.".format(
                email_template, email_address, user_url, wiid))

        # Send the email.
        if email.send() == 0:
            sent_emails += 1
        else:
            logger.error("failed to send email to {}.".format(email_address))

    # If at least one email has been sent, the action is considered successful
    # see https://bitbucket.org/cbinckly/remote_actions/issues/6
    if not sent_emails:
        logger.error("no emails sent successfully.")
        error("Could not send any emails. "
              "Sending approval form email step failed. "
              "Check the remote actions log for more details.")
        return 1
    else:
        if sent_emails < len(users):
            message = "{} of {} emails failed to send.".format(
                len(users) - sent_emails, len(users))
            warning(message)
            logger.warn(message)

    # Success.
    return 0

