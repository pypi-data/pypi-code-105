from hydroplane.hydro import hydro
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, MATCH, ALL 

class HydroCard:
    def __init__(self) -> None:
        pass

    def hydro_plain_card(self, card_idx, card_size, body): 
        className = "col-lg-12 mb-4"
        if card_size == "large":
            className = "col-lg-12 mb-4"
        elif card_size == "medium":
            className = "col-lg-8 mb-4"
        elif card_size == "small":
            className = "col-lg-6 mb-4" 
        elif card_size == "preview-1":
            className = "col-lg-8 mb-4" 
        elif card_size == "preview-2":
            className = "col-lg-4 mb-4" 
        else:
            className = "col-lg-12 mb-4"
        return html.Div(className=className, children=[ 
                html.Div(id="card-id", style={"display":"none"}, children=card_idx),
                html.Div(className="card", children=[ 
                    html.Div(id={'type':'card-plain-body','index':card_idx}, className="card-body", style={"display":"block"}, children=body)
                ])
            ])
    def hydro_simple_card(card_idx, card_size, header, body): 
        className = "col-lg-12 mb-4"
        if card_size == "large":
            className = "col-lg-12 mb-4"
        elif card_size == "medium":
            className = "col-lg-8 mb-4"
        elif card_size == "small":
            className = "col-lg-6 mb-4" 
        return html.Div(className=className, children=[ 
                html.Div(id="card-id", style={"display":"none"}, children=card_idx),
                html.Div(className="card", children=[
                    html.Div(className="card-header", children=[ 
                        header 
                    ]),
                    
                    html.Div(id={'type':'card-simple','index':card_idx}, className="card-body", style={"display":"block"}, children=body) 
                ])
            ])