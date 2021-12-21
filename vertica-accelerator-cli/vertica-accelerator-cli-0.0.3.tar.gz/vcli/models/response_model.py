#
#  (c) Copyright 2021 Micro Focus or one of its affiliates.
#

from dataclasses import dataclass
from typing import Dict
import json


@dataclass
class ResponseModel:
    return_code: int = None
    data: Dict = None
    error_message: str = ""
    job_id: str = ""

    def __repr__(self):
        output = {}
        if self.return_code is not None:
            output['return_code'] = self.return_code
        if self.data:
            output['data'] = self.data
        if self.job_id:
            output['job_id'] = self.job_id
        if self.error_message:
            output['error_message'] = self.error_message
        return json.dumps(output, indent=4)

    def __str__(self):
        output = {}
        if self.return_code is not None:
            output['return_code'] = self.return_code
        if self.data:
            output['data'] = self.data
        if self.job_id:
            output['job_id'] = self.job_id
        if self.error_message:
            output['error_message'] = self.error_message
        return json.dumps(output, indent=4)
