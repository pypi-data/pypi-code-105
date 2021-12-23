"""
The poller component connects to fleetingforms.io using
a Sage Company's unique token and downloads any actions that have been
completed or are in error.

On every execution, the poller takes the following steps::

    for each form in the polling results:
        if the form is completed and workflow related:
            progress the workflow based on the user action
        if the form is in error:
            log the error

    delete all processed forms
    log a summary of the actions taken

The poller can be executed from the Scripts panel or run using
:ref:`Process Scheduler <running-the-poller-with-process-scheduler>`.

The poller logs to
``Sage300/SharedData/Company/<ComanyName>/ppforms.poll.log``
"""
try:
    from accpac import *
except ImportError:
    pass

import datetime

from extools.env import execution_context, EXEC_VI, EXEC_PS

from remote_actions import get_logger, get_log_path, _alert, _error
from remote_actions.pollers.errors import (
        PollerError, 
        PollerStartupError, )
from remote_actions.pollers.adobe_sign import AdobeSignPoller
from remote_actions.pollers.fleeting_forms import FleetingFormPoller

# Version information for debugging
VERSION = '6.0.12'

def main(*args, **kwargs):
    """Entry point for execution - perform a poll."""

    # Configure a logger to write to the log file.
    global logger

    uniquifier = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    log_path = get_log_path("poller", uniquifier)
    logger = get_logger("poller", uniquifier)

    logger.info("[start] - version {}, org {}, user {}, program {}.".format(
            VERSION, org, user, program))

    # Create a new poller for this organization and poll.
    successes, errors = [], []

    for poller in [AdobeSignPoller, FleetingFormPoller, ]:
        try:
            p = poller(org)
            if p.configured:
                s, e = p.poll()
                successes.extend(s)
                errors.extend(e)
            else:
                logger.info("Poller {} not configured.".format(poller))
        except PollerStartupError:
            logger.warn("Poller {} not configured or failed to start.".format(
                    poller.__class__.__name__))
        except PollerError as e:
            # _error("Error in poller: {}".format(e))
            errors.append(repr(e))
            logger.error(repr(e))
        except Exception as e:
            # _error("General failure in poller: {}".format(e))
            errors.append(repr(e))
            logger.error(repr(e))

    summary = """
    Polling complete.

    {} approvals applied successfully
    {} errors encountered.

    See the details in the PS Log.
    """.format(len(successes), len(errors))
    _alert(summary)

    if execution_context() == EXEC_PS:
        # When running through PS, log a completion message.
        log_message = "{}|{}|{}".format(
                "ERR" if errors else "OK",
                len(errors),
                log_path)
        log(log_message)

    if execution_context() == EXEC_VI:
        # When running through the scripts panel, close the empty UI.
        # This fails on Extender 9/10:
        # UI().closeUI()
        pass

