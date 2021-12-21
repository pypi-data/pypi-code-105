from dataclasses import dataclass
from typing import Dict, List, Union

import dash_bootstrap_components as dbc
from dash import dcc, html

from .base_component import BaseComponent


@dataclass
class CustomDropdown(BaseComponent):
    id: str
    size: str
    label: str
    options: List[Union[Dict[str, str], Dict[str, int], Dict[int, int], Dict[int, str]]]
    default_value: Union[int, str, List[int], List[str]]
    multi: bool = False
    searchable: bool = False
    clearable: bool = False

    @property
    def layout(self):
        return html.Div(
            className=f"custom-dropdown-style {self.size}",
            children=[
                dbc.Label(self.label, html_for=self.id),
                dcc.Dropdown(
                    id=self.id,
                    options=self.options,
                    multi=self.multi,
                    value=self.default_value,
                    searchable=self.searchable,
                    clearable=self.clearable,
                ),
            ],
        )
