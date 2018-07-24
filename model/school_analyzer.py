# -*- coding: UTF-8 -*-
import sys,re,json,time
reload(sys)
sys.setdefaultencoding("UTF-8")
st = time.time()
school_id = {}
school_info = []
tp_to_int = {"一等奖":0,"二等奖":1,"三等奖":2,"金牌":0,"银牌":1,"铜牌":2}

sc = [100,90,80,70,60,50]+[40]*4+[30]*20+[25]*30+[15]*90+[10]*100+[5]*200+[2]*500
sc_rt = {"NOI":1,"NOID类":0.75,"CTSC":0.6,"WC":0.5,"APIO":0.4,"NOIP提高":0.1,"NOIP普及":0.06}
ppl_rt = {"NOI":1,"CTSC":1,"WC":1,"APIO":1,"NOIP提高":0.075,"NOIP普及":0.075,"NOID类":1}
rk = {}

with open("school_merged.txt") as src:
	cnt = -1
	for i in src:
		cnt+=1
		school_info.append({"id":cnt,"name":[],"awards":{},"rating":0})
		for j in i.split(',')[1:]:
			school_id[j.strip()] = cnt
			school_info[-1]["name"].append(j.strip())
def dmp(a):
	return json.dumps(a, encoding="UTF-8", ensure_ascii=False).replace('"',"'")
with open("data.txt") as source:
	for i in source:
		cur = i.strip().split(',')
		cname = cur[0]
		if not "D" in cname:
			if not cname in rk:
				rk[cname] = []
			if cur[5]!="@":
				rk[cname].append(int(cur[5]))
				crk = rk[cname].index(int(cur[5]))
			else:
				rk[cname].append(0)
				crk = len(rk)
		else:
			ccname = cname[:7]
			rk[ccname].append(int(cur[5]))
			rk[ccname].sort(reverse = True)
			crk = rk[ccname].index(int(cur[5]))
			rk[ccname].remove(int(cur[5]))
		year = int(re.findall(r"[0-9]{4}", cname, re.MULTILINE)[0])
		ctype = cname.replace(str(year),"")
		award_type = tp_to_int[cur[1][len(cur[0]):]]
		schid = school_id[cur[4]]
		caw = school_info[schid]["awards"]
		if not ctype in caw:
			caw[ctype] = {}
		if not year in caw[ctype]:
			caw[ctype][year] = [0,0,0]
		caw[ctype][year][award_type]+=1
		school_info[schid]["awards"] = caw
		school_info[schid]["rating"] += sc[max(int(crk*ppl_rt[ctype]),0)]*sc_rt[ctype]*(0.8**(2018-year))
f = open("school_data.txt","w")
school_info = sorted(school_info,key = lambda t: t["rating"])
rk = ["A","Z","AA","ZZ","AAA","ZZZ","AAAA","ZZZZ","AAAAA","ZZZZZ","AAAAAA","ZZZZZZ"]
rkreq = [2000,800,400,150,80,60,40,30,15,5,1.5,0]
for i in school_info:
	cr = ""
	for kk in range(12):
		if i["rating"]>rkreq[kk]:
			cr = rk[kk]
			break
	f.write('"'+str(i["id"])+'","'+dmp(i["name"])+'","'+dmp(i["awards"])+'","'+str(int(i["rating"]*10))+'","'+cr+'"\n')
