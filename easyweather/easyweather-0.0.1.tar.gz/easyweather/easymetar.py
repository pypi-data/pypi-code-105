


from bs4 import BeautifulSoup
from urllib.request import urlopen



def getWeather(location,toReturn = 'all',rawOrDcode = 'raw'):
	tempUrl = 'https://www.aviationweather.gov/metar/data?ids='
	tempFormat = '&format='
	urlEnd = '&date=&hours=0'
	url = tempUrl+location+tempFormat+rawOrDcode+urlEnd
	client = urlopen(url)
	page = client.read()
	client.close()
	pageSoup = BeautifulSoup(page,'html.parser')
	infoContainer = pageSoup.find('div',{'id':'awc_main_content_wrap'})
	try:
		allData = infoContainer.find('code').text
	except:
		return "no metar found for specified airport"
	dataSeparate = allData.split(" ")

	

	if toReturn == 'all':
		return allData

	elif toReturn == 'dataAt':
		return infoContainer.find('p').text

	elif toReturn=="location":
		return dataSeparate[0]

	elif toReturn=='dateTime':
		return dataSeparate[1]

	elif toReturn == 'wind':
		for block in dataSeparate:
			if "KT" in block:
				return block

	elif toReturn=='visibility':
		for block in dataSeparate:
			if "SM" in block:
				return block

	elif toReturn=='skyCondition':
		clouds=''
		for block in dataSeparate:
			if "SKC" in block or "SCT" in block or "CLR" in block or "FEW" in block or "OVC" in block or "BKN" in block:
				clouds+=block+' '
		return clouds

	elif toReturn=='TDPS':
		for block in dataSeparate:
			if "/" in block :
				return block

	elif toReturn=='Alt':
		for block in dataSeparate:
			if "A" in block and len(block)==5:
				return block

	elif toReturn=='RMK':
		return('RMK' + allData.split('RMK')[1])
	
	return "ERROR: getWeather() function call could not retrieve information. Function call may have been improperly formatted"

#print(getWeather('EHAM','TDPS'))