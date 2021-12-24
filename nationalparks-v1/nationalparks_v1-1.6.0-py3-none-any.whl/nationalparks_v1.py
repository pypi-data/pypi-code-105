# -*- coding: utf-8 -*-
"""
Created on Tue Dec 14 18:24:06 2021
@author: Bengusu Ozcan

"""

import requests
import os
import pandas as pd
import geopy.distance
import re
import csv
from importlib import resources
pd.set_option("display.max_rows", None, "display.max_columns", None)

def national_parks():
    print("""
    National parks are areas that are under the protection of states or organizations with their
exceptional nature or historical significance. The United States has many national parks, 
conserved carefully and almost always open to visitors. 
    This package helps you to explore national parks and plan your next national park trip.
    Please note that for some of the functions below, you will need a US National Parks API key.
A free API key can be acquired from: https://www.nps.gov/subjects/developer/get-started.htm
    
    Here are the things you can do with this package:
    - dist_calc(): find the closest national park based on your coordinates
    - how_far(): calculate the approximate distance of a specific park based on your coordinates.
    - park_desc(): read a short description of a certain national park.
    - activity_search(): find parks based on an activity you would like to do.
    Call activity_list() for a full list of activities you can choose from.
    - park_popularity(): find the most or least visited parks based on the latest info online.
    - alerts(): learn the latest alerts, closures or warnings for the park you are interested in.
    - pet_friendly(): quickly check if there are pet restrictions in a certain park. If you see 
    that there are restrictions, call pet_restrictions() for details of pet restrictions.
""")

def name_check(name):
    """
    NAME: name_check
    ----------
    DESCRIPTION: Replaces and corrects users' park name query with a unique identifier in order
    to save them searching for the exact name of the national park. Works for the top 20 national
    parks in terms of number of visits.
    ----------
    PARAMETERS:
    name: str, the name of the national park in the user query
    -------
    RETURNS: str, replaces user's searched national park name with the expected full name if 
    there is a match, returns user's search term if not
    """
    if re.search('smoky', name.lower()): 
        name='Great Smoky Mountains National Park'
    elif re.search('yellow', name.lower()): 
        name='Yellowstone National Park'
    elif re.search('zion', name.lower()): 
        name='Zion National Park'
    elif re.search('rocky', name.lower()): 
        name='Rocky Mountain National Park'
    elif re.search('teton', name.lower()): 
        name='Zion National Park'
    elif re.search('parshant', name.lower()): 
        name='Grand Canyon-Parashant National Monument'
    elif (re.search('grand', name.lower()) and re.search('canyon',name.lower())): 
        name='Grand Canyon National Park'
    elif re.search('cuyahoga', name.lower()): 
        name='Cuyahoga Valley National Park'
    elif re.search('acadian', name.lower()): 
        name='Maine Acadian Culture'
    elif re.search('acadia', name.lower()): 
        name='Acadia National Park'
    elif re.search('olympic', name.lower()): 
        name='Olympic National Park'
    elif re.search('joshua', name.lower()): 
        name='Joshua Tree National Park'
    elif re.search('indiana', name.lower()): 
        name='Indiana Dunes National Park'
    elif re.search('yosemite', name.lower()): 
        name='Yosemite National Park'
    elif re.search('shenandoah', name.lower()): 
        name='Shenandoah National Park'
    elif re.search('bryce', name.lower()): 
        name='Bryce Canyon National Park'
    elif re.search('hot', name.lower()) and re.search('spring',name.lower()): 
        name='Hot Springs National Park'
    elif re.search('arches', name.lower()): 
        name='Arches National Park'
    elif re.search('rainier', name.lower()): 
        name='Mount Rainier National Park'
    elif re.search('capitol', name.lower()) and re.search('reef',name.lower()): 
        name='Maine Acadian Culture'
    else:
        name=name
        #if no keyword is matched with a popular park name, then user's query is returned
    return name

