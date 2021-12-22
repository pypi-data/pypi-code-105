#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import domain, tech, tech

from ..graphql.input.edit_tech_input import EditTechInput
from ..graphql.input.add_tech_input import AddTechInput
from ..graphql.mutation.add_tech import addTech
from ..graphql.mutation.edit_tech import editTech
from ..graphql.mutation.remove_tech import removeTech
from ..graphql.query.techs import techs
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_tech(
    client: SymphonyClient, name: str, domain: str
) -> tech:
   
    tech_input = AddTechInput(name=name, domainFk=domain)
    result = addTech.execute(client, input=tech_input)
    return tech(name=result.name, id=result.id, domainFK=result.domainFk)


def edit_tech(
    client: SymphonyClient,
    tech: tech,
    new_name: Optional[str] = None,
    domain: domain = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editTech.execute(client, input=EditTechInput(id=tech.id, name=new_name, domainFk=domain))

def get_tech(client: SymphonyClient) -> Iterator[tech]:

    tech_ = techs.execute(client, first=PAGINATION_STEP)
    edges = tech_.edges if tech_ else []
    while tech_ is not None and tech_.pageInfo.hasNextPage:
        tech_ = techs.execute(
            client, after=tech_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if tech_ is not None:
            edges.extend(tech_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield tech(
                id=node.id,
                name=node.name,
                domainFK=node.id

            )


def remove_tech(client: SymphonyClient, id: str) -> None:
    removeTech.execute(client, id=id)


