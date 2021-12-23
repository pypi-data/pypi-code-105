## P1 AP Invoice Batch Number
"""
This workflow action generates a an A/P Batch Listing report and stores
the path in the ARINVRPTPATH Workflow Instance Vairable.
"""
from accpac import *

from pathlib import Path

REPORT_WAIT_RETRIES = 5
REPORT_WAIT_SLEEP = 2

def workflow(e):
    """Execute the workflow step.

    This function is invoked by the workflow engine. It generates a new A/P
    Invoice Batch Listing and sets the ARINVRPTPTH workflow variable.

    :param e: the workflow arguments for this action.
    :type e: ``accpac.WorkflowArgs``
    :returns: 0/1
    :rtype: int
    """
    batch_number = e.wi.getViewKey()
    filename = "{}-AP_Invoice_Batch_Listing.pdf".format(batch_number)
    report_dir = Path(getOrgPath(), "ap_invoices")
    if not report_dir.exists():
        report_dir.mkdir()

    report_path = report_dir / filename

    if generate_ap_invoice_batch_report(report_path, batch_number):
        e.wi.setValue("APINVRPTPATH", str(report_path))
        return 0

    return 1

def generate_ap_invoice_batch_report(report_path, cntbtch):
    """Generate an A/P Batch Listing Report.

    :param report_path: Path to write the report file to.
    :type report_path: pathlib.Path or str
    :returns: report path on success, else ""
    :rtype: str
    """
    report = Report()
    report.reportName = "APIBTCLZ"

    report.destination = "file"
    report.printDirectory = str(report_path)

    try:
        report.setParameter("FROMBATCH", cntbtch)
        report.setParameter("TOBATCH", cntbtch)
        report.setParameter("FROMDATE", "19990101")
        report.setParameter("TODATE", "20510311")
        report.setParameter("SHOWJOB", "1")
        report.setParameter("TAXDETAIL", "1")
        report.setParameter("SCHED", "Y")
        report.setParameter("SHOWCMTS", "1")
        report.setParameter("SWRET", "1")
        report.setParameter("RETDETAIL", "1")
        report.setParameter("INCLPRNDBTCH", "1")
        report.setParameter("ENTERED", "1")
        report.setParameter("IMPORTED", "2")
        report.setParameter("GENERATED", "3")
        report.setParameter("RECURRING", "4")
        report.setParameter("EXTERNAL", "5")
        report.setParameter("RETAINAGE", "6")
        report.setParameter("OPEN", "1")
        report.setParameter("READYPOST", "7")
        report.setParameter("POSTED", "3")
        report.setParameter("BATCHTYPE", "Entered, Imported, Generated, Recurring, External, Retainage")
        report.setParameter("BATCHSTATUS", "Open, Ready To Post, Posted")
        report.setParameter("FCURNDEC", "2")
        report.setParameter("MULTCURN", "N")
        report.setParameter("SWPMACTIVE", "1")
        report.setParameter("CONTRACT", "Contract")
        report.setParameter("PROJECT", "Project")
        report.setParameter("CATEGORY", "Category")
        report.setParameter("OPTFLDS?", "Y")
        report.setParameter("SHOWRCWHT", "1")
        report.print(None)
    except Exception as err:
        _debug("Report generation exception: {}".format(err))
        return ""

    tries = 0

    while tries < REPORT_WAIT_RETRIES:
        if report_path.exists():
            return report_path
        tries += 1
        time.sleep(REPORT_WAIT_SLEEP)

    return ""


