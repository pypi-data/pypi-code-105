from dataclasses import dataclass

from dash import html

from .base_component import BaseComponent


@dataclass
class Kpi(BaseComponent):
    id: str
    size: str
    kpi_value: int
    kpi_text: str
    kpi_unit: str = None
    double_kpi: bool = False
    secondary_id: str = None
    secondary_kpi_value: int = None
    secondary_kpi_text: str = None
    secondary_kpi_unit: str = None

    @property
    def layout(self):
        if self.double_kpi:
            return self._get_double_kpi_layout()
        return self._get_single_kpi_layout()

    def _get_single_kpi_layout(self):

        return html.Div(
            className=self.size,
            children=[
                html.Div(
                    className="content-container kpi-container",
                    children=[
                        html.Div(
                            className="row text-center",
                            children=[
                                html.Div(
                                    className="col kpi-body",
                                    children=[
                                        html.Span(
                                            id=self.id, children=[self.kpi_value]
                                        ),
                                        html.Span(self.kpi_unit),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="row container-title",
                            children=[
                                html.Div(
                                    className="col kpi-title text-center",
                                    children=[self.kpi_text],
                                )
                            ],
                        ),
                    ],
                )
            ],
        )

    def _get_double_kpi_layout(self):
        return html.Div(
            className=self.size,
            children=[
                html.Div(
                    className="content-container kpi-container",
                    children=[
                        html.Div(
                            className="row",
                            children=[
                                html.Div(
                                    className="col main-kpi text-end kpi-body",
                                    children=[
                                        html.Span(
                                            id=self.id, children=[self.kpi_value]
                                        ),
                                        html.Span(self.kpi_unit),
                                    ],
                                ),
                                html.Div(
                                    className="col secondary-kpi",
                                    children=[
                                        html.Div(
                                            className="row",
                                            children=[
                                                html.Div(
                                                    className="col secondary-kpi-body",
                                                    children=[
                                                        html.Span(
                                                            id=self.secondary_id,
                                                            children=[
                                                                self.secondary_kpi_value
                                                            ],
                                                        ),
                                                        html.Span(
                                                            self.secondary_kpi_unit
                                                        ),
                                                    ],
                                                ),
                                                html.Div(
                                                    className="row secondary-kpi-title",
                                                    children=[self.secondary_kpi_text],
                                                ),
                                            ],
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            className="row container-title",
                            children=[
                                html.Div(
                                    className="col kpi-title text-center",
                                    children=[self.kpi_text],
                                ),
                            ],
                        ),
                    ],
                )
            ],
        )
