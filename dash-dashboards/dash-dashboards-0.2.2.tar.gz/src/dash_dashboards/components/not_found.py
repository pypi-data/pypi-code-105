from dataclasses import dataclass

from dash import dcc, html

from .base_component import BaseComponent


@dataclass
class NotFound(BaseComponent):
    id: str
    size: str = "col-6"

    @property
    def layout(self):
        return html.Div(
            className="page-container",
            children=[
                html.Div(
                    className="row g-4 page-content d-flex justify-content-center",
                    children=[
                        html.Div(
                            id=self.id,
                            className=f"""content-container not-found-content
                            align-center {self.size}""",
                            children=[
                                html.Img(
                                    className="not-found-img",
                                    src="../assets/img/wrong-way.svg",
                                    height=100,
                                ),
                                html.Div(
                                    className="not-found-text",
                                    children=[
                                        "Oops! You've followed the wrong route! :("
                                    ],
                                ),
                                html.Div(
                                    children=[
                                        dcc.Link(
                                            className="""list-group-item border-0
                                            d-inline-block text-truncate nav-item
                                            not-found-link auto-width""",
                                            href="/",
                                            children=[
                                                html.I(className="bi bi-arrow-left"),
                                                html.Span(
                                                    "Get back to the right track."
                                                ),
                                            ],
                                        ),
                                    ]
                                ),
                            ],
                        ),
                    ],
                ),
            ],
        )
