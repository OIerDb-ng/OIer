# -*- coding: UTF-8 -*-
import re,json,time
from pypinyin import lazy_pinyin as lapi
contests = {}
awd_by_name = {}
grades = {"高二":5,"初三":3,"高三":6,"高一":4,"初二":2,"中六":6,
	"中五":5,"初一":1,"初四":4,"中四":4,"高二年级":5,"中一":1,"中二":2,"中三":3,"六年级":0,"五年级":-1,"小六":0,"六":0,"小学":0,"初中":2.213472384803661,"预初":0}
sex = {"男":1,"女":-1,"@":0}
st = time.time()
school_id = {}
school_pos = {}
general = {'APIO': 4.5790, 'NOI': 4.7086, 'WC': 4.6628, 'CTSC': 4.6140, 'NOID类': 4.6678, 'NOIP提高': 4.6761, 'NOIP普及': 2.2134}

def output():
    py_sp = {}
    for i in open("special_pinyin.txt").readlines():
        py_sp[i.split('\t')[0]] = i.split('\t')[1].strip()
	result = open("result.txt","w")
	id = 0
	for i in awd_by_name:
        piny = ""
        for ecp in py_sp:
            if ecp[0] in i and i.find(ecp[0]) == 0:
                piny = ecp[1] + "".join( [ io[0] for io in lapi(i[len(ecp[0]):]) ])
                break
        if piny == "":
            piny = "".join( [ io[0] for io in lapi(i) ])
		for j in awd_by_name[i]:
			csex = 0
			cyear = 0
			cycnt = 0
			for k in j:
				del k["name"]
				#del k["cal_y"]
				if csex == 0:
					csex = k["sex"]
				del k["sex"]
				cyear += k["cal_y"]
				cycnt+=1
				del k["cal_y"],k["rule"],k["year"]
			cyear = int(cyear/cycnt+0.5)
			result.write(str(id)+","+i+",,,"+piny+',,"'+json.dumps(j,ensure_ascii=False).replace('"',"'")+'",'+str(csex)+",,"+str(cyear)+"\n")
			id+=1
	result.close()
with open("school_oped.txt") as src:
	cnt = -1
	for i in src:
		cnt+=1
		for j in i.split(',')[2:]:
			school_pos[cnt] = i.split(',')[0]+i.split(',')[1]
			school_id[j.strip()] = cnt
with open("data.txt") as source:
	for i in source:
		cur = i.strip().split(',')
		cname = cur[0]
		if not cname in contests.keys():
			year = re.findall(r"[0-9]{4}", cname, re.MULTILINE)[0]
			contests[cname] = {"identity":cname,"participants":[],"year":int(year),"ctype":cname.replace(year,""),"sure":[]}
		grade = 10000
		if cur[3] in grades.keys():
			grade = grades[cur[3]]
		elif cur[3]!='@':
			try:
				grade = contests[cname]["year"]-int(re.findall(r"[0-9]{4}", cur[3], re.MULTILINE)[0])+1+3*("高" in cur[3])
			except:
				print(cur)
		cur = {"identity":cname,"ctype":contests[cname]["ctype"],"award_type":cur[1],"name":cur[2],"grade":cur[3],"school":cur[4].strip(),"school_id":school_id[cur[4].strip()],"score":cur[5],"province":cur[6],"sex":sex[cur[7]],"rank": 1,"year" : contests[cname]["year"],"rule" : hash(cur[8])}
		cur["cal_y"] = cur["year"]-grade-("NOIP" not in cur["ctype"])
		if grade == 10000:
			cur["cal_y"] = cur["year"]-general[cur["ctype"]]-("NOIP" not in cur["ctype"])
		if contests[cname]["participants"]!=[]:
			lp = contests[cname]["participants"][-1]
			if lp["score"]!=cur["score"] or cur["score"] == "@":
				cur["rank"] = len(contests[cname]["participants"])+1
			else:
				cur["rank"] = lp["rank"]
		contests[cname]["participants"].append(cur)
		if cur["name"] not in awd_by_name:
			awd_by_name[cur["name"]] = []
		#print( cur["name"])
		awd_by_name[cur["name"]].append([cur])
def oi_year(i):
	return i["year"]-("NOIP" not in i["ctype"])
def diff_ana(a,b):
	for i in a:
		for j in b:
			if i["identity"] == j["identity"]:
				return 100000
			if abs(i["sex"]-j["sex"]) == 2:
				return 100000
			if i["rule"] and j["rule"]:
				return 10000*(i["rule"]!=j["rule"])
	cdst = 0
	sid1 = 0
	sid2 = 0
	minya,maxya,minyb,maxyb = 10000,0,10000,0
	for i in a:
		if sid1 == 0:
			sid1 = i["school_id"]
		if sid1 != 0 and sid1 != i["school_id"]:
			return 10000
		cc = oi_year(i)
		minya = min(minya,cc)
		maxya = max(maxya,cc)
	for i in b:
		if sid2 == 0:
			sid2 = i["school_id"]
			if sid2 != 0 and sid2 != i["school_id"]:
				return 10000
		cc = oi_year(i)
		minyb = min(minyb,cc)
		maxyb = max(maxyb,cc)
	cdst += (minyb-maxya-1)*80
	cy = 0
	if sid1 != sid2:
		cy+=1
		cdst+=60
	if school_pos[sid1]!=school_pos[sid2]:
		cy+=1
		cdst+=60
	cdst+=max((maxya+1-minyb)*cy*100,0)
	myear = 10000
	gyear = -1
	for i in a+b:
		myear = min(myear,i["cal_y"])
		gyear = max(gyear,i["cal_y"])
	cdst+=(gyear-myear)*100
	return cdst

for each_n in awd_by_name:
    globeid = 0
	while 1:
		awd_by_name[each_n] = sorted(awd_by_name[each_n],key = lambda i:oi_year(i[0]))
		minn,cs = 10000,len(awd_by_name[each_n])
		ml,mr = 0,0
		clen = len(awd_by_name[each_n])
		for i in range(clen):
			for j in range(i+1,clen):
				cg = diff_ana(awd_by_name[each_n][i],awd_by_name[each_n][j])
				if cg<minn:
					minn,ml,mr = cg,i,j
		if minn<200:
			awd_by_name[each_n][ml].extend(awd_by_name[each_n][mr])
			del awd_by_name[each_n][mr]
		else:
			break
output()

