from hydroplane.hydro import hydro
from hydroplane.components.card import HydroCard
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL 

class HydroSimple:
    def __init__(self):
        self.cards = HydroCard()

    def hydro_simple(self):
        card_body = html.Section(id="simple", children=[
            "SIMPLE"
        ])
        simple = self.cards.hydro_plain_card(1, "large", card_body)
        return simple

 