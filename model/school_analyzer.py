# -*- coding: UTF-8 -*-
import sys,re,json,time
st = time.time()
school_id = {}
school_info = []
tp_to_int = {"一等奖":0,"二等奖":1,"三等奖":2,"金牌":0,"银牌":1,"铜牌":2}

sc = list(range(100,39,-1))+[i*0.01 for i in list(range(3600,750,-15))]+[i*0.01 for i in list(range(750,0,-5))]
sc_rt = {"NOI":1,"NOID类":0.75,"CTSC":0.6,"WC":0.5,"APIO":0.4,"NOIP提高":0.1,"NOIP普及":0.06}
rk = {}
recy = {}
recd = {}
with open("school_oped.txt") as src:
	cnt = -1
	for i in src:
		cnt+=1
		school_info.append({"id":cnt,"name":[],"awards":{},"rating":0,"prov":i.split(',')[0],"city":i.split(',')[1]})
		for j in i.split(',')[2:]:
			school_id[j.strip()] = cnt
			school_info[-1]["name"].append(j.strip())
def dmp(a):
	return json.dumps(a, ensure_ascii=False).replace('"',"'")
dp = {}
with open("data.txt") as source:
	for i in source:
		if 'D类' in i:
			i = i.split('D类')[0]
		if not i.split(',')[0] in dp:
			dp[i.split(',')[0]] = 1
		else:
			dp[i.split(',')[0]] += 1
with open("data.txt") as source:
	for i in source:
		cur = i.strip().split(',')
		cname = cur[0].strip()
		if not "D" in cname:
			if not cname in rk:
				rk[cname] = []
			if cur[5]!="":
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
		#print(cur[1])
		#print(cur[0])
		award_type = tp_to_int[cur[1]]
		csn = cur[4].strip()
		if csn not in recy or year>recy[csn]:
			recy[csn] = year
			recd[csn] = 0
		recd[csn] += 1
		schid = school_id[cur[4].strip()]
		caw = school_info[schid]["awards"]
		if not ctype in caw:
			caw[ctype] = {}
		if not year in caw[ctype]:
			caw[ctype][year] = [0,0,0]
		caw[ctype][year][award_type]+=1
		school_info[schid]["awards"] = caw
		if 'D类' in cname:
			cname = cname.split('D类')[0]
		school_info[schid]["rating"] += sc[max(int(crk*390/dp[cname]),0)]*sc_rt[ctype]*(0.8**(2018-year))
f = open("school_data.txt","w")
school_info = sorted(school_info,key = lambda t: t["rating"],reverse = True)
rk = ["A+","A","A-","B+","B","B-","C","D","E","F","G","H"]
rkreq = [4000,1600,800,300,120,80,40,20,10,3,1.2,0]
count = 1
for i in school_info:
	cr = ""
	for kk in range(12):
		if i["rating"]>rkreq[kk]:
			cr = rk[kk]
			break
	f.write('"'+str(i["id"])+'","'+dmp(sorted(i["name"],key = lambda x:recy[x]*10000+recd[x],reverse = True))+'","'+dmp(i["awards"])+'","'+str(int(i["rating"]*10))+'","'+cr+'","'+i["prov"]+'","'+i["city"]+'","'+str(count)+'"\n')
	count+=1;
