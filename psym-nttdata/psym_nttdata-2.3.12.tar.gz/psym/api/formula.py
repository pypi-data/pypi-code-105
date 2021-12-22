#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import  NetworkType, formula, Kpi, tech

from ..graphql.input.edit_formula_input import EditFormulaInput
from ..graphql.input.add_formula_input import AddFormulaInput
from ..graphql.mutation.add_formula import addFormula
from ..graphql.mutation.edit_formula import editFormula
from ..graphql.mutation.remove_formula import removeFormula
from ..graphql.query.formulas import formulas
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_formula(
    client: SymphonyClient, textFormula: str, status: bool,  tech: str, networkType: str,  kpi: str
) -> formula:
   
    formula_input = AddFormulaInput(
    textFormula=textFormula, 
    status=status, 
    techFk= tech,
    networkTypeFk= networkType,
    kpiFk= kpi
   
   )
    result = addFormula.execute(client, input=formula_input)
    return formula(textFormula=result.textFormula, 
    id=result.id,  
    status=result.status, 
    techFk=result.techFk,
    networkTypeFk=result.networkTypeFk,
    kpiFk=result.kpiFk
)

def edit_formula(
    client: SymphonyClient,
    formula: formula,
    new_name: Optional[str] = None,
    status: bool = None,
    tech: tech = None,
    networkType: NetworkType = None,
    kpi: Kpi = None
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editFormula.execute(client, input=EditFormulaInput(
        id=formula.id, 
        textFormula=new_name,
        status= status,
        networkTypeFk=networkType,
        kpiFk=kpi,
        techFk=tech
        ))


def get_formulas(client: SymphonyClient) -> Iterator[Kpi]:

    formulas_ = formulas.execute(client, first=PAGINATION_STEP)
    edges = formulas_.edges if formulas_ else []
    while formulas_ is not None and formulas_.pageInfo.hasNextPage:
        formulas_ = formulas.execute(
            client, after=formulas_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if formulas_ is not None:
            edges.extend(formulas_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield formula(
                id=node.id,
                textFormula=node.textFormula,
                status=node.status,
                networkTypeFk=node.networkTypeFk,
                kpiFk=node.kpiFk,
                techFk=node.techFk

            )


def remove_formula(client: SymphonyClient, id: str) -> None:
    removeFormula.execute(client, id=id)








