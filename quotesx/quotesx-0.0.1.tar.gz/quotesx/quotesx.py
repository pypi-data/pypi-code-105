def getQuote():
    import requests
    import json

    response = requests.get('https://zenquotes.io/api/random')
    json_data = json.loads(response.text)
    getQuote = json_data[0]['q'] + ' -' + json_data[0]['a']
    return(getQuote)