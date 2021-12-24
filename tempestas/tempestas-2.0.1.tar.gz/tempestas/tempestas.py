import requests

class Weather:
    """
    Creates a Weather object with apikey as input and either a city or lat & lon coordinates.
    
    Package use:
    # Create a weather object using apikey and city/lat & lon arguments.
    # Get your own apikey from https://openweathermap.org
    # Don't use the below API key since it is guaranteed not to work. 
    # Wait for a few hours for the API to be activated.
    # All temperatures are in C°.
    
    
    # Using a city name
    >>> weather = Weather(apikey="774ca6a061b89f07a9cbb1a0b701c340", city="Toronto")
    
    # Using latitude and longitude coordinates
    >>> weather = Weather(apikey=""774ca6a061b89f07a9cbb1a0b701c340", lat=43.6532, lon=79.3832)
    
    # Get full weather data for the next 24 hours.
    >>> weather.next_1d()
    
    # Get simplified weather data for the next 24 hours
    >>> weather.next_1d_simplified()
    
    
    Sample url for sky condition icons:
    https://openweathermap.org/img/wn/10d@2x.png
    
    """
    
    def __init__(self, apikey, city=None, lat=None, lon=None):
        if city:
            url = f"https://api.openweathermap.org/data/2.5/forecast?q={city}&APPID={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        elif lat and lon:
            url = f"https://api.openweathermap.org/data/2.5/forecast?lat={lat}&lon={lon}&APPID={apikey}&units=metric"
            r = requests.get(url)
            self.data = r.json()
        else:
            raise TypeError("No city or lat & lon arguments passed.")
        
        if self.data['cod'] != '200':
            raise ValueError(self.data["message"])

    def next_1d(self):
        return self.data['list'][:9]
    
    def next_1d_simplified(self):
        simple_data = []
        for dict in self.data['list'][:9]:
            simple_data.append((dict['dt_txt'], str(dict['main']['temp'])+"".join('C°'), dict['weather'][0]['description'], dict['weather'][0]['icon']))
        return simple_data
