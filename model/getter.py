# -*- coding: UTF-8 -*-
import requests

def getpos(i):
	e = requests.get('http://api.map.baidu.com/?qt=s&c=1&wd='+i+'&rn=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk58896')
	ret = ["",""]
	try:
		cur = ""
		try:
			cur = e.text.split('","address_norm":"')[1].split('"')[0]
		except:
			e = requests.get('http://api.map.baidu.com/?qt=s&c='+e.text.decode("unicode-escape").split('{"code":')[1].split(',')[0]+'&wd='+i+'&rn=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk58896')
			cur = e.text.split('","address_norm":"')[1].split('"')[0]
		cur = cur.encode("utf-8").decode('unicode-escape')
		ret[0] = cur.split('[')[1].split('(')[0]
		ret[1] = cur.split('[')[2].split('(')[0]
	except:
		pass
	return ret