def parks_list():
    """
    NAME:parks_list
    ----------
    DESCRIPTION: Matches the park name the user queried for the park code required for the API
    search. Uses the 'parks_list.csv' file available in the data folder in the package. 
    ----------
    PARAMETERS: None.
    ----------
    RETURNS: A pandas dataframe about the requested info type about national parks in a state
    """
    data_df = None
    my_package_csv_files = []
    
    with resources.open_text('nationalparks_v1.data', 'parks_list.csv') as fhandle: # , encoding = 'utf-8'

        line = fhandle.readline()
        while line:
            line_contents = [ '{}'.format(x) for x in list(csv.reader([line], delimiter=',', quotechar='"'))[0] ]
            if not line_contents is None and len(line_contents) > 0:
                my_package_csv_files.append(line_contents)

            line = fhandle.readline()

    if not my_package_csv_files is None:
        columns = my_package_csv_files[0] # get the header columns
        data_df = pd.DataFrame(data = my_package_csv_files[1:], columns = columns)
        
    return data_df 

def parks_names():
    """
    NAME: parks_names
    ----------
    DESCRIPTION: Returns a list of national parks for the user to search for the exact name of 
    the national park they want to query for.
    ----------
    PARAMETERS: None.
    -------
    RETURNS: A pandas dataframe of the names of the park names to use in queries
    """
    parks=parks_list()
    parks_names=pd.DataFrame(parks['fullName'])
    pd.set_option("display.max_rows", None, "display.max_columns", None)
    parks_names= parks_names.rename(columns={"fullName":"Park Names to Search for"})
    return(parks_names)
    display(parks_names.style.hide_index())
    
    
def dist_calc (lat,long,n):
    """
    NAME: dist_calc
    ----------
    DESCRIPTION: Returns the closest n national parks based on given latitude and longitude.
    Does not require an API key but requires user to provide the latitude and longitude of an
    exact location
    ----------
    PARAMETERS:
    lat: float, latitude of the origin location
    long: float, longitude of the origin location
    n: number of national parks to be listed
    ----------
    RETURNS: A pandas dataframe of closest parks to you and their approximate distance in Km
    """
    park_dist = pd.DataFrame(columns = ["Closest parks to you", "Approximate Distance in Km"])
    parks=parks_list()
    for index,row in parks.iterrows():
        #iterating over each park and retrieved location
        #calculating distance of each park using geopy package
        dist = geopy.distance.distance((lat,long), (row['latitude'],row['longitude'])).km
        temp = pd.DataFrame([[row["fullName"],dist]], columns = ["Closest parks to you", "Approximate Distance in Km"])
        park_dist=park_dist.append(temp)
        #among all distances calculated, selecting top or bottom n result
    return park_dist.nsmallest(n,"Approximate Distance in Km")

def how_far(park_name, lat, long):
    """
    NAME: how_far
    ----------
    DESCRIPTION: Calculates the approximate euclidian distance (e.g. as a straight line between
    the two locations on the map) of a national park in Km based on user's latitude and longitude.
    ----------
    PARAMETERS:
    park_name: str, the name of the national park user search for
    lat: float, latitude of the origin location
    long: float, longitude of the origin location
    -------
    RETURNS: A string stating the calculated distance
    """
    park_name=name_check(park_name)
    parks=parks_list()
    #if the park name user entered doesn't exist in the database, user is asked to check a name list
    assert (parks[parks['fullName']==park_name]).empty==False, f"{park_name} is not a valid park name to serach for. Please call parks_names() to see an alphabetic list of the parks you can search for."
    lat_park=parks.loc[parks['fullName'] == park_name, 'latitude'].item()
    long_park=parks.loc[parks['fullName'] == park_name, 'longitude'].item()
    #locating the specific park user looked for 
    #calculating the distance from the given location to the specific park
    dist = geopy.distance.distance((lat,long), (lat_park,long_park)).km
    result=str("The distance between your loaction and "+str(park_name)+" is approximately "+str(dist)+" km")  
    return(result)
    
    
