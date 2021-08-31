(() => {
	'use strict';

	let OIerDb = Object.create(null), pred = () => true, first_init = true;
	Object.defineProperty(globalThis, 'OIerDb', {enumerable: true, value: OIerDb});

	if (!globalThis || !globalThis.indexedDB) {
		document.addEventListener('DOMContentLoaded', () => {
			document.getElementById('content').innerHTML = '<h3 class="ui dividing header">请更新浏览器</h3><p>非常抱歉，您的浏览器不支持 <code>indexedDB</code>。请<a href="https://www.google.cn/chrome/" target="_blank">升级至最新版浏览器</a>查看😅</h3>';
		});
		return;
	}

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
		this.contestants = [];
		this.level_counts = {};
	}

	OIerDb.Contest.prototype.school_year = function () {
		return this.year - !this.fall_semester;
	}

	OIerDb.Contest.prototype.n_contestants = function () {
		return this.capacity ? this.capacity : this.contestants.length;
	}

	function __builtin_add_contestant(contest, record) {
		contest.contestants.push(record);
		if (!(record.level in contest.level_counts)) {
			contest.level_counts[record.level] = 0;
		}
		++contest.level_counts[record.level];
	}

	async function fetch_raw_data() {
		return (await fetch('/oierdb-ng/data/result')).text();
	}

	async function version_check() {
		let digest = localStorage.data_sha512;
		let upstream = await (await fetch('/oierdb-ng/data-sha512')).text();
		if (digest === upstream) {
			return true;
		}
		let response = await fetch_raw_data();
		localStorage.data_sha512 = upstream;
		return response;
	}

	async function load_from_indexDB() {
		return new Promise((fulfill, reject) => {
			let request = indexedDB.open('OIerDb');
			request.onerror = reject;
			request.onsuccess = () => fulfill(request.result);
			request.onupgradeneeded = reject;
		}).then(db => {
			let os = db.transaction('main').objectStore('main'), data = {};
			return new Promise((fulfill, reject) => {
				let request = os.get('oiers');
				request.onerror = reject;
				request.onsuccess = () => {OIerDb.oiers = request.result; fulfill();}
			});
		});
	}

	async function save_to_indexDB() {
		return new Promise((fulfill, reject) => {
			let request = indexedDB.open('OIerDb');
			request.onerror = reject;
			request.onsuccess = () => fulfill(request.result);
			request.onupgradeneeded = () => {
				let db = request.result;
				if (!db.objectStoreNames.contains('main')) {
					db.createObjectStore('main');
				}
			}
		}).then(db => {
			let os = db.transaction('main', 'readwrite').objectStore('main');
			return new Promise((fulfill, reject) => {
				let request = os.put(OIerDb.oiers, 'oiers');
				request.onerror = reject;
				request.onsuccess = fulfill;
			});
		});
	}

	function link() {
		OIerDb.contests.forEach(contest => {contest.contestants = []; contest.level_counts = {};});
		OIerDb.schools.forEach(school => {school.members = []; school.records = [];});
		OIerDb.oiers.forEach(oier => {
			oier.provinces = Array.from(new Set(oier.records.map(record => record.province)));
			oier.records.forEach(record => {
				record.contest = OIerDb.contests[record.contest];
				record.school = OIerDb.schools[record.school];
				record.oier = oier;
				__builtin_add_contestant(record.contest, record);
				record.school.records.push(record);
				record.school.members.push(oier);
			});
		});
		OIerDb.contests.forEach(contest => contest.contestants.sort((x, y) => x.rank - y.rank));
		OIerDb.schools.forEach(school => school.members = Array.from(new Set(school.members)));
	}

	function text_to_raw(response) {
		let lines = response.split('\n'), data = [];
		for (let line of lines) {
			let fields = line.split(',');
			if (fields.length !== 9) continue;
			let [uid, initials, name, gender, enroll_middle, oierdb_score, ccf_score, ccf_level, compressed_records] = fields;
			let records = compressed_records.split('/').map(record => {
				let [contest, school, score, rank, province_id, award_level_id] = record.split(':');
				return {
					contest,
					school,
					...(score !== '' && {score: parseFloat(score)}),
					rank: parseInt(rank),
					province: province_id in OIerDb.provinces ? OIerDb.provinces[province_id] : province_id,
					level: award_level_id in OIerDb.award_levels ? OIerDb.award_levels[award_level_id] : award_level_id
				};
			});
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
				records,
			};
			data.push(oier);
		}
		OIerDb.oiers = data;
	}

	OIerDb.init = async function () {
		let support_timing = console.time && console.timeEnd;
		if (support_timing) console.time('预处理时长');
		if (first_init) {
			OIerDb.contests = OIerDb.contests.map((x, id) => new OIerDb.Contest(id, x));
			OIerDb.schools = OIerDb.schools.map((x, id) => ({id, name: x[0], province: x[1], city: x[2], members: [], records: []}));
			first_init = false;
		}
		try {
			let response = await version_check();
			if (response === true) {
				try {
					await load_from_indexDB();
					return link(), true;
				} catch (e1) {
					console.log(`旧数据受损，原因：${e1.message}，重新读取中...`);
					response = await fetch_raw_data();
				}
			}
			text_to_raw(response);
			await save_to_indexDB();
			return link(), true;
		} catch (e) {
			console.log(`预处理失败，原因：${e.message}`);
		} finally {
			if (support_timing) console.timeEnd('预处理时长');
		}
		return false;
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
})();
