from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Callable, List, Union

import dash_bootstrap_components as dbc
from dash import dcc, html
from dash.development.base_component import Component

ItemLayoutClass = Union[dcc.Link, dbc.Accordion]


class BaseMenuItem(ABC):
    @abstractmethod
    def get_menu_item_layout(self) -> ItemLayoutClass:
        ...  # pragma: no cover

    @property
    @abstractmethod
    def pages(self) -> List["MenuItem"]:
        ...  # pragma: no cover


@dataclass
class MenuItem(BaseMenuItem):
    name: str
    layout: Union[Component, Callable[[None], Component]]
    route: str
    icon: str = None

    def get_menu_item_layout(self) -> ItemLayoutClass:
        return dcc.Link(
            href=self.route,
            className="list-group-item border-0 d-inline-block text-truncate nav-item",
            children=[html.I(className=self.icon), html.Span(self.name)],
        )

    def get_layout(self) -> Component:
        return self.layout() if callable(self.layout) else self.layout

    @property
    def pages(self) -> List["MenuItem"]:
        return [self]


@dataclass
class MenuGroup(BaseMenuItem):
    name: str
    items: List[MenuItem]

    def get_menu_item_layout(self) -> ItemLayoutClass:
        return dbc.Accordion(
            start_collapsed=True,
            className="nav-accordion",
            flush=True,
            children=[
                dbc.AccordionItem(
                    title=self.name,
                    children=[item.get_menu_item_layout() for item in self.items],
                )
            ],
        )

    @property
    def pages(self) -> List["MenuItem"]:
        return self.items


def get_main_layout(navigation_layout: List[Component]) -> Component:
    return html.Div(
        children=[
            dcc.Location(id="url", refresh=False),
            html.Div(
                className="row flex-nowrap px-2",
                children=[
                    html.Div(
                        className="col-auto px-0",
                        children=[
                            html.Div(
                                id="sidebar",
                                children=[
                                    html.Div(
                                        id="sidebar-nav",
                                        className="""list-group border-0 rounded-0
                                            text-sm-start min-vh-100 nav-group""",
                                        # NAVIGATION CONTENT
                                        children=navigation_layout,
                                    )
                                ],
                            )
                        ],
                    ),
                    html.Main(
                        className="col",
                        children=[
                            html.Div(
                                id="main-container",
                                className="main-container overflow-hidden",
                                # BODY CONTENT
                                children=[html.Div(id="content")],
                            )
                        ],
                    ),
                ],
            ),
        ]
    )


Menu = List[BaseMenuItem]
