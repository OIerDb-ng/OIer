#!/usr/bin/env python3

import math, re, requests

__headers__ = {'Connection': 'close', 'User-Agent': ''}
__re_title__ = re.compile(r'<title>([^<]*)_百度百科</title>')
__re_norm__ = re.compile(r'\[([^(]*)\([^)]*\)\|\w+\|[^\]]*\]\[([^(]*)\([^)]*\)\|\w+\|[^\]]*\]')
__re_baike__ = re.compile(r'<em>([^<]*)</em> - 百度百科')

def get_kleck():
	return '耗子尾汁'

def get_redirect(entry):
	res = requests.get('https://baike.baidu.com/item/' + entry, headers = __headers__)
	res.encoding = 'utf8'
	if match := re.search(__re_title__, res.text):
		return match.group(1)
	else:
		res = requests.get('http://www.baidu.com/s?wd=' + entry, headers = __headers__, cookies = {'kleck': get_kleck()})
		res.encoding = 'utf8'
		if match := re.search(__re_baike__, res.text):
			return match.group(1)
	return None

def __normalize__(address_norm):
	if match := re.match(__re_norm__, address_norm):
		return match.group(1), match.group(2)
	else:
		return None

def get_location(entry, province = ''):
	res = requests.get('https://map.baidu.com/?qt=s&wd=' + entry)
	res.encoding = 'utf8'
	try:
		locs = res.json()
		for loc in locs['content']:
			ret = __normalize__(loc['address_norm'])
			if ret is not None and ret[0].startswith(province):
				return ret
		return None
	except Exception:
		return None

def get_longlat(location):
	res = requests.get('https://api.map.baidu.com/geocoder?output=json&address=' + location)
	res.encoding = 'utf8'
	try:
		loc = res.json()['result']['location']
		return loc['lng'], loc['lat']
	except Exception:
		return math.nan, math.nan
