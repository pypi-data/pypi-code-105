import os

from hydroplane import hydro, hydro_router, Hydroplane 
from hydroplane import Input, Output, State, MATCH, ALL

# INITIALIZE HYDROPLANE
hydroplane_postgres_env = {
    "host": os.environ['POSTGRES_HOST'],
    "port": os.environ['POSTGRES_PORT'],
    "database": os.environ['POSTGRES_DB'],
    "user": os.environ['POSTGRES_USER'],
    "password": os.environ['POSTGRES_PASSWORD']
}
hp = Hydroplane("hydroPLANE", 8053, hydroplane_postgres_env)


# HYDROPLANE GUI ROUTER
@hydro.callback(
    Output('page-content', 'children'),
    Input('url', 'pathname')
)
def display_page(pathname):  
    return hydro_router(hp, pathname)

