import requests as rq
import sim

url = 'http://fanyi.youdao.com/translate'

def translate(words='', doctype='json', type_='AUTO'):
	if not words:
		return 'None'
	words = sim.filtemoji(words)
	params = {
		'doctype':doctype,
		'type': type_,
		'i': words
	}
	res = rq.get(url,params=params).json()
	if res['errorCode'] == 0:
		return res['translateResult'][0][0]['tgt']
	return -1

def translate_list(words='', doctype='json', type_='AUTO'):
	if not words:
		return 'None'
	results = []
	for word in words:
		results.append(translate(u''+sim.filtemoji(word)))
	return results

# def get_params(words='', doctype='json', type_='AUTO'):
# 	params = {
# 		'doctype':doctype,
# 		'type': type_,
# 		'i': words
# 	}
# 	return params

# def get(params):
# 	return rq.get(url,params=params).json()