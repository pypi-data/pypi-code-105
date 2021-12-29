r"""©2020 HARDRELICE. All Rights Reserved.
 ╻ ╻ ┏━┓ ┏━┓ ┏━┓ ┏━┓ ┏━╸ ╻   ╻  ┏━╸ ┏━╸ TM
 ┣━┫ ┣━┫ ┣━┛ ┃ ┃ ┣━┛ ┣━╸ ┃   ┃  ┃   ┣━╸
 ╹ ╹ ╹ ╹ ╹ ╹ ┗━┛ ╹ ╹ ┗━╸ ┗━╸ ╹  ┗━╸ ┗━╸

A tool using api <https://api.imjad.cn/pixiv/v1/> & <https://api.imjad.cn/pixiv/v2/> to search & download pic from Pixiv
"""

import api.translate.youdao as yd
from pathlib import Path
import requests as rq
import random
import json
import time
import sim
import os


module_path = os.path.join(os.path.dirname(__file__), '')
lost = open(os.path.join(module_path,'lost.png'),'rb').read()

testurl = 'https://i.pximg.net/img-master/img/2010/02/21/00/03/29/8913281_p0_master1200.jpg'

goodUsers = open(os.path.join(module_path, 'users.txt')).readlines()

host	= 'https://api.imjad.cn/pixiv/v1/'
host2	= 'https://api.imjad.cn/pixiv/v2/'

headers = {
	'user-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.122 Safari/537.36',
	'referer':'https://www.pixiv.net/',
	'host':'www.pixiv.net'
}

class Pixiv:
	def __init__(self, results, translate=0):
		self.results	= results
		self.response	= self.results['response'][0]
		self.title		= self.response['title']
		self.caption	= self.response['caption']
		self.tags		= self.response['tags']
		self.stats		= self.response['stats']
		self.image_urls	= self.response['image_urls']
		self.px_128x128	= self.image_urls['px_128x128']
		self.px_480mw	= self.image_urls['px_480mw']
		self.small		= self.image_urls['small']
		self.medium		= self.image_urls['medium']
		self.large		= self.image_urls['large']
		self.width		= self.response['width']
		self.height		= self.response['height']
		self.time       = self.response['created_time']
		self.last_time	= self.response['reuploaded_time']
		self.age_limit	= self.response['age_limit']
		self.user		= self.response['user']
		self.id_		= self.user['id']
		self.account	= self.user['account']
		self.name		= self.user['name']
		self.avartar	= self.user['profile_image_urls']['px_50x50']
		self.profile	= self.user['profile']
		self.is_manga	= self.response['is_manga']
		self.manga		= []
		if self.is_manga:
			self.pages	= self.response['metadata']['pages']
			for page in self.pages:
				self.manga.append(page['image_urls']['large'])
		if translate:
			self.title		= yd.translate(words = self.response['title'])
			self.caption	= yd.translate(words = self.response['caption'])
			self.tags		= yd.translate_list(words = self.response['tags'])

class User:
	def __init__(self, response):
		self.id_		= response['user']['id']
		self.account	= response['user']['account']
		self.name		= response['user']['name']
		self.avartar	= response['user']['profile_image_urls']['medium']
		self.is_premium	= response['profile']['is_premium']
		self.illusts	= response['profile']['total_illusts']
		self.manga		= response['profile']['total_manga']
		self.novels		= response['profile']['total_novels']
		self.webpage	= response['profile']['webpage']
		self.gender		= response['profile']['gender']
		self.region		= response['profile']['region']
		self.code		= response['profile']['country_code']
		self.twitter	= response['profile']['twitter_url']
		self.pawoo		= response['profile']['pawoo_url']

