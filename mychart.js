var config = {
	type: 'line',
	data: {
		labels: ['2010', '2011', '2012', '2013', '2014', '2015', '2016'],
		datasets: [{
			label: 'My First dataset',
			backgroundColor: "#ee961b",
			borderColor: "#ee961b",
			data: [
				1,3,0,0,2,4,3
			],
			fill: false,
		}, {
			label: 'My Second dataset',
			fill: false,
			backgroundColor: "#939291",
			borderColor: "#939291",
			data: [
				4,1,0,0,6,2,5
			],
		},{
			label: 'My Second dataset',
			fill: false,
			backgroundColor: "#9c593b",
			borderColor: "#9c593b",
			data: [
				1,2,3,4,6,7,9
			],
		}]
	},
	options: {
		maintainAspectRatio: false,
		title: {
			display: true,
			text: 'Chart.js Line Chart'
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

window.onload = function() {
	var ctx = document.getElementById('canvas').getContext('2d');
	window.myLine = new Chart(ctx, config);
};
