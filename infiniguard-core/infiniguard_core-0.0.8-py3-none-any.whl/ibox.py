import infinisdk
import logging
from distutils.version import LooseVersion
from .consts import SUPPORTED_VERSIONS, IBOX_HOSTNAME
from .credentials import (
    IBOX_CREDENTIALS_KEY, load_credentials, save_credentials, IGUARD_TENANT_NAME_KEY,
    CredentialsKeyNotFoundInStore
)
from infi.caching import cached_function

logger = logging.getLogger(__name__)


class IBoxException(Exception):
    pass


class UnsupportedIBoxVersion(IBoxException):
    pass


class UnsupportedIBoxModel(IBoxException):
    pass


class TenantNotFound(IBoxException):
    pass


@cached_function
def get_ibox():
    logger.info(f"Connecting to InfiniBox '{IBOX_HOSTNAME}'")

    ibox = infinisdk.InfiniBox(IBOX_HOSTNAME, use_ssl=True, auth=load_credentials(IBOX_CREDENTIALS_KEY))
    ibox.api._use_basic_auth = True

    tenant = get_iguard_tenant(ibox)
    if tenant:
        ibox.api._session.headers['X-INFINIDAT-TENANT-ID'] = str(tenant.get_id())

    ibox_version = LooseVersion(ibox.get_version())
    if ibox_version not in SUPPORTED_VERSIONS:
        raise UnsupportedIBoxVersion(f"Infinibox version {ibox_version} "
                                     f"is not supported by this version of InfiniGuard")

    logger.debug(f'InfiniBox version: {ibox_version}')
    logger.debug(f"Infinibox serial: '{ibox.get_serial()}'")
    logger.debug(f"Infinibox is_active: '{ibox.is_active()}'")

    return ibox


def get_iguard_tenant(ibox):
    try:
        tenant_name = load_credentials(IGUARD_TENANT_NAME_KEY)[1]
    except CredentialsKeyNotFoundInStore:
        logger.debug("Could not find tenant in credential store")
        return None

    try:
        tenant = ibox.tenants.get(name=tenant_name)
    except infinisdk.core.exceptions.ObjectNotFound:
        raise TenantNotFound(f"Tenant name exists in credential store, but not in InfiniBox")

    return tenant


