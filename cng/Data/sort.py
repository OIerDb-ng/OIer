Filename = "opt1.csv"
f = open(Filename).read().split('\n')
opt = open("opt1.csv",'a')
for i in f:
	c = i.split(',')
	if c[3] == "":
		continue
	opt.write("%s,%s,%s,%s,%s,%s,%s,%s,\n"%(con,award,c[3],c[7],c[6],c[5],c[1],c[4]))
opt.close()

