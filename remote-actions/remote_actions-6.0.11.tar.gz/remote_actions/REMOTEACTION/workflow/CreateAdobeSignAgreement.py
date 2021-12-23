## P1 Document Paths
## P2 Approvers
## P3 Agreement Name
## P4 Next Steps (Signed=SignedStep1,SignedStep2,...;Rejected=Step;Error=Step)

"""
This workflow action generates a new Adobe Sign Agreement from the documents
provided that is automatically sent by Adobe to  Approvers for signing.
"""
try:
    from accpac import *
except ImportError:
    pass

from pathlib import Path

from remote_actions import (resolve_users, get_logger, )
from remote_actions.services.adobe_sign import (
        AdobeSignClient,
        add_workflow_agreement,
        add_agreement_docs)

VERSION = '6.0.11'

def parse_action_parameter(value):
    """Parse the action parameter (P4) of a workflow action.

    P4 for the workflow actions defines the button labels and progress to steps
    in a separated key value pair string format::

        <label>=<next step>,<next step>;<label>=<next step>;
        Approve=Approved1,Approved+RTP;Rejected=Rejected

    :param value: the action parameter as input into the template.
    :type value: string
    :returns: label to next step name mappings
    :rtype: collections.OrderedDict
    """
    actions = {}
    steps = value.split(';')
    for step in steps:
        label, next_step = step.split('=')
        if not next_step:
            raise ValueError("The step to proceed to must be set.")
        if ',' in next_step:
            next_step = next_step.split(',')
        actions[label] = next_step
    return actions

def workflow(e):
    """Execute the workflow step.

    This function is invoked by the workflow engine. It takes all the steps
    required to start a new Adobe Sign Agreement:

    1. Upload the required documents.
    2. Create new agreement.

    After the agreement is created Adobe Sign will automatically notify
    signers.

    :param e: the workflow arguments for this action.
    :type e: ``accpac.WorkflowArgs``
    :returns: 0/1
    :rtype: int
    """

    wiid = e.wi.viworkih.get("WIID")
    if not wiid:
        error("Failed to get workflow ID.")
        return 1

    logger = get_logger("CreateAdobeSignAgreement wiid({})".format(wiid))

    # Parse the actions from P4 into a { label: nextstep, } data structure
    action_param = e.resolve(e.p4)
    try:
        actions = parse_action_parameter(action_param)
    except (IndexError, ValueError):
        showMessageBox("The actions (P4) must be a ;-separated list "
                       "of label=nextstep pairs, e.g."
                       "'Approve=Approved+RTP;Rejected=Rejected;Error=Error'")
        logger.exception("P4 invalid {}".format(action_param))
        return 1
    logger.info("parsed actions {} from {}".format(actions, action_param))

    # Get a new client and setup the token.
    ac = AdobeSignClient()

    if not ac.setup_token():
        showMessageBox("Failed to setup connection.  Check the Adobe Sign "
                       "Connect utility in Remote Actions.")
        logger.error("failed to setup connection.")
        return 1

    # Upload the documents
    doc_param = e.resolve(e.p1)
    docs = [Path(d) for d in doc_param.split(",")]
    tdids = []

    for doc in docs:
        logger.debug("Uploading document {}.".format(doc))
        tdids.append(ac.upload_document(doc))

    # Create the agreement
    users = resolve_users(e.resolve(e.p2))
    user_emails = [email for _, email in users if email]

    logger.debug("Creating new agreement '{}' for docs {} and "
                 "signers {}".format(
                     e.resolve(e.p3),
                     ", ".join([t[0:10] for t in tdids]),
                     ", ".join(user_emails)))

    aid = ac.create_agreement(e.resolve(e.p3), tdids, user_emails,
                              externalId={"id": wiid}, )

    signed_action = actions.get("Signed")
    if isinstance(signed_action, list):
        signed_action = ",".join(signed_action)

    add_workflow_agreement(
            wiid, aid, signed_action,
            actions.get('Rejected', ''), actions.get('Error', ""))

    add_agreement_docs(aid, tdids)

    logger.debug("Created new agreement {}.".format(aid))

    return 0
