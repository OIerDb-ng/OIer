#!/usr/bin/env python3

from collections import Counter
from decimal import Decimal as D, getcontext
from itertools import chain
from sys import stderr
getcontext().prec = 64

provinces = ['安徽', '北京', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南',
			 '黑龙江', '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古', '山东', '山西',
			 '陕西', '上海', '四川', '天津', '新疆', '浙江', '重庆', '宁夏', '云南', '澳门',
			 '香港', '青海', '西藏', '台湾']

award_levels = ['金牌', '银牌', '铜牌', '一等奖', '二等奖', '三等奖', '国际金牌', '国际银牌', '国际铜牌']

def __main__():
	import json, pypinyin
	from contest import Contest
	global	add_contestant, contests, contest_type_coefficient,		\
			decay_coefficient, enrollment_middle, get_contest_id,	\
			get_grades, get_initials, get_mode, rank_coefficient

	with open('static/contests.json') as f:
		for contest in json.load(f):
			Contest.create(contest)

	with open('static/grades.json') as f:
		g_ = json.load(f)
	g_initial = g_['initial']
	g_element = g_['element']
	g_special = g_['special']

	with open('static/surnames.json') as f:
		surnames = json.load(f)

	with open('static/scoring.json') as f:
		scoring = json.load(f)

	rc_list_legacy =  [D(i) for i in range(100, 39, -1)]			\
					+ [D('0.15') * i for i in range(240, 50, -1)]	\
					+ [D('0.03') * i for i in range(250, 50, -1)]

	rc_list = [D(i) for i in range(100, 39, -1)]			\
			+ [D('0.15') * i for i in range(239, 50, -1)]	\
			+ [D('0.05') * i for i in range(150, -1, -1)]
	assert len(rc_list) == 401
	assert sorted(rc_list, reverse = True) == rc_list

	def get_initials(name):
		''' 获取拼音首字母。

		name: 姓名。
		'''
		return ''.join(get_initial_list(name))

	def get_initial_list(name):
		initial = pypinyin.lazy_pinyin(name, style=pypinyin.Style.FIRST_LETTER)
		for i in range(len(name), 0, -1):
			if name[:i] in surnames:
				initial[:i] = surnames[name[:i]]
		return initial

	def get_grades(grade_name):
		''' 获取可能的年级列表。

		grade_name: 年级名称。

		返回值: 以初一为 16，(2^可能年级) 列表之和，需要保证年级在 0 ~ 31 之间。
		'''

		if grade_name in g_special:
			return g_special[grade_name]
		ret, cur = g_initial, grade_name
		while True:
			if cur == '':
				ret = 1 << ret
				g_special.setdefault(grade_name, ret)
				return ret
			for element in g_element:
				if cur.startswith(element):
					ret += g_element[element]
					cur = cur[len(element):]
					break
			else:
				raise ValueError('未知的年级：\x1b[032m\'{}\'\x1b[0m'.format(grade_name))

	def enrollment_middle(contest, grades):
		''' 获取初中入学年份列表。

		contest: 比赛对象。
		grades: 所有可能的年级列表。

		返回值: set，表示所有可能的入学年份列表。
		'''

		year = contest.school_year()
		mask = grades
		ems = set()
		while mask:
			grade = (mask & -mask).bit_length() - 16
			ems.add(year - grade + 1)
			mask &= mask - 1
		return ems

	def get_mode(sets):
		''' 获取最佳初中入学年份。

		sets: 集合的列表，每个集合表示可能的入学年份集合。

		返回值: 最佳入学年份的列表。
		'''

		counter = Counter(chain(*sets))
		most = counter.most_common(1)[0][1]
		return sorted(k for k, v in counter.items() if v == most)

	def decay_coefficient(year):
		''' 获取因年份造成的衰变系数，<b>该函数可以自行修改</b>。

		year: 比赛年份。

		返回值: 系数，<b>需为 Decimal 类型</b>。
		'''

		return D('1.25') ** (year - 2000)

	def rank_coefficient(rank, total, name = None):
		''' 获取因排名产生的系数，<b>该函数可以自行修改</b>。

		rank: 当前排名。
		total: 总人数。
		name: 姓名，用于输出错误信息，无需用到。

		返回值: 系数，<b>需为 Decimal 类型</b>。
		'''

		if not (1 <= rank <= total):
			print('\x1b[01;33mwarning: \x1b[0m诡异的排名：\x1b[32m{}\x1b[0m / \x1b[32m{}\x1b[0m (from \x1b[32m{}\x1b[0m)，已自动 clamped'.format(rank, total, name), file = stderr)
		return rc_list[400 * max(min(rank, total), 1) // total]

	def contest_type_coefficient(type, name = None):
		''' 获取不同比赛类型产生的系数，<b>该函数可以自行修改</b>。

		type: <b>字符串</b>，为比赛类型。
		name: 姓名，用于输出错误信息，无需用到。

		返回值: 系数，<b>需为 Decimal 类型</b>。
		'''

		if type not in scoring:
			print('\x1b[01;33mwarning: \x1b[0m未知的比赛类型：\x1b[32m\'{}\'\x1b[0m (from \x1b[32m{}\x1b[0m)，不计算贡献'.format(type, name), file = stderr)
		return D(scoring.get(type, '0'))

__main__()
