from hydroplane.hydro import hydro
from dash import html, dcc, callback_context
from dash.dependencies import Input, Output, State, MATCH, ALL 


class HydroNavigation:
    def __init__(self, hydro_name, messages_enabled, alarms_enabled, profile_enabled): 
        self.hydro_name = hydro_name
        self.messages_enabled = messages_enabled
        self.alarms_enabled = alarms_enabled
        self.profile_enabled = profile_enabled


    # TOP NAVIGATION
    def hydro_top_navigation_profile(self):
        # Profile
        return html.Li(className="nav-item dropdown no-caret dropdown-user me-3 me-lg-4", children=[
            html.Button(id={
                                'type': 'top-nav-dropdown-btn',
                                'index': 3
                            }, className="btn btn-icon btn-transparent-dark dropdown-toggle avatar", n_clicks=0, children=[
                html.Img(className="avatar-img img-fluid", src=hydro.get_asset_url('img/illustrations/profiles/profile-1.png'))
            ]),
            html.Div(id={
                            'type': 'top-nav-dropdown-output',
                            'index': 3
                        }, style={"display": "none"}, className="dropdown-menu dropdown-menu-end border-0 shadow", children=[
                html.H6(className="dropdown-header d-flex align-items-center", children=[
                    html.Img(className="dropdown-user-img", src=hydro.get_asset_url('img/illustrations/profiles/profile-1.png')),
                    html.Div(className="dropdown-user-details", children=[
                        html.Div(className="dropdown-user-details-name", children=[
                            "John Doe"
                        ]),
                        html.Div(className="dropdown-user-details-email", children=[
                            "jdoe@email.com"
                        ])
                    ])
                ]),
                html.Div(className="dropdown-divider"),
                html.Button(id="account-settings", n_clicks=0, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-sliders-h")
                    ]),
                    "Settings"
                ]),
                html.Div(className="dropdown-divider"),
                html.Div(style={"display": "inline-flex"}, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-hat-wizard")
                    ]),
                    dcc.Link("Data Source Wizard", href="/wizard/data-source/add")
                ]), 
                html.Div(style={"display": "inline-flex"}, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-hat-wizard")
                    ]),
                    dcc.Link("Query Wizard", href="/wizard/query/add")
                ]),  
                html.Button(id="card-wizard", n_clicks=0, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-hat-wizard")
                    ]),
                    dcc.Link("Card Wizard", href="/wizard/card")
                ]),
                html.Button(id="page-wizard", n_clicks=0, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-hat-wizard")
                    ]),
                    dcc.Link("Page Wizard", href="/wizard/page")
                ]),
                html.Button(id="collection-wizard", n_clicks=0, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-hat-wizard")
                    ]),
                    dcc.Link("Collection Wizard", href="/wizard/collection")
                ]),
                html.Div(className="dropdown-divider"),
                html.Button(id="collection-system-health", n_clicks=0, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-heartbeat")
                    ]),
                    "System Health"
                ]),
                html.Button(id="collection-users", n_clicks=0, className="dropdown-item", children=[
                    html.Div(className="dropdown-item-icon", children=[
                        html.I(className="fas fa-heartbeat")
                    ]),
                    "User Management"
                ])
            ])
        ])


    def hydro_top_navigation_messages(self):
        # Message Center
        return html.Li(className="nav-item dropdown no-caret d-none d-sm-block me-3 dropdown-notifications", children=[
            html.Button(id={
                                'type': 'top-nav-dropdown-btn',
                                'index': 2
                            }, n_clicks=0, className="btn btn-icon btn-transparent-dark dropdown-toggle", children=[
                html.I(className="far fa-envelope")
            ]),
            html.Div(id={
                            'type': 'top-nav-dropdown-output',
                            'index': 2
                        }, style={"display": "none"}, className="dropdown-menu dropdown-menu-end border-0 shadow", children=[
                html.H6(className="dropdown-header dropdown-notifications-header", children=[
                    html.I(className="me-2 fas fa-bell"),
                    "Message Center"
                ]),
                html.A(className="dropdown-item dropdown-notifications-item", children=[
                    html.Img(className="dropdown-notifications-item-img", src="assets/img/illustrations/profiles/profile-2.png"),
                    html.Div(className="dropdown-notifications-item-content", children=[
                        html.Div(className="dropdown-notifications-item-content-text", children=[
                            "Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."
                        ]),
                        html.Div(className="dropdown-notifications-item-content-details", children=[
                            "Thomas Wilcox · 58m"
                        ])
                    ])
                ])
            ])
        ])

    def hydro_top_navigation_alerts(self):
        # Alerts
        return html.Li(className="nav-item dropdown no-caret d-none d-sm-block me-3 dropdown-notifications", children=[
            html.Button(id={
                                'type': 'top-nav-dropdown-btn',
                                'index': 1
                            }, n_clicks=0, className="btn btn-icon btn-transparent-dark dropdown-toggle", children=[
                html.I(className="far fa-bell")
            ]),
            html.Div(id={
                            'type': 'top-nav-dropdown-output',
                            'index': 1
                        }, style={"display": "none"}, className="dropdown-menu dropdown-menu-end border-0 shadow", children=[
                html.H6(className="dropdown-header dropdown-notifications-header", children=[
                    html.I(className="fas fa-bell"),
                    "Alerts Center"
                ]),
                html.A(className="dropdown-item dropdown-notifications-item", children=[
                    html.Div(className="dropdown-notifications-item-icon bg-warning", children=[
                        html.I(className="fas fa-bell")
                    ]),
                    html.Div(className="dropdown-notifications-item-content", children=[
                        html.Div(className="dropdown-notifications-item-content-details", children=[
                            "December 29, 2021"
                        ]),
                        html.Div(className="dropdown-notifications-item-content-text", children=[
                            "This is an alert message. It's nothing serious, but it requires your attention."
                        ])
                    ])
                ])
            ])
        ])

    def hydro_top_navigation(self, toggle=True):
        top_nav_list = []
        if self.alarms_enabled:
            top_nav_list.append(self.hydro_top_navigation_alerts())
        if self.messages_enabled:
            top_nav_list.append(self.hydro_top_navigation_messages())
        if self.profile_enabled: 
            top_nav_list.append(html.Div(className="topbar-divider d-none d-sm-block"))
            top_nav_list.append(self.hydro_top_navigation_profile())
        top_nav_toggle = html.Div(children=[
            html.Br(),
            html.Button(id="sidebar-toggle-btn", n_clicks=0, style={"display": "none"}, className="btn btn-icon btn-transparent-dark order-1 order-lg-0 me-2 ms-lg-2 me-lg-0", children=[ 
                        html.I(className="fas fa-bars") 
                    ])
        ])
        if toggle:
            top_nav_toggle = html.Button(id="sidebar-toggle-btn", n_clicks=0, className="btn btn-icon btn-transparent-dark order-1 order-lg-0 me-2 ms-lg-2 me-lg-0", children=[ 
                        html.I(className="fas fa-bars") 
                    ])
        return html.Nav(className="topnav navbar navbar-expand shadow justify-content-between justify-content-sm-start navbar-light bg-white", id="sidenavAccordion", children=[
                    
                    top_nav_toggle,
                    # Branding / Logo
                    html.A(className="navbar-brand pe-3 ps-4 ps-lg-2", children=[
                        self.hydro_name
                    ]),
                    # Top Right Features
                    html.Ul(id="nav-top-right-features", style={"display": "flex"}, className="navbar-nav align-items-center ms-auto", children=top_nav_list)
                ])




# TOP NAVIGATION CALLBACKS
@hydro.callback(
    Output({'type': 'top-nav-dropdown-output', 'index': MATCH}, 'style'),
    Output({'type': 'top-nav-dropdown-btn', 'index': MATCH}, 'children'), 
    Input({'type': 'top-nav-dropdown-btn', 'index': MATCH}, 'n_clicks'), 
    Input({'type': 'top-nav-dropdown-output', 'index': MATCH}, 'style'),
    Input({'type': 'top-nav-dropdown-btn', 'index': MATCH}, 'children'),
)
def display_dropdown_output(btn_clicks, style, children): 
    ctx = callback_context  
    button_clicked = ctx.triggered[0]["prop_id"].split(".")[0]  
    if 'top-nav-dropdown-btn' in button_clicked and style["display"] == "none":
        return {"display": "block"}, children
    return {"display": "none"}, children