from datetime import datetime
from enum import Enum
from typing import List, Optional

from openmodule.models.base import OpenModuleModel, ZMQMessage, timezone_validator, base64_validator, \
    datetime_to_timestamp


class ValidationProviderRequestTicketType(str, Enum):
    qr = "qr"


class ValidationProviderResponseState(str, Enum):
    ok = "ok"
    not_applicable = "not_applicable"


class ValidationProviderResponseCommonError(str, Enum):
    # unique validation id was already used
    already_used = "already_used"
    # e.g. signature validation error
    invalid = "invalid"
    expired = "expired"
    outside_timewindow = "outside_timewindow"
    unknown_error = "unknown_error"


class ValidationProviderRegisterRequestMessage(ZMQMessage):
    """
    sent by the controller as a request to all validation providers
    each validation provider who wants to register itself at the controller has to answer
    with a register message
    """
    type: str = "register_request"


class ValidationProviderRegisterMessage(ZMQMessage):
    """
    sent by a validation provider if it wants to register itself at the controller
    """
    type: str = "register"


class ValidationProviderUnregisterMessage(ZMQMessage):
    """
    sent by a validation provider if it shuts down and wants to unregister itself
    """
    type: str = "unregister"


class ValidateRequest(OpenModuleModel):
    name: str
    occupant_id: str
    type: ValidationProviderRequestTicketType
    # payload has to be base64 encoded
    payload: str

    _b64_payload = base64_validator("payload")


class ValidateResponseError(OpenModuleModel):
    type: ValidationProviderResponseCommonError
    start: Optional[datetime]
    end: Optional[datetime]

    _tz_start = timezone_validator("start")
    _tz_end = timezone_validator("end")

    def dict(self, **kwargs):
        data = super().dict(**kwargs)
        if data.get("start") is not None:
            data["start"] = datetime_to_timestamp(data["start"])
        if data.get("end") is not None:
            data["end"] = datetime_to_timestamp(data["end"])
        return data


class ValidateCostEntry(OpenModuleModel):
    # common parameters
    group: Optional[str] = None

    # if None, source will be set to service name on default: e.g. "service_iocontroller"
    source: Optional[str] = None

    # product item switches
    product_item_id: Optional[str] = None

    # enable/disable the cost group
    active: Optional[bool] = None

    # time validations
    delta_time_seconds: Optional[int] = None

    # amount payments
    delta_amount: Optional[int] = None


class ValidateResponseCostEntry(ValidateCostEntry):
    # common parameters
    source_id: Optional[str] = None
    idempotency_key: Optional[str] = None


class ValidateResponse(OpenModuleModel):
    occupant_id: str
    state: ValidationProviderResponseState
    error: Optional[ValidateResponseError]
    cost_entries: Optional[List[dict]]
