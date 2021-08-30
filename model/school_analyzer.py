# -*- coding: UTF-8 -*-
import sys,re,json,time,datetime,hashlib
st = time.time()
school_id = {}
school_info = []
tp_to_int = {"一等奖":0,"二等奖":1,"三等奖":2,"金牌":0,"国际金牌":0,"银牌":1,"铜牌":2}

sc = list(range(100,39,-1))+[i*0.01 for i in list(range(3600,750,-15))]+[i*0.01 for i in list(range(750,0,-5))]
sc_rt = {"IOI":2,"NOI":1,"NOID类":0.75,"CTSC":0.6,"WC":0.5,"APIO":0.4,"NOIP提高":0.1,"NOIP普及":0.04,"CSP提高":0.1,"CSP入门":0.04,"NOIP":0.15}
name_map = {}
rk = {}
recy = {}
recd = {}
with open("school_oped.txt",encoding='utf-8') as src:
    cnt = -1
    for i in src:
        cnt+=1
        try:
            school_info.append({"id":eval("0x"+hashlib.md5(i.split(',')[2].encode("utf8")).hexdigest())%998244353,"name":[],"awards":{},"rating":0,"prov":i.split(',')[0],"city":i.split(',')[1]})
        except:
            print(i)
        for j in i.split(',')[2:]:
            school_id[j.strip()] = cnt
            school_info[-1]["name"].append(j.strip())
def dmp(a):
    return json.dumps(a, ensure_ascii=False).replace('"',"'")
dp = {}
with open("data.txt",encoding='utf-8') as source:
    for i in source:
        if 'D类' in i:
            i = i.split('D类')[0]
        if not i.split(',')[0] in dp:
            dp[i.split(',')[0]] = 1
        else:
            dp[i.split(',')[0]] += 1
        if "IOI" in i.split(',')[0]:
            dp[i.split(',')[0]] = 300
with open("data.txt",encoding='utf-8') as source:
    for i in source:
        cur = i.strip().split(',')
        cname = cur[0].strip()
        if not "D" in cname:
            if not cname in rk:
                rk[cname] = []
            if cur[5]!="":
                rk[cname].append(float(cur[5].split("(")[0]))
                crk = rk[cname].index(float(cur[5].split("(")[0]))
                if "(" in cur[5]:
                    crk = int(cur[5].split("k")[1].split(")")[0])
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
        if ctype in name_map:
            ctype = name_map[ctype]
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
        school_info[schid]["rating"] += sc[max(int(crk*390/dp[cname]),0)]*sc_rt[ctype]*(0.75**(datetime.datetime.now().year-year))
#print(dp)
f = open("school_data.csv","w",encoding='utf-8')
f.write("id,name,awards,rating,division,province,city,rank\n")
school_info = sorted(school_info,key = lambda t: t["rating"],reverse = True)
rk = ["A+","A","A-","B+","B","B-","C","D","E","F","G","H"]
rkreq = [5000, 1800, 1000, 300, 120, 90, 45, 16, 9.0, 1.7, 1.08, 0.0]
count = 1
for i in school_info:
    cr = ""
    for kk in range(12):
        if i["rating"]>rkreq[kk]:
            cr = rk[kk]
            break
    c = []
    for j in i["name"]:
        if j not in recy:
            c.append(j)
    for j in c:
        i["name"].remove(j)
    f.write('"'+str(i["id"])+'","'+dmp(sorted(i["name"],key = lambda x:recy[x]*10000+recd[x],reverse = True))+'","'+dmp(i["awards"])+'","'+str(int(i["rating"]*100+1))+'","'+cr+'","'+i["prov"]+'","'+i["city"]+'","'+str(count)+'"\n')
    count+=1
