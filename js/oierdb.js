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

	OIerDb.Contest = function (id, settings) {
		this.id = id;
		this.contestants = [];
		this.level_counts = {};
		for (let setting in settings) this[setting] = settings[setting];
	}

	OIerDb.Contest.prototype.school_year = function () {
		return this.year - !self.fall_semester;
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
		let digest = localStorage.data_sha512;
		let upstream = await (await fetch('/oierdb-ng/data-sha512')).text();
		if (digest !== upstream) {
			localStorage.data_sha512 = upstream;
			localStorage.data = await (await fetch('/oierdb-ng/data/result')).text();
		}
		OIerDb.compressed_data = localStorage.data;
		OIerDb.contests = OIerDb.contests.map((x, i) => new OIerDb.Contest(i, x));
		update_succ = true;
	}

	OIerDb.frontend_process = function () {
		if (!update_succ) {
			throw Error('请先调用 await OIerDb.update()');
		}
		let lines = OIerDb.compressed_data.split('\n'), rank = 0, data = [];
		for (let line of lines) {
			let fields = line.split(',');
			if (fields.length !== 9) continue;
			++rank;
			let [uid, initials, name, gender, enroll_middle, oierdb_score, ccf_score, ccf_level, compressed_records] = fields;
			let records = compressed_records.split('/').map(record => {
				let [contest_id, school_id, score, rank, province] = record.split(':');
				return {
					contest: OIerDb.contests[contest_id],
					school: OIerDb.schools[school_id],
					score: parseFloat(score),
					rank: parseInt(rank),
					level: 0, // TODO
					province
				};
			});
			let provinces = Array.from(new Set(records.map(record => record.province)));
			let oier = {uid, initials, name, gender, enroll_middle, oierdb_score, ccf_score, ccf_level, records, provinces};
			records.forEach(record => {record.oier = oier; record.contest.add_contestant(record)});
			data.push(oier);
		}
		OIerDb.data = data;
	}

	Object.defineProperty(globalThis, 'OIerDb', {enumerable: true, value: OIerDb});
})();
