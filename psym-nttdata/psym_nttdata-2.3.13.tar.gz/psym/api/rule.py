#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import rule, threshold, eventSeverity, ruleType

#from ..graphql.input.edit_rule_input import EditRuleInput 
from ..graphql.input.add_rule_input import AddRuleInput
from ..graphql.mutation.add_rule import addRule
#from ..graphql.mutation.edit_rule import editRule
#from ..graphql.mutation.remove_rule import removerule
#from ..graphql.query.rules import rules
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_rule(
    client: SymphonyClient, 
    name: str,
    gracePeriod: int,
    ruleType: str,
    eventTypeName: str,
    specificProblem: str,
    additionalInfo: str,
    status: bool,
    eventSeverity: str,
    threshold: str
) -> rule:
   

    rule_input = AddRuleInput(
    name=name,
    gracePeriod=gracePeriod,
    ruleType=ruleType,
    eventTypeName=eventTypeName,
    specificProblem=specificProblem,
    additionalInfo=additionalInfo,
    status=status,
    eventSeverity=eventSeverity,
    threshold=threshold
    

    )

    result = addRule.execute(client, input=rule_input)

    return rule(
    name=result.name, 
    id=result.id, 
    gracePeriod=result.gracePeriod,
    ruleType=result.ruleType,
    eventTypeName=result.eventTypeName,
    specificProblem=result.specificProblem,
    additionalInfo=result.additionalInfo,
    status=result.status,
    eventSeverity=result.eventSeverity,
    threshold=result.threshold
    )