def getImg_old(url = 0, name = 0, path = './', type_ = 'jpg', id_ = 0, setting = 'large', useCurl = 0):
	if url:
		if not name:
			name_ = str(sim.tuple2str(sim.localtime(6)))
		else:
			name_ = str(name)
		path_ = os.path.join(path, sim.standardfile(name_) + '.' + type_)
		if not Path(path).exists():
			os.mkdir(path)
			print('[N] mkdir successed')
		if useCurl:
			os.system('curl --header "referer: https://www.pixiv.net/" -o '+ path_ + ' ' + url)
		else:
			img = rq.get(url, stream = True, headers = headers)
			length = float(img.headers['content-length'])
			length_M = length / 1000 / 1000
			length_M_str = str(length_M)[:4]
			count = 0
			count_tmp = 0
			delta = 0.5
			cnt = 0
			time1 = time.time()
			with open(path_, 'ab') as f:
				for chunk in img.iter_content(chunk_size = 512):
					if chunk:
						f.write(chunk)
						f.flush()
						count += len(chunk)
						if time.time() - time1 > delta:
							percent = count / length * 100
							num = int(percent / 2)
							speed_raw = (count - count_tmp)/delta
							speed = (count - count_tmp) / 1000 / 1000 / delta
							count_tmp = count
							left = str(int((length-count)/speed_raw))
							print('\r' + num*'█' + (50-num)*' ' + str(percent)[:4] + '% ' + str(speed)[:4] + 'M/s ' + length_M_str +'M ' + left + 's   ',end='',flush=True)
							time1 = time.time()
				f.close()
		print('\n','[N]',str(name_) + '.' + type_, 'successfully downloaded')
	else:
		results, processed = getInfo(id_ = id_)
		if results == None:
			return
		image_urls = processed.image_urls
		if not name:
			name = processed.title
		getImg(url = image_urls[setting], name = name, path = path, type_ = type_, setting = setting, useCurl = useCurl)

def getImg(url = 0, name = 0, path = './', type_ = 'jpg', id_ = 0, setting = 'large', useCurl = 0):
	if url:
		if not name:
			name_ = str(sim.tuple2str(sim.localtime(6)))
		else:
			name_ = str(name)
		path_ = os.path.join(path, sim.standardfile(name_) + '.' + type_)
		if not Path(path).exists():
			os.mkdir(path)
			print('[N] mkdir successed')
		if useCurl:
			os.system('curl --header "referer: https://www.pixiv.net/" -o '+ path_ + ' ' + url)
		else:
			img = sim.download(url, headers = headers, delta_time = 0.1)
			f = open(path_, 'ab')
			f.write(img.getvalue())
			f.close()
		print('\n','[N]',str(name_) + '.' + type_, 'successfully downloaded')
		return
	else:
		results, processed = getInfo(id_ = id_)
		if results == None:
			return
		image_urls = processed.image_urls
		if not name:
			name = processed.title
		getImg(url = image_urls[setting], name = name, path = path, type_ = type_, setting = setting, useCurl = useCurl)

def getImg_raw(url = 0, id_ = 0, setting = 'large'):
	if url:
		print('[N]','start to get content')
		try:
			img = rq.get(url, headers = headers)
			raw = img.content
			print('[N]','successfully got content')
			return raw
		except :
			print('[E]','something went wrong')
	if id_:
		try:
			results, processed = getInfo(id_=id_)
			if results['status'] == 'success':
				image_urls = processed.image_urls
			raw = getImg_raw(url = image_urls[setting], setting = setting)
			return raw
		except:
			print('[E]','something went wrong')
	return lost

def getImg_raw_test(url = 0, id_ = 0, setting = 'large'):
	if url:
		print('[N]','start to get content')
		try:
			img = sim.download(url, headers = headers, delta_time = 0.5)
			raw = img.getvalue()
			print('[N]','successfully got content')
			return raw
		except :
			print('[E]','something went wrong')
	if id_:
		try:
			results, processed = getInfo(id_=id_)
			if results['status'] == 'success':
				image_urls = processed.image_urls
			raw = getImg_raw(url = image_urls[setting], setting = setting)
			return raw
		except:
			print('[E]','something went wrong')
	return lost

