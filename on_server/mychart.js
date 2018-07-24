/*var config = {
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
};*/
var config = {
    title: {
        text: '折线图堆叠',
        textStyle:{color:"#fff"}
    },
    tooltip: {
        trigger: 'axis'
    },
    legend: {
        data:['邮件营销','联盟广告','视频广告','直接访问','搜索引擎'],
        textStyle:{color:"#fff"}
    },
    grid: {
        left: '3%',
        right: '4%',
        bottom: '3%',
        containLabel: true,
        borderColor:"#fff"
    },
    toolbox: {
        feature: {
            saveAsImage: {}
        }
    },
    xAxis: {
        type: 'category',
        boundaryGap: false,
        data: ['周一','周二','周三','周四','周五','周六','周日']
    },
    yAxis: {
        type: 'value'
    },
    color: ["#ee961b","#939291","#9c593b"]
    ,
    series: [
        {
            name:'邮件营销',
            type:'line',
            stack: '总量',
            data:[120, 132, 101, 134, 90, 230, 210]
        },
        {
            name:'联盟广告',
            type:'line',
            stack: '总量',
            data:[220, 182, 191, 234, 290, 330, 310]
        },
        {
            name:'视频广告',
            type:'line',
            stack: '总量',
            data:[150, 232, 201, 154, 190, 330, 410]
        }
    ]
};


var model = [
	{
		label: '1=/Au',
		data: [0,0,0,0,0,0,0,0,0],fill: false,
	},{
		label: '2=/Ag',
		fill: false,
		data: [
			   0,0,0,0,0,0,0,0,0
			   ],
	},{
		label: '3=/Cu',
		fill: false,
		data: [
			   0,0,0,0,0,0,0,0,0
			   ],
	}
]

window.onload = function() {
	var myChart = echarts.init(document.getElementById('cht'));
	myChart.setOption(config);
};