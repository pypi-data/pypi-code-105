#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import ruleType

from ..graphql.input.edit_rule_type_input import EditRuleTypeInput
from ..graphql.input.add_rule_type_input import AddRuleTypeInput
from ..graphql.mutation.add_rule_type import addRuleType
from ..graphql.mutation.edit_rule_type import editRuleType
from ..graphql.mutation.remove_rule_type import removeRuleType
from ..graphql.query.rule_types import ruleTypes
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_rule_type(
    client: SymphonyClient, name: str
) -> ruleType:
   
    rule_type_input = AddRuleTypeInput(name=name)
    result = addRuleType.execute(client, input=rule_type_input)
    return ruleType(name=result.name, id=result.id)

def edit_rule_type(
    client: SymphonyClient,
    rule_type: ruleType,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editRuleType.execute(client, input=EditRuleTypeInput(id=rule_type.id, name=new_name))

def get_rule_types(client: SymphonyClient) -> Iterator[ruleType]:

    rule_types_ = ruleTypes.execute(client, first=PAGINATION_STEP)
    edges = rule_types_.edges if rule_types_ else []
    while rule_types_ is not None and rule_types_.pageInfo.hasNextPage:
        rule_types_ = ruleTypes.execute(
            client, after=rule_types_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if rule_types_ is not None:
            edges.extend(rule_types_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield ruleType(
                id=node.id,
                name=node.name,
            )


def remove_rule_type(client: SymphonyClient, id: str) -> None:
    removeRuleType.execute(client, id=id)