def park_desc(park_name,token):
    """
    NAME:park_desc
    ----------
    DESCRIPTION: Returns the blurb description of a national park user search for, provided by 
    the US National Parks Services to give a snapshot of what that park is like to the user.
    ----------
    PARAMETERS:
    park_name: str, the name of the national park user search for
    token: should be acquired through this link: https://www.nps.gov/subjects/developer/get-started.htm
    -------
    RETURNS:A string as the description of the national park
    """
    park_name=name_check(park_name)
    parks=parks_list()
    assert (parks[parks['fullName']==park_name]).empty==False, f"{park_name} is not a valid park name to serach for. Please call parks_names() to see an alphabetic list of the parks you can search for."
    code=parks.loc[parks['fullName'] == park_name, 'parkCode'].item()
    #API code works on park code. retreiving the park code from the park name user entered
    url='https://developer.nps.gov/api/v1/parks?parkCode='+str(code)+'&api_key='+str(token)
    park = requests.get(url)
    if str(park.status_code)[0] == '4':
        raise Exception("Your API code is not working as expected. Please make sure you acquired one correctly.")
    elif park.status_code == 200:
        #retreiving the data field and then specific column of json output of API query
        park_df=pd.DataFrame(park.json()['data'])
        definition_df=park_df['description'].item()
        return str(definition_df)
    else: 
        raise Exception("You either reached your query limit or there is an unidentified problem with this server right now. Please try again later.")
         
def activity_list():
    """
    NAME: activity_list
    -------
    DESCRIPTION: Returns the full list of all activities that are available to do in national 
    parks for user to choose from.
    -------
    PARAMETERS: None.
    -------
    RETURNS: A string contains the list of activities
    """
    data_df = None
    my_package_csv_files = []
    
    with resources.open_text('nationalparks_v1.data', 'activities.csv') as fhandle: # , encoding = 'utf-8'

        line = fhandle.readline()
        while line:
            line_contents = [ '{}'.format(x) for x in list(csv.reader([line], delimiter=',', quotechar='"'))[0] ]
            if not line_contents is None and len(line_contents) > 0:
                my_package_csv_files.append(line_contents)

            line = fhandle.readline()

    if not my_package_csv_files is None:
        columns = my_package_csv_files[0] # get the header columns
        data_df = pd.DataFrame(data = my_package_csv_files[1:], columns = columns)
        
    return data_df 

    events="Here are the activities you can search for: "
    for index,row in data_df.iterrows():
        #retreiving all the activities from the activities list already pulled by API
        #preparing a shorter list by printing each item on the dataframe
        events+=row['name']+", "
    print(events[:-2])
    events=""
    
def activity_search(activity, token):
    """
    NAME: activity_search
    -------
    DESCRIPTION: Returns a dataframe that lists all the national parks that are suitable for the 
    activity the user searched for.
    ----------
    PARAMETERS:
    activity: str, name of the activity searched
    token: Should be acquired through this link: https://www.nps.gov/subjects/developer/get-started.htm
    -------
    RETURNS: A pandas dataframe with the list of national parks
    """data_df = None
    my_package_csv_files = []
    
    with resources.open_text('nationalparks_v1.data', 'activities.csv') as fhandle: # , encoding = 'utf-8'

        line = fhandle.readline()
        while line:
            line_contents = [ '{}'.format(x) for x in list(csv.reader([line], delimiter=',', quotechar='"'))[0] ]
            if not line_contents is None and len(line_contents) > 0:
                my_package_csv_files.append(line_contents)

            line = fhandle.readline()

    if not my_package_csv_files is None:
        columns = my_package_csv_files[0] # get the header columns
        data_df = pd.DataFrame(data = my_package_csv_files[1:], columns = columns)
        
    return data_df 

    data_df=data_df.apply(lambda x: x.astype(str).str.lower())
    assert (data_df[data_df['name']==activity]).empty==False, f"{activity} is not a valid activity name to serach for. Please call activity_list() to see a list of activities you can search for."
    code=data_df.loc[data_df['name']==activity,'id'].item()
    #getting park code from the park name entered to use in the API query
    url='https://developer.nps.gov/api/v1/activities/parks?q='+str(code)+'&api_key='+str(token)
    park_activities = requests.get(url)
    if str(park_activities.status_code)[0] == '4':
        raise Exception("Your API code is not working as expected. Please make sure you acquired one correctly.")
    elif park_activities.status_code==200:
        pactivities_df=pd.DataFrame(park_activities.json()['data'])
        alist=pactivities_df['parks']
        for i in alist:
            temp_df= pd.DataFrame.from_dict(i)
            temp_df= temp_df[["states","fullName"]]
            temp_df= temp_df.rename(columns={"states":"State","fullName": f"Parks you can do {activity}"})
            return(temp_df.style.hide_index())
        #given that the returned json result contains list of dictionaries, the park name is 
        #retreived by multiple iterations over the json field and only two fileds are returned
    else: 
        raise Exception("You either reached your query limit or there is an unidentified problem with this server right now. Please try again later.")
        
