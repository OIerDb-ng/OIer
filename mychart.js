var config = {
	type: 'line',
	data: {
		labels: ['2010', '2011', '2012', '2013', '2014', '2015', '2016', '2017', '2018'],
		datasets: []
	},
	options: {
        responsive:true,
		maintainAspectRatio: false,
		title: {
			display: true,
			text: '历年获奖人数'
		},
		tooltips: {
			mode: 'index',
			intersect: false,
		},
		hover: {
			mode: 'nearest',
			intersect: true
		},
		scales: {
			xAxes: [{
				display: true,
				scaleLabel: {
					display: true,
					labelString: '年份'
				}
            }],
            yAxes: [{
                display: true,
				scaleLabel: {
                    display: true,
                    labelString: '获奖人数'
                }
            }]
		}
	}
};
var model = [
	{
		label: '1=/Au',
		backgroundColor: "#ee961b",
		borderColor: "#ee961b",
		data: [0,0,0,0,0,0,0,0,0],fill: false,
	},{
		label: '2=/Ag',
		fill: false,
		backgroundColor: "#939291",
		borderColor: "#939291",
		data: [
			   0,0,0,0,0,0,0,0,0
			   ],
	},{
		label: '3=/Cu',
		fill: false,
		backgroundColor: "#9c593b",
		borderColor: "#9c593b",
		data: [
			   0,0,0,0,0,0,0,0,0
			   ],
	}
]

window.onload = function() {
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, config);
};