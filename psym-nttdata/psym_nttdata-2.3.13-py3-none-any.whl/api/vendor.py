#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import Vendor

from ..graphql.input.edit_vendor_input import EditVendorInput
from ..graphql.input.add_vendor_input import AddVendorInput
from ..graphql.mutation.add_vendor import addVendor
from ..graphql.mutation.edit_vendor import editVendor
from ..graphql.mutation.remove_vendor import removeVendor
from ..graphql.query.vendors import vendors
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_vendor(
    client: SymphonyClient, name: str
) -> Vendor:
   
    vendor_input = AddVendorInput(name=name)
    result = addVendor.execute(client, input=vendor_input)
    return Vendor(name=result.name, id=result.id)

def edit_vendor(
    client: SymphonyClient,
    vendor: Vendor,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editVendor.execute(client, input=EditVendorInput(id=vendor.id, name=new_name))


def get_vendors(client: SymphonyClient) -> Iterator[Vendor]:

    vendors_ = vendors.execute(client, first=PAGINATION_STEP)
    edges = vendors_.edges if vendors_ else []
    while vendors_ is not None and vendors_.pageInfo.hasNextPage:
        vendors_ = vendors.execute(
            client, after=vendors_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if vendors_ is not None:
            edges.extend(vendors_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield Vendor(
                id=node.id,
                name=node.name,
            )


def remove_vendor(client: SymphonyClient, id: str) -> None:
    removeVendor.execute(client, id=id)