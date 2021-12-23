#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import comparator

from ..graphql.input.edit_comparator_input import EditComparatorInput
from ..graphql.input.add_comparator_input import AddComparatorInput
from ..graphql.mutation.add_comparator import addComparator
from ..graphql.mutation.edit_comparator import editComparator
from ..graphql.mutation.remove_comparator import removeComparator
from ..graphql.query.comparators import comparators
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_comparator(
    client: SymphonyClient, name: str
) -> comparator:
   
    comparator_input = AddComparatorInput(name=name)
    result = addComparator.execute(client, input=comparator_input)
    return comparator(name=result.name, id=result.id)

def edit_comparator(
    client: SymphonyClient,
    comparator: comparator,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editComparator.execute(client, input=EditComparatorInput(id=comparator.id, name=new_name))

def get_comparators(client: SymphonyClient) -> Iterator[comparator]:

    comparators_ = comparators.execute(client, first=PAGINATION_STEP)
    edges = comparators_.edges if comparators_ else []
    while comparators_ is not None and comparators_.pageInfo.hasNextPage:
        comparators_ = comparators.execute(
            client, after=comparators_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if comparators_ is not None:
            edges.extend(comparators_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield comparator(
                id=node.id,
                name=node.name,
            )


def remove_comparator(client: SymphonyClient, id: str) -> None:
    removeComparator.execute(client, id=id)