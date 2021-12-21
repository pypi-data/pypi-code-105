#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

from dataclasses import dataclass, field


@dataclass
class CliOptions:
    config: str = field(repr=False, metadata=dict(args=["config"]), default='config')
    login: str = field(repr=False, metadata=dict(args=["login"]), default='login')
    profile: str = field(repr=False, metadata=dict(args=["--profile"]), default='profile')
