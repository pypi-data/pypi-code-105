from hydroplane.hydro import hydro, hydro_router
from hydroplane.components.navigation import HydroNavigation
from hydroplane.components.card import HydroCard
from hydroplane.components.onboard import HydroOnboarding
from hydroplane.components.simple import HydroSimple
from hydroplane.data_sources.postgres import HydroPostgres, DATA_SOURCES_TABLE, QUERIES_TABLE, CARDS_TABLE, PAGES_TABLE, COLLECTIONS_TABLE, LOGS_TABLE, SETTINGS_TABLE
from hydroplane.data_sources.druid import HydroDruid

import dash, psycopg2, sys, json, hashlib, uuid, base64, os
from dash import html, dcc
from dash.dependencies import Input, Output, State, MATCH, ALL 
from urllib.parse import urlparse


random_value = uuid.uuid4().hex

hydroplane_postgres_environment = {
    "host": os.getenv('POSTGRES_HOST', 'pg_host'),
    "port": os.getenv('POSTGRES_PORT', 'pg_port'),
    "database": os.getenv('POSTGRES_DB', 'pg_db'),
    "user": os.getenv('POSTGRES_USER', 'pg_user'),
    "password": os.getenv('POSTGRES_PASSWORD', 'pg_pw')
}

class Hydroplane:
    def __init__(self, hydro_name, hydro_port, hydro_debug=True, hydro_threaded=True, hydro_archive=None, hydro_messages=None, hydro_alerts=None):
        # HYDRO INPUTTS
        self.hydro_name = hydro_name
        self.hydro_port = hydro_port 
        self.hydro_debug = hydro_debug
        self.hydro_threaded = hydro_threaded
        self.hydro_archive = hydro_archive
        self.hydro_messages = hydro_messages
        self.hydro_alerts = hydro_alerts

        # HYDRO COMPONENTS
        self.hydro_components_navigation = HydroNavigation(self.hydro_name, self.hydro_messages, self.hydro_alerts)
        self.hydro_components_card = HydroCard()
        self.hydro_components_chart = None
        self.hydro_components_table = None
        self.hydro_components_onboarding = HydroOnboarding()
        self. hydro_components_simple = HydroSimple()
        # HYDRO WIZARDS
        self.hydro_wizard_data_source = None
        self.hydro_wizard_query = None
        self.hydro_wizard_card = None
        self.hydro_wizard_page = None
        self.hydro_wizard_collection = None
        # HYDRO POSTGRES
        self.hydro_data_source_postgres = HydroPostgres(hydroplane_postgres_environment["host"], hydroplane_postgres_environment["port"], hydroplane_postgres_environment["database"], hydroplane_postgres_environment["user"], hydroplane_postgres_environment["password"])
 
    def hydro_wireframe(self, hydro_top_navigation): 
        wireframe = html.Div(id="wrapper", children=[
                        html.Div(id="wrapper-children", className="nav-fixed sidenav-toggled", children = [ 
                            # URL
                            dcc.Location(id='url', refresh=False), 
                            # TOP NAVIGATION  
                            hydro_top_navigation,

                            # MAIN CONTENT (PAGE + SIDE NAV)
                            html.Div(id="layoutSidenav", children=[
                                # SIDE NAVIGATION
                                html.Div(id="hydro-sidenav-navigation"),
                                # PAGE CONTENT 
                                html.Div(id="layoutSidenav_content", children=[
                                    html.Div(id="hydro-page-content", className="container-xl px-4 mt-5")
                                ])
                            ])
                        ]) 
                    ])
        return wireframe
        
    def simple_hydro(self):
        hydro_top_navigation = self.hydro_components_navigation.hydro_top_navigation(toggle=False)
        hydro.layout = self.hydro_wireframe(self, hydro_top_navigation)
        hydro.run_server(host="0.0.0.0", port="8053", debug=self.hydro_debug, threaded=self.hydro_threaded)

    def start_up(self):
        # check if postgres is available, if not then wait and retry 
        # CREATE POSTGRES CONNECTION
        try:
            conn = self.hydro_data_source_postgres.postgres_create_connection() 
        except psycopg2.OperationalError:
            # print("Oops!", sys.exc_info()[0], "occurred.")
            print("ERROR: POSTGRES CONNECTION FAILURE - psycopg2.OperationalError")
        else:
            # CREATE IF DOES NOT EXIST POSTGRES TABLES
            self.hydro_data_source_postgres.postgres_create_table(conn, "DATA SOURCES", DATA_SOURCES_TABLE)
            self.hydro_data_source_postgres.postgres_create_table(conn, "QUERIES", QUERIES_TABLE)
            self.hydro_data_source_postgres.postgres_create_table(conn, "CARDS", CARDS_TABLE)
            self.hydro_data_source_postgres.postgres_create_table(conn, "PAGES", PAGES_TABLE)
            self.hydro_data_source_postgres.postgres_create_table(conn, "COLLECTIONS", COLLECTIONS_TABLE)
            self.hydro_data_source_postgres.postgres_create_table(conn, "LOGS", LOGS_TABLE)
            self.hydro_data_source_postgres.postgres_create_table(conn, "SETTINGS", SETTINGS_TABLE)  

            # LOOK FOR EXISTING COLLECTIONS, PAGES, CARDS, QUERIES, DATA SOURCES

            # IF NONE ONBOARD USER
            wireframe_body_onboarding = self.hydro_components_onboarding.hydro_onboarding_guide()

            # CLOSE POSTGRES CONNECTION
            self.hydro_data_source_postgres.postgres_close_connection(conn) 


            # SET HYDRO LAYOUT
            hydro_top_navigation = self.hydro_components_navigation.hydro_top_navigation()
            hydro_body = wireframe_body_onboarding
            hydro.layout = self.hydro_wireframe(hydro_top_navigation)
            # RUN WEBSERVER
            hydro.run_server(host="0.0.0.0", port="8053", debug=self.hydro_debug, threaded=self.hydro_threaded)
            # hydro.run_server(host="0.0.0.0", port=str(self.hydro_port), debug=self.hydro_debug, threaded=self.hydro_threaded)
        





# HYDROPLANE GUI ROUTER
@hydro.callback(
    Output('hydro-page-content', 'children'),
    Output('hydro-sidenav-navigation', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):   
    
    # LOOK FOR EXISTING COLLECTIONS, PAGES, CARDS, QUERIES, DATA SOURCES 
    # IF NONE ONBOARD USER
    wireframe_body_onboarding = HydroOnboarding().hydro_onboarding_guide()
    if pathname == "/onboarding": 
        print(wireframe_body_onboarding) 
        return wireframe_body_onboarding, ""
    x = hydro_router(1, pathname)
    print(x)
    return x, ""


@hydro.callback(
    Output('wrapper-children', 'className'),
    Output('sidebar-toggle-btn', 'n_clicks'),
    Input('sidebar-toggle-btn', 'n_clicks'), 
    Input('wrapper-children', 'className')
)
def sidebar_toggle(btn, current_cls):
    if btn > 0 and current_cls == "nav-fixed sidenav-toggled":
        return "nav-fixed", 0 
    else:
        return "nav-fixed sidenav-toggled", 0