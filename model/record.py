#!/usr/bin/env python3

from itertools import chain
import util
__school_penalty__ = {0: 0, 1: -40, 2: 60, 3: 120, 4: 180, 5: 300}

class Record:
	__auto_increment__ = 0

	def __init__(self, oier, contest, score, rank, level, grades, school, province, gender):
		Record.__auto_increment__ += 1
		self.id = Record.__auto_increment__
		self.oier = oier
		self.contest = contest
		self.score = score
		self.rank = rank
		self.level = level
		self.grades = grades
		self.school = school
		self.province = province
		self.gender = gender
		self.ems = util.enrollment_middle(contest, grades)

	def __repr__(self):
		return '{}(pro={},school={},grade={},c={})'.format(self.oier.name, self.province, self.school.name, self.grade, self.contest.name)

	@staticmethod
	def distance(A, B, inf = 2147483647):
		''' 获取两个记录组的距离。

		A: 第一个记录组。
		B: 第二个记录组。
		'''

		assert len(A) and len(B)

		for a in A:
			for b in B:
				if a.contest is b.contest:
					return inf
				if abs(a.gender - b.gender) == 2:
					return inf
				if a.contest.school_year() == b.contest.school_year() and len(a.ems & b.ems) == 0:
					return inf

		schools = set(record.school.id for record in chain(A, B))
		locations = set(record.school.location() for record in chain(A, B))
		provinces = set(record.province for record in chain(A, B))
		aem = util.get_mode([record.ems for record in A])
		bem = util.get_mode([record.ems for record in B])
		diff = min(abs(i - j) for i in aem for j in bem)

		return	__school_penalty__.get(len(schools), 600)		\
				+ 80 * (len(locations) + len(provinces) - 3)	\
				+ 100 * diff
