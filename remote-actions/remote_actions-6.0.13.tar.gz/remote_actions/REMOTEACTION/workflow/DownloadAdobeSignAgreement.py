## P1 Output File Path
"""
This workflow action generates a new Adobe Sign Agreement from the documents
provided that is automatically sent by Adobe to  Approvers for signing.
"""
try:
    from accpac import *
except ImportError:
    pass

from pathlib import Path

from remote_actions import get_logger
from remote_actions.services.adobe_sign import (
        AdobeSignClient, agreement_id_for_wiid, )

VERSION = '6.0.13'

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

    logger = get_logger("DownloadAdobeSignAgreement wiid({})".format(wiid))

    ac = AdobeSignClient()

    if not ac.setup_token():
        showMessageBox("Failed to setup connection.  Check the Adobe Sign "
                       "Connect utility in Remote Actions.")
        logger.error("failed to setup connection.")
        return 1

    # Upload the documents
    output_path = Path(e.resolve(e.p1))
    if not output_path.parent.exists():
        logger.info("creating parent path {}.".format(output_path.parent))
        try:
            output_path.parent.mkdir(parents=True)
        except:
            logger.error("failed to create output path {}".format(
                output_path.parent))
            return 1

    agreement_id = agreement_id_for_wiid(wiid)
    logger.info("writing agreement {} documents to {}.".format(
            agreement_id, output_path))

    with output_path.open('wb') as f:
        f.write(ac.download_agreement_document(agreement_id))

    logger.debug("write complete.")

    return 0
