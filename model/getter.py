# -*- coding: UTF-8 -*-
import requests

def getpos(i):
	e = requests.get('http://api.map.baidu.com/?qt=s&c=1&wd='+i+'&rn=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk58896')
	ret = ["",""]
	try:
		cur = ""
		print(e.text.split('","address_norm":"')[1].split('","admin_info"')[0])
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

f = open('a.txt')
opt = open('b.txt','w')
for i in f.readlines():
	a = i.split()[0]
	b = i.split()[1].strip()
	c = getpos(b)
	print(c)
	c[0] = c[0][:-1]
	if a == c[0]:
		opt.write(c[0]+','+c[1]+','+b+'\n')
		print(c[0]+','+c[1]+','+b)
	else:
		print(b+" NOT FOUND")
		opt.write(a+',未分区,'+b+'\n')
