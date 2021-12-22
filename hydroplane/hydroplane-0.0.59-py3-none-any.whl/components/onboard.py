from hydroplane.hydro import hydro
from hydroplane.components.card import HydroCard
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL 

class HydroOnboarding:
    def __init__(self):
        self.cards = HydroCard()

    def hydro_onboarding_guide(self):
        card_body = html.Section(id="slideshow", children=[
            html.Div(id="slideshow-container", children=[
                html.Div(id="image"),
                dcc.Interval(id='interval', interval=3000)
            ])
        ])
        onboarding = self.cards.hydro_plain_card(1, "large", card_body)
        return onboarding



@hydro.callback(
    Output('image', 'children'),
    Input('interval', 'n_intervals')
)
def onboarding_carousel(n):
    if n == None or n % 3 == 1:
        img = html.Img(src="http://placeimg.com/625/225/any")
    elif n % 3 == 2:
        img = html.Img(src="http://placeimg.com/625/225/animals")
    elif n % 3 == 0:
        img = html.Img(src="http://placeimg.com/625/225/arch")
    else:
        img = "None"
    return img