# -*- coding: UTF-8 -*-
data = []
with open("tg.txt") as ipt:
	caw = ""
	for i in ipt.readlines():
		if not '\t' in i:
			caw = i.strip()
			continue
		spl = i.split('\t')
		data.append(["NOIP2018提高",caw,spl[3],spl[7],spl[6],spl[5],spl[2],spl[4]])
data = sorted(data,key = lambda x: -float(x[5]))
with open("tgout.txt","w") as opt:
	for i in data:
		opt.write(''.join([j.strip()+',' for j in i])+'\n')
