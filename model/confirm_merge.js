#!/usr/bin/env node

const fs = require('fs');

let hash = {}, schools = fs.readFileSync('data/school.txt', 'utf8').trim().split('\n');

for (let [idx, line] of schools.entries()) {
	line = line.trim();
	if (!line.length || line[0] === '#') continue;
	hash[line.split(',')[2]] = idx;
}
let n = schools.length;

let data = fs.readFileSync('data/merge_preview.txt', 'utf8').split('\n');

for (let line of data) {
	line = line.trim();
	if (!line.length || line[0] === '#') continue;
	let [cmd, ...data] = line.split(' ');
	switch (cmd) {
		case 'b': {
			let [name, origin] = data;
			let idx = hash[origin];
			console.assert(idx != null);
			schools[idx] += `,${name}`;
			break;
		}
		case 'f': {
			let [name, origin] = data;
			let idx = hash[origin];
			console.assert(idx != null);
			let segments = schools[idx].split(',');
			segments.splice(2, 0, name);
			schools[idx] = segments.join(',');
			break;
		}
		case 'c': {
			let [province, city, name] = data;
			schools.push(`${province},${city},${name}`);
			hash[name] = n++;
			break;
		}
	}
}

fs.writeFileSync('data/school_new.txt', schools.join('\n') + '\n', 'utf8');
