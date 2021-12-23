"""
This workflow action opens the document status view from
in the Adobe Sign console using the default browser.
"""
try:
    from accpac import *
except ImportError:
    pass

import webbrowser

from remote_actions import get_logger
from remote_actions.services.adobe_sign import (
        AdobeSignClient, agreement_id_for_wiid, )

VERSION = '6.0.12'

def workflow(e):
    """Execute the workflow step.

    This function is invoked by the workflow engine. It downloads
    the combined documents for the agreement and writes them in
    the path defined in P1.

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

    logger = get_logger("ViewAdobeSignAgreementInBrowser wiid({})".format(wiid))

    ac = AdobeSignClient()
    url = ac.agreement_public_url(agreement_id_for_wiid(wiid))

    logger.debug("opening {}".format(url))
    webbrowser.open(url)

    return 0