def park_popularity(sorting, n):
    """
    NAME: park_popularity
    -------
    DESCRIPTION: Scrapes the most up to date number of visitors information for national parks 
    from Wikipedia and returns the n number of most and least visited national parks.
    -------
    PARAMTERS:
    sorting: str, identifies the sorting order. Enter "most" or "least"
    token: should be acquired through this link: https://www.nps.gov/subjects/developer/get-started.htm
    -------
    RETURNS: A pandas dataframe with the name of the park and the number of visitors
    """
    wiki=pd.read_html('https://en.wikipedia.org/wiki/List_of_national_parks_of_the_United_States')[1]
    wiki_names = wiki[[col for col in wiki.columns if 'Name' in col]]
    wiki_num=wiki[[col for col in wiki.columns if 'visitor' in col]]
    #scraping latest visitor information per national park from Wikipedia
    wikifinal=pd.concat([wiki_names, wiki_num], axis=1)
    wikifinal.rename(columns = {list(wikifinal)[0]: 'Name of the Park'}, inplace = True)
    wikifinal.rename(columns = {list(wikifinal)[1]: 'Number of Visitors'}, inplace = True)
    wikifinal['Name of the Park'] = wikifinal['Name of the Park'].str.replace('*','', regex=True)
    wikifinal["Number of Visitors"] = pd.to_numeric(wikifinal["Number of Visitors"])
    #formatting the wikipedia table by getting rid of * and selecting and renaming only necessary column
    if sorting == "most":
        disp= wikifinal.nlargest(n,"Number of Visitors")
    elif sorting =="least":
        disp= wikifinal.nsmallest(n,"Number of Visitors")
        #returning highest or lowest number of visitors per park
    else: 
        raise Exception("Please use 'most' or 'least' as you search order")
    disp['Number of Visitors'] = disp.apply(lambda x: "{:,}".format(x['Number of Visitors']), axis=1)
    #formatting the visitor number by commas for aesthetics purposes
    return disp.style.hide_index()

def alerts(park_name, token):
    """
    NAME: alerts
    ----------
    DESCRIPTION: Returns the active alerts existing for a park on US National Park Services along
    with their description and the latest announcement date.
    ----------
    PARAMETERS:
    info_tye: str, can only be alerts, campgrounds, amenities, places or people
    state_code: 2 letter code of the US state queried
    limit: # of entries to be queried. Hourly limit of this API is 1000 requests
    api_key: should be acquired through this link: https://www.nps.gov/subjects/developer/get-started.htm
    -------
    RETURNS: Multiple strings that contains the announcement name, category and the description of
    the alert.
    """   
    park_name=name_check(park_name)
    parks=parks_list()
    assert (parks[parks['fullName']==park_name]).empty==False, f"{park_name} is not a valid park name to serach for. Please call parks_names() to see an alphabetic list of the parks you can search for."
    code=parks.loc[parks['fullName'] == park_name, 'parkCode'].item()
    #getting park code from the park name entered to use in the API query
    api_url = "https://developer.nps.gov/api/v1/alerts?parkCode="+str(code)+"&api_key="+str(token)
    r = requests.get(str(api_url))
    if str(r.status_code)[0] == '4':
        raise Exception("Your API code is not working as expected. Please make sure you acquired one correctly.")
    elif r.status_code == 200:
        print("Here are the active alerts for this park:")
        for i in r.json()['data']:
            print(f"{i['category']} announced on {i['lastIndexedDate']}.")
            print(f"Description: {i['description']}")   
            print(f"If you want to learn more about this alert, visit {i['url']}")
            #selecting multiple fields and preparing a paragraph using f strings with only the necessary
            #information from a bigger alerts table
    else: 
        raise Exception("You either reached your query limit or there is an unidentified problem with this server right now. Please try again later.")
        
