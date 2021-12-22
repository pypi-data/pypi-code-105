from distutils.version import LooseVersion
from capacity import TB
from collections import namedtuple

ModelInfo = namedtuple('ModelInfo', ('nodes', 'capacity'))
SUPPORTED_MODELS = {
    'B4260': ModelInfo(3, 1025 * TB),
    'B4260N': ModelInfo(3, 1025 * TB),
    'B4306': ModelInfo(3, 1025 * TB),
    'B4212N': ModelInfo(3, 2050 * TB),
    'B4312': ModelInfo(3, 2050 * TB)
}

FRU_NODE = 4

SUPPORTED_VERSIONS = [LooseVersion("3.0.30.50"), LooseVersion("4.0.13.0"),
                      LooseVersion("4.0.12.30"), LooseVersion("4.0.41.10"),
                      LooseVersion("4.0.44.10"), LooseVersion("5.0.22.0"), LooseVersion("4.0.61.10"), LooseVersion("5.0.27.0")]
THREE_NODE_VERSION = [name for name, info in SUPPORTED_MODELS.items() if info.nodes == 3]

IBOX_HOSTNAME = 'node-master'
IBOX_USER_EMAIL = 'iba@infinidat.com'

SHARED_HOME = '/home/shared'
LINUX_GROUP = 'infinishare'
