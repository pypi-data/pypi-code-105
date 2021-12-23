## P1 Output File Path
"""
This workflow action downloads the audit report for a transaction and
saves it to the provided file path.
"""
try:
    from accpac import *
except ImportError:
    pass

from pathlib import Path

from remote_actions import get_logger
from remote_actions.services.adobe_sign import (
        AdobeSignClient, agreement_id_for_wiid, )

VERSION = '6.0.12'

def workflow(e):
    """Execute the workflow step.

    This function is invoked by the workflow engine. It downloads
    the audit report for the agreement and writes them in
    the path defined in P1.

    :param e: the workflow arguments for this action.
    :type e: ``accpac.WorkflowArgs``
    :returns: 0/1
    :rtype: int
    """

    wiid = e.wi.viworkih.get("WIID")
    if not wiid:
        error("Failed to get workflow ID.")
        return 1

    logger = get_logger("DownloadAdobeSignAgreementAuditReport wiid({})".format(wiid))

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
    logger.info("writing agreement {} audit report to {}.".format(
            agreement_id, output_path))

    with output_path.open('wb') as f:
        f.write(ac.download_agreement_audit_report(agreement_id))

    return 0
