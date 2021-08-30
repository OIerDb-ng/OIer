#!/usr/bin/env python3

class School:
	__all_school_list__ = []
	__school_name_map__ = {}

	def __init__(self, idx, name, province, city, aliases):
		self.id = idx
		self.name = name
		self.province = province
		self.city = city
		self.aliases = aliases

	@staticmethod
	def create(name, province, city, aliases):
		''' 新建学校。

		name: 正式名称。
		province: 省份。
		city: 城市（或区）。
		aliases: 别名列表（可以为空）。
		'''

		idx = School.count_all()
		school = School(idx, name, province, city, aliases)
		School.__all_school_list__.append(school)
		School.__school_name_map__[name] = school
		for alias in aliases:
			School.__school_name_map__[alias] = school
		return school

	@staticmethod
	def by_name(name):
		''' 根据名称返回学校

		name: 学校名称。
		'''

		if name in School.__school_name_map__:
			return School.__school_name_map__[name]
		raise ValueError('未知的学校名：\x1b[32m\'{}\'\x1b[0m'.format(name))

	@staticmethod
	def count_all():
		'获取当前学校总数。'

		return len(School.__all_school_list__)

	def location(self):
		'获取位置，格式为 province,city。'

		return self.province + ',' + self.city
