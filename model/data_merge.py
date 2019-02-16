# -*- coding: UTF-8 -*-
import sys, re, json, time
from pypinyin import lazy_pinyin as lapi
reload(sys)
sys.setdefaultencoding("UTF-8")
contests = {}
all_oiers = {}
grades = {
	"高二": 5,
	"初三": 3,
	"高三": 6,
	"高一": 4,
	"初二": 2,
	"中六": 6,
	"中五": 5,
	"初一": 1,
	"初四": 4,
	"中四": 4,
	"高二年级": 5,
	"中一": 1,
	"中三": 3,
	"六年级": 0,
	"五年级": -1,
	"小六": 0
}
sex = {"男": 1, "女": -1, "@": 0}
st = time.time()
school_id = {}

with open("merged.txt") as src:
	cnt = -1
	for i in src:
		cnt += 1
		for j in i.split(',')[1:]:
			school_id[j.strip()] = cnt

with open("data.txt") as source:
	for i in source:
		cur = i.strip().split(',')
		cname = cur[0]
		if not cname in contests.keys():
			# Log new contest
			year = re.findall(r"[0-9]{4}", cname, re.MULTILINE)[0]
			contests[cname] = {
				"identity": cname,
				"participants": [],
				"year": int(year),
				"ctype": cname.replace(year, ""),
				"sure": []
			}
		grade = 10000
		s = 0
		if cur[3] in grades.keys():
			grade = grades[cur[3]]
		cur = {
			"identity": cname,
			"ctype": contests[cname]["ctype"],
			"award_type": cur[1][len(cur[0]):],
			"name": cur[2],
			"grade": grade,
			"school": cur[4],
			"school_id": school_id[cur[4]],
			"score": cur[5],
			"province": cur[6],
			"sex": sex[cur[7]],
			"rank": 1
		}
		if contests[cname]["participants"] != []:
			lp = contests[cname]["participants"][-1]
			if lp["score"] != cur["score"] or cur["score"] == "@":
				cur["rank"] = len(contests[cname]["participants"]) + 1
			else:
				cur["rank"] = lp["rank"]
		contests[cname]["participants"].append(cur)
print time.time() - st
for i in contests:
	con_year = 0
	if "NOIP" in contests[i]["identity"]:
		con_year = contests[i]["year"]
	else:
		con_year = contests[i]["year"] - 1
	for j in contests[i]["participants"]:
		cname = j["name"]
		if not cname in all_oiers:
			all_oiers[cname] = []
		bestu = -1
		bestr = 0
		cyear = con_year - j["grade"]
		for uid in range(len(all_oiers[cname])):
			if abs(all_oiers[cname][uid]["sex"] - j["sex"]) != 2:
				curr = 41
				if all_oiers[cname][uid]["year"] > 0 and cyear > 0:
					a = abs(all_oiers[cname][uid]["year"] - (cyear))
					if a == 1:
						curr -= 100
					if a >= 2:
						curr -= 100000
				for each_record in all_oiers[cname][uid]["records"]:
					if each_record["province"] == j["province"]:
						curr += 120
					if each_record["school_id"] == j["school_id"]:
						curr += 120
					if each_record["province"] != j["province"] and (
							each_record["grade"] - 3.5) * (
								j["grade"] - 3.5) > 0:
						curr -= 2400
					if each_record["identity"] == i:
						curr -= 100000
				if curr > bestr:
					bestr = curr
					bestu = uid
		if bestu != -1:
			#merge
			if all_oiers[cname][bestu]["sex"] == 0:
				all_oiers[cname][bestu]["sex"] = j["sex"]
			if all_oiers[cname][bestu]["year"] < 0:
				all_oiers[cname][bestu]["year"] = cyear
			all_oiers[cname][bestu]["records"].append(j)
		else:
			#new
			piny = "".join([io[0] for io in lapi(cname.decode("utf8"))])
			all_oiers[cname].append({
				"name": cname,
				"pinyin": piny,
				"sex": 0,
				"year": cyear,
				"records": [j]
			})
			bestu = len(all_oiers[cname]) - 1
		if all_oiers[cname][bestu]["sex"] == 0:
			all_oiers[cname][bestu]["sex"] = j["sex"]
print time.time() - st
n = open("result.txt", "w")
id = 0
for i in all_oiers:
	for j in all_oiers[i]:
		for k in j["records"]:
			del k["sex"]
			del k["name"]
		#n.write(json.dumps(j, encoding="UTF-8", ensure_ascii=False))
		n.write(
			str(id) + "," + j["name"] + ",,," + j["pinyin"] + ',,"' +
			json.dumps(j["records"], encoding="UTF-8", ensure_ascii=False).
			replace('"', "'") + '",' + str(j["sex"]) + ",," + str(j["year"]))
		id += 1
		n.write("\n")