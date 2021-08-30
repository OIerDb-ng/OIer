(() => {
	'use strict';

	let OIerDb = Object.create(null), pred = () => true, update_succ = false;

	Object.defineProperty(OIerDb, 'provinces', {
		enumerable: true,
		value: ['安徽', '北京', '福建', '甘肃', '广东', '广西', '贵州', '海南', '河北', '河南',
				'黑龙江', '湖北', '湖南', '吉林', '江苏', '江西', '辽宁', '内蒙古', '山东', '山西',
				'陕西', '上海', '四川', '天津', '新疆', '浙江', '重庆', '宁夏', '云南', '澳门',
				'香港', '青海', '西藏', '台湾']
	});

	Object.defineProperty(OIerDb, 'award_levels', {
		enumerable: true,
		value: ['金牌', '银牌', '铜牌', '一等奖', '二等奖', '三等奖', '国际金牌', '国际银牌', '国际铜牌']
	});

	OIerDb.Contest = function (id, settings) {
		this.id = id;
		for (let setting in settings) this[setting] = settings[setting];
		this.reset_data();
	}

	OIerDb.Contest.prototype.reset_data = function() {
		this.contestants = [];
		this.level_counts = {};
	}

	OIerDb.Contest.prototype.school_year = function () {
		return this.year - !this.fall_semester;
	}

	OIerDb.Contest.prototype.n_contestants = function () {
		return this.capacity ? this.capacity : this.contestants.length;
	}

	OIerDb.Contest.prototype.add_contestant = function (record) {
		this.contestants.push(record);
		if (!(record.level in this.level_counts)) {
			this.level_counts[record.level] = 0;
		}
		++this.level_counts[record.level];
	}

	OIerDb.update = async function () {
		OIerDb.contests = OIerDb.contests.map((x, i) => new OIerDb.Contest(i, x));
		let digest = localStorage.data_sha512;
		let upstream = await (await fetch('/oierdb-ng/data-sha512')).text();
		if (digest !== upstream) {
			localStorage.data = await (await fetch('/oierdb-ng/data/result')).text();
			localStorage.data_sha512 = upstream;
		}
		OIerDb.data = localStorage.data;
		update_succ = true;
	}

	OIerDb.frontend_process = function () {
		if (!update_succ) {
			throw Error('请先调用 await OIerDb.update()');
		}
		OIerDb.contests.forEach(contest => contest.reset_data());
		OIerDb.schools.forEach(school => (school.members = [], school.records = []));
		let lines = OIerDb.data.split('\n'), data = [];
		for (let line of lines) {
			let fields = line.split(',');
			if (fields.length !== 9) continue;
			let [uid, initials, name, gender, enroll_middle, oierdb_score, ccf_score, ccf_level, compressed_records] = fields;
			let records = compressed_records.split('/').map(record => {
				let [contest_id, school_id, score, rank, province_id, award_level_id] = record.split(':');
				return {
					contest: OIerDb.contests[contest_id],
					school: OIerDb.schools[school_id],
					...(score !== '' && {score: parseFloat(score)}),
					rank: parseInt(rank),
					province: province_id in OIerDb.provinces ? OIerDb.provinces[province_id] : province_id,
					level: award_level_id in OIerDb.award_levels ? OIerDb.award_levels[award_level_id] : award_level_id
				};
			});
			let provinces = Array.from(new Set(records.map(record => record.province)));
			let oier = {
				rank: data.length,
				uid: parseInt(uid),
				initials,
				name,
				gender: parseInt(gender),
				enroll_middle: parseInt(enroll_middle),
				oierdb_score: parseFloat(oierdb_score),
				ccf_score: parseFloat(ccf_score),
				ccf_level: parseInt(ccf_level),
				records, provinces
			};
			records.forEach(record => {
				record.oier = oier;
				record.contest.add_contestant(record);
				record.school.records.push(record);
				record.school.members.push(oier);
			});
			data.push(oier);
		}
		OIerDb.oiers = data;
		OIerDb.contests.forEach(contest => contest.contestants.sort((x, y) => x.rank - y.rank));
		OIerDb.schools.forEach(school => school.members = Array.from(new Set(school.members)));
	}

	OIerDb.init = async function () {
		let support_timing = console.time && console.timeEnd, succ = false;
		if (support_timing) console.time('预处理时长');
		try {
			await OIerDb.update();
			OIerDb.frontend_process();
			succ = true;
		} catch (e) {
			console.log(`预处理失败，原因：${e.message}`);
		} finally {
			if (support_timing) console.timeEnd('预处理时长');
		}
		return succ;
	}

	Object.defineProperty(OIerDb, 'predicate', {
		enumerable: true,
		get: () => pred,
		set: f => {
			if (typeof f !== 'function' || f.length !== 0) {
				throw Error('OIerDb.predicate 应为函数');
			}
			pred = f;
		}
	});

	if (localStorage.oierdb_predicate) {
		try {
			OIerDb.predicate = new Function(localStorage.oierdb_predicate);
		} catch (e) {
		}
	}

	Object.defineProperty(globalThis, 'OIerDb', {enumerable: true, value: OIerDb});
})();
