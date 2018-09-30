f = open("OI_school.csv")
op = open("mdt.txt","w")
for i in f.readlines():
    c = i.split('","')
    op.write(c[-3]+','+c[-2]+','+"".join([i+',' for i in eval(c[1])])[:-1]+'\n')
