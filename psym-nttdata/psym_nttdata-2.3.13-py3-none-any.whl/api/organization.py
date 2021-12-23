#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import organization
from psym.common.data_enum import Entity
from psym.exceptions import EntityNotFoundError

from ..graphql.input.edit_organization_input import EditOrganizationInput
from ..graphql.input.add_organization_input import AddOrganizationInput
from ..graphql.mutation.add_organization import addOrganization
from ..graphql.mutation.edit_organization import editOrganization
from ..graphql.mutation.remove_organization import removeOrganization
from ..graphql.query.organizations import organizations
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_organization(
    client: SymphonyClient, name: str, description: str
) -> organization:
   
    organization_input = AddOrganizationInput(name=name, description=description)
    result = addOrganization.execute(client, input=organization_input)
    return organization(name=result.name, id=result.id, description=result.description)

def edit_organization(
    client: SymphonyClient,
    organization: organization,
    new_name: Optional[str] = None,
    new_description: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_description is not None:
        params.update({"_name_": new_description})
    if new_name is not None:
        editOrganization.execute(client, input=EditOrganizationInput(id=organization.id, name=new_name, description=new_description))

def get_organizations(client: SymphonyClient) -> Iterator[organization]:

    organizations_ = organizations.execute(client, first=PAGINATION_STEP)
    edges = organizations_.edges if organizations_ else []
    while organizations_ is not None and organizations_.pageInfo.hasNextPage:
        organizations_ = organizations.execute(
            client, after=organizations_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if organizations_ is not None:
            edges.extend(organizations_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield organization(
                id=node.id,
                name=node.name,
                description=node.description
            )



def remove_organization(client: SymphonyClient, id: str) -> None:
    removeOrganization.execute(client, id=id)


def get_organization_by_name(client: SymphonyClient, name: str) -> organization:
    organization_name = get_organizations(client=client)
    for organization_names in organization_name:
        if organization_names.name == name:
            return organization_names
    raise EntityNotFoundError(entity=Entity.organization, entity_name=name)