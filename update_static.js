#!/usr/bin/env node

const fs = require('fs');

let output = {};

fs.readdirSync('model/static').filter(fn => fn.endsWith('.json')).map(fn => {
	let name = fn.substr(0, fn.length - 5), content = fs.readFileSync(`model/static/${fn}`, {encoding: 'utf-8'});
	output[name] = {
		enumerable: true,
		value: JSON.parse(content),
		writable: true
	}
});

let schools = [];
output.schools = {enumerable: true, value: schools, writable: true};
fs.readFileSync('model/data/school.txt', {encoding: 'utf-8'}).split('\n').forEach(line => {
	let fields = line.split(',');
	if (fields.length > 2) {
		let [province, city, name] = fields;
		schools.push([name, province, city]);
	}
});

fs.writeFileSync('js/oierdb_static.js', `Object.defineProperties(OIerDb,${JSON.stringify(output)});\n`);
