#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import Kpi, ruleLimit

from ..graphql.input.edit_rule_limit_input import EditRuleLimitInput
from ..graphql.input.add_rule_limit_input import AddRuleLimitInput
from ..graphql.mutation.add_rule_limit import addRuleLimit
from ..graphql.mutation.edit_rule_limit import editRuleLimit
from ..graphql.mutation.remove_rule_limit import removeRuleLimit
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_rule_limit(
    client: SymphonyClient, 
            number: int,
            limitType: str,
            comparator: str,
            rule: str,
) -> ruleLimit:
   
    rule_limit_input = AddRuleLimitInput(            
            number= number,
            limitType=limitType,
            comparator=comparator,
            rule=rule,)
    result = addRuleLimit.execute(client, input=rule_limit_input)
    return ruleLimit(            
            id=result.id,
            number=result.number,
            limitType=result.limitType,
            comparator=result.comparator,
            rule=result.rule,)


def edit_rule_limit(
    client: SymphonyClient,
    rule_limit: ruleLimit,
    new_number: Optional[int] = None,
    limitType: str= None,
    comparator: str= None,
    rule: str= None,
) -> None:
    params: Dict[str, Any] = {}
    if new_number is not None:
        params.update({"_name_": new_number})
    if new_number is not None:
        editRuleLimit.execute(client, input=EditRuleLimitInput(
        id=rule_limit.id, 
        number= new_number,
        limitType=limitType,
        comparator=comparator,
        rule=rule))



def remove_rule_limit(client: SymphonyClient, id: str) -> None:
    removeRuleLimit.execute(client, id=id)


