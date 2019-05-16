# -*- coding: UTF-8 -*-
import re,json,time
from pypinyin import lazy_pinyin as lapi
contests = {}
awd_by_name = {}
final_output_data = []
grades = {"高二":5,"初三":3,"高三":6,"高一":4,"初二":2,"中六":6,
	"中五":5,"初一":1,"初四":4,"中四":4,"高二年级":5,"中一":1,"中二":2,"中三":3,"七年级":1,"六年级":0,"五年级":-1,"四年级":-2,"三年级":-3,"二年级":-4,"一年级":-5,"小六":0,"六":0,"小学":0,"初中":2.213472384803661,"预初":0}
sex = {"男":1,"女":-1,"":0}
contest_date = {"NOIP提高":11/12.0,"NOIP普及":11/12.0,"APIO":5.3/12.0,"CTSC":5.6/12.0,"NOI":7/12.0,"NOID类":7/12.0,"WC":1/12.0}
st = time.time()
school_id = {}
school_pos = {}
general = {'APIO': 4.5790, 'NOI': 4.7086, 'WC': 4.6628, 'CTSC': 4.6140, 'NOID类': 4.6678, 'NOIP提高': 4.6761, 'NOIP普及': 2.2134}

sc = list(range(100,39,-1))+[i*0.01 for i in list(range(3600,750,-15))]+[i*0.01 for i in list(range(750,150,-3))]
sc_rt = {"NOI":1,"NOID类":0.75,"CTSC":0.2,"WC":0.5,"APIO":0.4,"NOIP提高":0.1,"NOIP普及":0.06}
cnts = {}
def output():
	result = open("result.csv","w")
	id = 0
	for j in final_output_data:
		i = j[-1]
		del j[-1]
		piny = j[-1]
		del j[-1]
		csex = 0
		cyear = 0
		j = sorted(j,key = lambda i: i['year']+contest_date[i['ctype']],reverse = True)
		for k in j:
			del k["name"]
			#del k["cal_y"]
			if csex == 0:
				csex = k["sex"]
			del k["sex"]
			if cyear == 0:
				cyear = k["cal_y"]
			del k["cal_y"],k["rule"],k["year"]
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
			cnts[cname] = 0
		cnts[cname]+=1
		grade = 10000
		if cur[3] in grades.keys():
			grade = grades[cur[3]]
		elif cur[3]!='':
			try:
				grade = contests[cname]["year"]-int(re.findall(r"[0-9]{4}", cur[3], re.MULTILINE)[0])+1+3*("高" in cur[3])
			except:
				print(cur)
		try:
			cur = {"identity":cname,"ctype":contests[cname]["ctype"],"award_type":cur[1],"name":cur[2],"grade":cur[3],"school":cur[4].strip(),"school_id":school_id[cur[4].strip()],"score":cur[5],"province":cur[6],"sex":sex[cur[7]],"rank": 1,"year" : contests[cname]["year"],"rule" : hash(cur[8])}
		except:
			print(i)
		cur["cal_y"] = cur["year"]-grade-("NOIP" not in cur["ctype"])
		if grade == 10000:
			cur["cal_y"] = cur["year"]-general[cur["ctype"]]-("NOIP" not in cur["ctype"])
		if contests[cname]["participants"]!=[]:
			lp = contests[cname]["participants"][-1]
			if lp["score"]!=cur["score"] or cur["score"] == "":
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
			if i["rule"] and j["rule"]:
				return 10000*(i["rule"]!=j["rule"])
			if abs(i["sex"]-j["sex"]) == 2:
				return 100000

	cdst = 0
	ccst = 80
	l = []
	poses = []
	provs = []
	minya,maxya,minyb,maxyb = 10000,0,10000,0
	for i in a:
		if i["school_id"] not in l:
			l.append(i["school_id"])
		if school_pos[i["school_id"]] not in poses:
			poses.append(school_pos[i["school_id"]])
		if i["province"] not in provs:
			provs.append(i["province"])
		cc = oi_year(i)
		minya = min(minya,cc)
		maxya = max(maxya,cc)
	for i in b:
		if i["school_id"] not in l:
			l.append(i["school_id"])
		if school_pos[i["school_id"]] not in poses:
			poses.append(school_pos[i["school_id"]])
		if i["province"] not in provs:
			provs.append(i["province"])
		cc = oi_year(i)
		minyb = min(minyb,cc)
		maxyb = max(maxyb,cc)
	ccst+=[0,-40,60,120,180,300,600,600,600][len(l)]
	ccst+=len(poses)*80-80
	ccst+=len(provs)*80-80
	cdst+=max((minyb-maxya-1)*ccst*0.5,0)
	cdst+= ccst-80
	myear = 10000
	gyear = -1
	for i in a+b:
		myear = min(myear,i["cal_y"])
		gyear = max(gyear,i["cal_y"])
	cc=(gyear-myear)*100
	if int(gyear)!=gyear or int(myear)!=myear:
		cc = max(cc-100,0)
	return cdst+cc

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
		if minn<=240:
			awd_by_name[each_n][ml].extend(awd_by_name[each_n][mr])
			del awd_by_name[each_n][mr]
		else:
			break
py_sp = {'逢': 'p', '区': 'o', '蕃': 'p', '折': 's', '句': 'g', '仇': 'q', '种': 'c', '查': 'z', '繁': 'p', '祭': 'z', '曾': 'z', '佴': 'n', '单': 's', '郇': 'x', '翟': 'z', '覃': 'q', '郗': 'c', '乐': 'y', '召': 's', '阚': 'k', '乜': 'n', '秘': 'b', '解': 'x'}

for i in awd_by_name:
	piny = ""
	if i[0] in py_sp:
		piny = py_sp[i[0]]+"".join( [ io[0] for io in lapi(i[1:]) ])
	else:
		piny = "".join( [ io[0] for io in lapi(i) ])
	for j in awd_by_name[i]:
		j.append(piny)
		j.append(i)
		final_output_data.append(j)
final_output_data = sorted(final_output_data,key = lambda i:sum([sc[int(j['rank']*400/cnts[j['identity']])]*sc_rt[j['ctype']]*(0.8**(2018-j['year'])) for j in i[:-2]]),reverse = True)
output()