def getImg_raw_flex(url = 0, id_ = 0, setting = 'large', object_ = None, delta_time = 1):
	if url:
		img = sim.download(url, headers = headers, delta_time = delta_time, object_ = object_)
		if not img:
			return 0
		return img.getvalue()
	else:
		results, processed = getInfo(id_ = id_)
		if results == None:
			return
		image_urls = processed.image_urls
		return getImg_raw_flex(url = image_urls[setting], setting = setting, object_ = object_, delta_time = delta_time)

def getImgList(idList, path = 'pixiv_temp', type_ = 'jpg',setting = 'large', useCurl = 0):
	for id_ in idList:
		try:
			id_[7]
			int(id_)
			getInfo(id_)
		except:
			continue
		getImg(id_ = id_, path = path, type_ = type_, setting = setting, useCurl = useCurl)

def getImgList_raw(idList, path = 'pixiv_temp',type_ = 'jpg',setting = 'large',useCurl = 0):
	rawList = []
	for id_ in idList:
		raw = getImg_raw(id_ = id_, setting = setting)
		rawList.append(raw)
	return rawList


def getInfo(id_, translate=0):
	params	= {
		'type': 'illust',
		'id':id_
	}
	results	= rq.post(url = host, params = params).json()
	print(results)
	# print(results)
	if results['status'] == 'success':
		processed = Pixiv(results, translate)
		return results, processed
	else:
		print('[E] Failed!')
		return None, None
	# with open('info.txt','w') as fp:
	# 	json.dump(results, fp, indent=2)
	# print(rq.post(url=host, params=params).url)
	# print(type(results),'||',results)

def getManga(id_, path = './', type_ = 'jpg', setting = 'large', useCurl = 0):
	results, processed = getInfo(id_)
	path = os.path.join(path, sim.standardfile(processed.title))
	page = 1
	for manga in processed.manga:
		getImg(url = manga, name = str(page), path = path, type_ = type_, useCurl = useCurl)
		page += 1

def getResponseId(response):
	idList = []
	for res in response:
		idList.append(int(res['id']))
	return idList

def getRankId(response):
	idList = []
	for res in response[0]['works']:
		idList.append(int(res['work']['id']))
	return idList

def getSearchImg(word, setting = 'small', path = './', mode = 'tags', order = 'desc', period = 'all', page = 1, per_page = 30):
	
	getImgList(getResponseId(search(word, mode = mode, order = order, period = period, page = page, per_page = per_page)), setting = setting, path = path)

def getUserInfo(id_):
	params	= {
		'type': 'member',
		'id': id_
	}
	results	= rq.post(url = host2, params = params).json()
	results['profile_publicity'] = ''
	results['workspace'] = ''
	try:
		return sim.easyclassify(results)
	except:
		print('[E]','class failed')
		return results

def getUserWorks(id_, period = 'all', page = 1, per_page = 30):
	params	= {
		'type': 'member_illust',
		'id': id_,
		'period': period,
		'page': page,
		'per_page': per_page
	}
	results	= rq.post(url = host, params = params).json()
	if results['status'] == 'success':
		return getResponseId(results['response'])

def search(word, mode = 'tags', order = 'desc', period = 'all', page = 1, per_page = 30):
	params	= {
		'type': 'search',
		'word': word,
		'mode': mode,
		'order': order,
		'period': period,
		'page': page,
		'per_page': per_page
	}
	results	= rq.post(url = host, params = params).json()
	if results['status'] == 'success':
		return getResponseId(results['response'])
	else:
		return -1

def rank(mode = 'daily',date = ''):
	params	= {
		'type': 'rank',
		'mode': mode,
		'date': date
	}
	results	= rq.post(url = host, params = params).json()
	if results['status'] == 'success':
		return getRankId(results['response'])
	else:
		return -1

def randomGoodUserId():

	return int(goodUsers[random.randint(0, len(goodUsers))][:-1])

def randomGoodUserWorkId():
	works = getUserWorks(randomGoodUserId())
	return int(works[random.randint(0, len(works))])















