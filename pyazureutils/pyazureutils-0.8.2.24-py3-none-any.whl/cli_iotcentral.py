"""
Azure IoT Central CLI entrypoint
"""
from logging import getLogger
from .iotcentral import iotcentral_register_device
from .status_codes import STATUS_SUCCESS, STATUS_FAILURE

def iotcentral_cli_handler(args):
    """
    CLI entry point for command: iotcentral
    """
    logger = getLogger(__name__)
    from .pyazureutils_errors import PyazureutilsError
    try:
        if args.action == "register-device":
            status = _action_register_device(args)
    except PyazureutilsError as exc:
        logger.error("Operation failed with %s: %s", type(exc).__name__, exc)
    return STATUS_FAILURE

def _action_register_device(args):
    """
    CLI entry point for action: register-device
    """
    print("Azure IoTCentral device registration\r\n")
    return iotcentral_register_device(args.app_name, args.certificate_file, args.display_name,
                                      args.subscription, args.device_template_name)
