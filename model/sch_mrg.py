# -*- coding: UTF-8 -*-
pos = eval(open("Pgot.txt").read())
l = []
poid = {}
s = open("school_oped_ori.txt").read().split('\n')

for i in s:
	cc = i.split(',')
	fnd = 0
	for j in cc[2:]:
		if j not in pos:
			continue
		if pos[j] in poid:
			print("MERGED ",l[poid[pos[j]]],cc)
			l[poid[pos[j]]].extend(cc[2:])
			fnd  = 1
			break
	if fnd == 0:
		for j in cc[2:]:
			if j in pos:
				poid[pos[j]] = len(l)
		l.append(cc)

opt = open("school_new.txt","w")
for i in l:
	opt.write("".join([j+"," for j in i])[:-1]+'\n')
opt.close()

