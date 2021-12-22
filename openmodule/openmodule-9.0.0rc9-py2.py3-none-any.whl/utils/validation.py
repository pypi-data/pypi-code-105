import logging

from openmodule.core import OpenModuleCore
from openmodule.models.backend import AccessRequest
from openmodule.models.validation import ValidationProviderRegisterRequestMessage, ValidateResponse, ValidateRequest, \
    ValidationProviderRegisterMessage, ValidationProviderUnregisterMessage
from openmodule.rpc.server import RPCServer


class ValidationProvider:
    """
    Validation provider template class
    provides basic functionality used for validation providers
    * subscribes to ValidationProviderMessages and automatically registers validation_provider
    * provides method for the validation_provider / validate rpc with the validate_ticket method
    """

    def __init__(self, core: OpenModuleCore, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.core = core
        self.log = logging.getLogger()

        self.register_at_controller()
        # BEWARE there is already a channel named "validation", see validation search in skidata-hostcom
        self.core.messages.register_handler(b"validation_provider", ValidationProviderRegisterRequestMessage,
                                            self.handle_validation_provider_register_request,
                                            match_type=True)

    def register_rpcs(self, rpc_server: RPCServer):
        rpc_server.add_filter(self._validation_provider_filter, "validation_provider", "validate")
        rpc_server.register_handler("validation_provider", "validate", request_class=ValidateRequest,
                                    response_class=ValidateResponse, handler=self.rpc_validate_ticket)

    def _validation_provider_filter(self, request, message, handler) -> bool:
        validation_provider = request.name
        if not validation_provider:
            return False
        return self.core.config.NAME == validation_provider

    def validate_ticket(self, request: ValidateRequest) -> ValidateResponse:
        """
        This method should validate a ticket for an occupant
        it should return a response with an error code if it fails
        :param request: ValidateRequest
        :return: ValidateResponse
        """
        raise NotImplementedError()

    def shutdown(self):
        self.unregister_at_controller()

    def rpc_validate_ticket(self, request: ValidateRequest, _) -> ValidateResponse:
        """
        Checks and validates a ticket for an occupant
        """

        response: ValidateResponse = self.validate_ticket(request)
        if response.cost_entries:
            for cost_entry in response.cost_entries:
                # if no source is set, source will be set to service_name: e.g. "service_iocontroller"
                if not cost_entry.source:
                    # 1. replace: removing service prefix: "om_"
                    # 2. replace: removing instance suffix: e.g. "_1", "_2"
                    cost_entry.source = self.core.config.NAME \
                        .replace(r"^om_", "") \
                        .replace(r"_\d+$", "")

        return response

    def handle_validation_provider_register_request(self, _):
        """
        Registers the validation provider if the message type is register_request
        """
        self.register_at_controller()

    def register_at_controller(self):
        self.core.publish(ValidationProviderRegisterMessage(), b"validation_provider")

    def unregister_at_controller(self):
        self.core.publish(ValidationProviderUnregisterMessage(), b"validation_provider")
