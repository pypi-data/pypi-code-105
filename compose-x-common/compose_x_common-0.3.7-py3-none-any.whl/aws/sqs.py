﻿#   -*- coding: utf-8 -*-
#  SPDX-License-Identifier: MPL-2.0
#  Copyright 2020-2021 John Mille <john@compose-x.io>
import re

SQS_QUEUE_ARN_RE = re.compile(
    r"^arn:aws(?:-[a-z]+)?:sqs:[\S]+:(?P<accountid>[0-9]{12}):(?P<id>[\S]+)$"
)
