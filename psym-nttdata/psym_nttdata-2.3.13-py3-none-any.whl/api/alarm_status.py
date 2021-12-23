#!/usr/bin/env python3
# Copyright (c) 2004-present Facebook All rights reserved.
# Use of this source code is governed by a BSD-style
# license that can be found in the LICENSE file.


from psym.client import SymphonyClient
from psym.common.data_class import alarmStatus

from ..graphql.input.edit_alarm_status_input import EditAlarmStatusInput
from ..graphql.input.add_alarm_status_input import AddAlarmStatusInput
from ..graphql.mutation.add_alarm_status import addAlarmStatus
from ..graphql.mutation.edit_alarm_status import editAlarmStatus
from ..graphql.mutation.remove_alarm_status import removeAlarmStatus
from ..graphql.query.alarm_statuses import alarmStatuses
from psym.common.constant import PAGINATION_STEP
from typing import Any, Dict, Iterator, List, Optional




def add_alarm_status(
    client: SymphonyClient, name: str
) -> alarmStatus:
   
    alarm_status_input = AddAlarmStatusInput(name=name)
    result = addAlarmStatus.execute(client, input=alarm_status_input)
    return alarmStatus(name=result.name, id=result.id)

def edit_alarm_status(
    client: SymphonyClient,
    alarm_status: alarmStatus,
    new_name: Optional[str] = None,
) -> None:
    params: Dict[str, Any] = {}
    if new_name is not None:
        params.update({"_name_": new_name})
    if new_name is not None:
        editAlarmStatus.execute(client, input=EditAlarmStatusInput(id=alarm_status.id, name=new_name))


def get_alarm_statuses(client: SymphonyClient) -> Iterator[alarmStatus]:

    alarm_statusess_ = alarmStatuses.execute(client, first=PAGINATION_STEP)
    edges = alarm_statusess_.edges if alarm_statusess_ else []
    while alarm_statusess_ is not None and alarm_statusess_.pageInfo.hasNextPage:
        alarm_statusess_ = alarmStatuses.execute(
            client, after=alarm_statusess_.pageInfo.endCursor, first=PAGINATION_STEP
        )
        if alarm_statusess_ is not None:
            edges.extend(alarm_statusess_.edges)

    for edge in edges:
        node = edge.node
        if node is not None:
            yield alarmStatus(
                id=node.id,
                name=node.name,
            )


def remove_alarm_status(client: SymphonyClient, id: str) -> None:
    removeAlarmStatus.execute(client, id=id)

    