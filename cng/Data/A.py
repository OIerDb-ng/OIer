Filename = "4.csv"
con = "CSP2019入门"
award = "三等奖"
f = open(Filename).read().split('\n')
opt = open("opt2.csv",'a')
for i in f:
	c = i.split(',')
	if c[3] == "":
		continue
	opt.write("%s,%s,%s,%s,%s,%s,%s,%s,\n"%(con,award,c[3],c[7],c[6],c[5],c[1],c[4]))
opt.close()

