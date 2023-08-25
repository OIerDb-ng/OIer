# -*- coding: UTF-8 -*-
import requests

pos = eval(open("lgot.txt").read())
import _thread
import time

fin = 0
def getpos(i):
	global fin
	if i in pos:
		fin+=1
		return
	e = requests.get('http://api.map.baidu.com/?qt=s&c=1&wd='+i+'&rn=10&ie=utf-8&oue=1&fromproduct=jsapi&res=api&callback=BMap._rd._cbk58896')
	#print(e.text)
	try:
		pos[i] = e.text.split('","address_norm":"')[1].split('","admin_info"')[0]
		fin+=1
	except:
		pass

f = open('alsch.txt').read().split('\n')

def getposes( threadName, delay):
	while len(f):
		a = f[-1]
		del f[-1]
		getpos(a)

for i in range(10):
	try:
		_thread.start_new_thread( getposes, ("Thread-1", 233, ) )
	except:
		print ("Error: 无法启动线程")

while 1:
	print(fin)
	time.sleep(3)
	with open("Pgot.txt","w") as opt:
		opt.write(str(pos))

