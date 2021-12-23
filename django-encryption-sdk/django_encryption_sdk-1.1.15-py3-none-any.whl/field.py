from django.db.models import CharField
from django.utils.translation import gettext_lazy as _


import logging

from .client import DataKeeper, crypto_client

logger = logging.getLogger(__name__)


class EncryptCharField(CharField):
    description = _("Encrypt String (base CharField)")

    def __init__(self, *args, edk_key='default', nonce=None, raw_type='str', raw_default='', **kwargs):
        """
        原始CharField
        """
        self.edk_key = edk_key
        self.raw_type = raw_type
        self.raw_default = raw_default
        self.nonce = nonce
        super().__init__(*args, **kwargs)

    # 将会在从数据库中载入的生命周期中调用，包括聚集和 values() 调用
    def from_db_value(self, value, expression, connection):
        if value is None:
            return value
        return self.to_python(value)

    # 回显python
    def to_python(self, value):
        if value is None:
            return value
        if isinstance(value, str):
            return crypto_client(self.edk_key).decrypt(value)
        return str(value)

    # 录入db
    def get_prep_value(self, value):
        # encode
        return crypto_client(self.edk_key).encrypt(value, self.nonce)


class DataKeeperCharField(CharField):
    description = _("Plain Data Keeper String (base CharField)")

    def __init__(self, *args, mask_type="auto", edk_key='default', nonce=None, raw_type='str', raw_default='', **kwargs):
        """
        mask_type: [num1] (*|**) [num2]
        num1:前num1位明文显示
        (*|**): *表示固定三个*，(即***)，**表示按遮挡长度显示*
        num2: 后num2位明文显示
        """
        self.mask_type = mask_type
        self.edk_key = edk_key
        self.raw_type = raw_type
        self.raw_default = raw_default
        self.nonce = nonce
        super().__init__(*args, **kwargs)

    def from_db_value(self, value, expression, connection):
        """
        将会在从数据库中载入的生命周期中调用，包括聚集和 values() 调用
        """
        if value is None:
            return value
        return self.to_python(value)

    def to_python(self, value):
        """
        回显python
        """
        if value is None:
            return value

        if isinstance(value, DataKeeper):
            return value

        return DataKeeper(cipher_text=value, mask_type=self.mask_type, edk_key=self.edk_key, field=self,
                          raw_type=self.raw_type, raw_default=self.raw_default, nonce=self.nonce)

    def get_prep_value(self, value):
        """
        落库
        """
        if value is None:
            return ""
        if isinstance(value, DataKeeper):
            return value.cipher()

        dk = DataKeeper(plain_text=value, edk_key=self.edk_key, raw_type=self.raw_type, nonce=self.nonce)
        return dk.cipher()

    def deconstruct(self):
        name, path, args, kwargs = super().deconstruct()
        # Only include kwarg if it's not the default
        if self.nonce is not None:
            kwargs["nonce"] = self.nonce
        if self.mask_type != "auto":
            kwargs["mask_type"] = self.mask_type
        if self.edk_key != 'default':
            kwargs["edk_key"] = self.edk_key
        if self.raw_type != 'str':
            kwargs["raw_type"] = self.raw_type
        if self.raw_default != '':
            kwargs["raw_default"] = self.raw_default
        return name, path, args, kwargs

