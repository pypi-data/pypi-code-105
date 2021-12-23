#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import Kpi, domain, KpiCategory

from ..graphql.input.edit_kpi_input import EditKpiInput
from ..graphql.input.add_kpi_input import AddKpiInput
from ..graphql.mutation.add_kpi import addKpi
from ..graphql.mutation.edit_kpi import editKpi
from ..graphql.mutation.remove_kpi import removeKpi
from ..graphql.query.kpis import kpis
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_kpi(
    client: SymphonyClient, name: str, description: str, status: bool, domain: str, kpiCategory: str
) -> Kpi:
   
    domain_input = AddKpiInput(name=name, description=description,
    status=status, 
    domainFk=domain,
    kpiCategoryFK=kpiCategory)

    result = addKpi.execute(client, input=domain_input)

    return Kpi(name=result.name, id=result.id, 
    description=result.description, 
    status=result.status, 
    domain=result.domainFk, 
    kpiCategory=result.kpiCategoryFK)

def edit_kpi(
    client: SymphonyClient,
    KPI: Kpi,
    new_name: Optional[str] = None,
    description: str = None,
    status: bool = None,
    domain: domain = None,
    kpiCategory: KpiCategory = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editKpi.execute(client, input=EditKpiInput(id=KPI.id, 
        name=new_name,
        description=description,
        status= status,
        domainFk=domain,
        kpiCategoryFK=kpiCategory
        ))


def get_kpis(client: SymphonyClient) -> Iterator[Kpi]:

    kpis_ = kpis.execute(client, first=PAGINATION_STEP)
    edges = kpis_.edges if kpis_ else []
    while kpis_ is not None and kpis_.pageInfo.hasNextPage:
        kpis_ = kpis.execute(
            client, after=kpis_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if kpis_ is not None:
            edges.extend(kpis_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield Kpi(
                id=node.id,
                name=node.name,
                description=node.description,
                status=node.status,
                domain=node.id,
                kpiCategory=node.id


            )


def remove_kpi(client: SymphonyClient, id: str) -> None:
    removeKpi.execute(client, id=id)







