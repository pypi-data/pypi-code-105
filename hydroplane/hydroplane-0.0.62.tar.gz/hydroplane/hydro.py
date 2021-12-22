import dash, os

external_stylesheets = [
    {
        'href': 'https://use.fontawesome.com/releases/v5.8.1/css/all.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-50oBUHEmvpQ+1lW4y57PTFmhCaXp0ML5d60M1M7uH2+nqUivzIebhndOJK28anvf',
        'crossorigin': 'anonymous'
    }
]
 
assets_path = os.path.dirname(os.path.abspath(__file__)) + '/assets'  
hydro = dash.Dash(__name__, external_stylesheets=external_stylesheets) 
hydro.title = "HYDROPLANE"
hydro.config.suppress_callback_exceptions=True



# HYDRO ROUTING 
def hydro_url_route_parser(url): 
    print(url)
    if url == None or url == "/":
        return None
    if url[0] == "/":
        url = url[1:]
    if url[-1] == "/":
        url = url[:-1] 
    return url.split("/")

def hydro_router(hp, url):
    # PARSE CURRENT PAGE URL
    parsed_url = hydro_url_route_parser(url) 
    # HYDRO RESERVED ROUTES - HOME PAGE
    if url == "/" or url == "":
        return "HYDRO HOME PAGE"

    if parsed_url == ["blok"]:
        return "MANUFACTURING"

    # HYDRO RESERVED ROUTES - QUICK START
    if parsed_url == ["quick-start"]:
        return "QUICK START PAGE"

    # HYDRO RESERVED ROUTES - DATA SOURCE WIZARD
    elif parsed_url == ["wizard", "data-source"]:
        return "WIZARD PAGE"
    elif parsed_url == ["wizard", "data-source", "add"]:
        return "ADD PAGE"
    elif parsed_url[:-1] == ["wizard", "data-source", "edit"]:
        edit_id = parsed_url[-1]
        return "EDIT PAGE" 

    # HYDRO RESERVED ROUTES - QUERY WIZARD
    elif parsed_url == ["wizard", "query"]:
        return "WIZARD PAGE"
    elif parsed_url == ["wizard", "query", "add"]:
        return "ADD PAGE"
    elif parsed_url[:-1] == ["wizard", "query", "edit"]:
        edit_id = parsed_url[-1]
        return "EDIT PAGE"

    # HYDRO RESERVED ROUTES - CARD WIZARD
    elif parsed_url == ["wizard", "card"]:
        return "WIZARD PAGE"
    elif parsed_url == ["wizard", "card", "add"]:
        return "ADD PAGE"
    elif parsed_url[:-1] == ["wizard", "card", "edit"]:
        edit_id = parsed_url[-1]
        return "EDIT PAGE"

    # HYDRO RESERVED ROUTES - PAGE WIZARD
    elif parsed_url == ["wizard", "page"]:
        return "WIZARD PAGE"
    elif parsed_url == ["wizard", "page", "add"]:
        return "ADD PAGE"
    elif parsed_url[:-1] == ["wizard", "page", "edit"]:
        edit_id = parsed_url[-1]
        return "EDIT PAGE"

    # HYDRO RESERVED ROUTES - COLLECTION WIZARD
    elif parsed_url == ["wizard", "collection"]:
        return "WIZARD PAGE"
    elif parsed_url == ["wizard", "collection", "add"]:
        return "ADD PAGE"
    elif parsed_url[:-1] == ["wizard", "collection", "edit"]:
        edit_id = parsed_url[-1]
        return "EDIT PAGE"
    else:
        return "TEST"
    

    # HYDRO CUSTOM PAGE ROUTES
    # routes = hp.LIST_AVAILABLE PAGES / ROUTES
    # for route in routes:
    #     parsed_route = hydro_url_route_parser(route)
    #     if parsed_route == parsed_url:
    #         return "QUERY PAGE URL AND GET PAGE ID, AND BUILD PAGE"

    