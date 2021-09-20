#!/usr/bin/env node

const fs = require('fs');

let output = {};

fs.readdirSync('static').filter(fn => fn.endsWith('.json')).map(fn => {
	let name = fn.substr(0, fn.length - 5), content = fs.readFileSync(`static/${fn}`, {encoding: 'utf-8'});
	output[name] = {
		enumerable: true,
		value: JSON.parse(content),
		writable: true
	}
});

output.schools = {
	enumerable: true,
	value: JSON.parse(fs.readFileSync('data/school.json', {encoding: 'utf-8'})),
	writable: true
};

fs.writeFileSync('../js/oierdb_static.js', `Object.defineProperties(OIerDb,${JSON.stringify(output)});\n`);
fs.unlinkSync('data/school.json');