def pet_friendly(park_name, token):
    """
    NAME: pet_friendly
    ----------
    DESCRIPTION: Informs you whether this national park is completely free of pet restrictions or guides you to another function to learn about the restrictions
    ----------
    PARAMETERS:
    park_name: The national park that you would like to go
    token: should be acquired through this link: https://www.nps.gov/subjects/developer/get-started.htm
    -------
    RETURNS: A string that states whether there are pet restrictions or not.
     """
    park_name=name_check(park_name)
    parks=parks_list()
    assert (parks[parks['fullName']==park_name]).empty==False, f"{park_name} is not a valid park name to serach for. Please call parks_names() to see an alphabetic list of the parks you can search for."
    code=parks.loc[parks['fullName'] == park_name, 'parkCode'].item()
    #getting park code from the park name entered to use in the API query
    api_code='https://developer.nps.gov/api/v1/thingstodo?parkCode='+str(code)+'&api_key='+str(token)
    r = requests.get(str(api_code))
    if str(r.status_code)[0]=='4':
        raise Exception("Your API code is not working as expected. Please make sure you acquired one correctly.")
    elif r.status_code==200:
        pets_df=pd.DataFrame(r.json()['data'])
        #since there is no single "pet friendliness" identifier, selecting multiple columns that
        #may list a pet restriction and building a condition that if any of them has "true" value
        #which indicates a restriction, warning the user that there are pet restrictions in the park
        if pets_df.empty:
            return str("There are no pet restrictions in this park. You are good to go!")
        elif ((pets_df[pets_df['arePetsPermittedWithRestrictions'].str.contains("true")]).empty or (pets_df[pets_df['arePetsPermitted'].str.contains("true")]).empty):
            return str("Pets are permitted in this park with certain restrictions. Please call pet_restrictions function to see what they are.")
    else: 
        return str("There are no pet restrictions in this park. You are good to go!")
        
def pet_restrictions(park_name, token):
    """
    NAME:pet_restrictions
    ----------
    DESCRIPTION: Provides a list of pet restrictions and locations that the restrictions apply for
    a specific national park.
    ----------
    PARAMETERS:
    park_name: The national park that you would like to go
    token: should be acquired through this link: https://www.nps.gov/subjects/developer/get-started.htm
    -------
    RETURNS: A dataframe that contains pet restrictions and the location of the restriction
     """
    park_name=name_check(park_name)
    parks=parks_list()
    assert (parks[parks['fullName']==park_name]).empty==False, f"{park_name} is not a valid park name to serach for. Please call parks_names() to see an alphabetic list of the parks you can search for."
    code=parks.loc[parks['fullName'] == park_name, 'parkCode'].item()
    #getting park code from the park name entered to use in the API query
    api_code='https://developer.nps.gov/api/v1/thingstodo?parkCode='+str(code)+'&api_key='+str(token)
    r = requests.get(str(api_code))
    pets_df=pd.DataFrame(r.json()['data'])
    if pets_df.empty:
        print("There are no pet restrictions in this park. You are good to go!")
    else:
        #pulling pet restrictions based on a given park name
        #selecting only the necessary columns of location and restriction description
        table = pd.DataFrame(pets_df[['location','petsDescription']])
        table= table.rename(columns={"location":"Restriction Location","petsDescription": "Description"})
        return(table.style.hide_index())