//chart1=>
function chart1_createChart(){
	var chart1_byitem_names = [];
	var chart1_bt_item = [];
  
	if(chart1_val == '수출금액'){
		for(var i=0; i<data1_export.length; i++) {
			if(parseInt(data1_export[i]['기간']) == chart1_year_value){
				chart1_byitem_names.push(data1_export[i]['품목명'])
				chart1_bt_item.push(parseInt(data1_export[i]['수출금액']))
			}
		}
	}
	else if(chart1_val == '수입금액'){
		for(var i=0; i<data1_import.length; i++) {
			if(parseInt(data1_import[i]['기간']) == chart1_year_value){
				chart1_byitem_names.push(data1_import[i]['품목명'])
				chart1_bt_item.push(parseInt(data1_import[i]['수입금액']))
			}
		}
	}
	else{
		for(var i=0; i<data1_tradebalance.length; i++) {
			if(parseInt(data1_tradebalance[i]['기간']) == chart1_year_value){
				chart1_byitem_names.push(data1_tradebalance[i]['품목명'])
				chart1_bt_item.push(parseInt(data1_tradebalance[i]['무역수지']))
			}
		}
	}
	
  
	var chart1_config = {
	   type: 'pie',
	   data: {
		 labels: chart1_byitem_names,
		 datasets: [{
		  backgroundColor: ['rgb(255, 99, 99)', 'rgb(255, 161, 99)', 'rgb(255, 245, 99)', 'rgb(182, 255, 99)','rgb(99, 255, 125)','rgb(99, 245, 255)','rgb(115, 99, 255)','rgb(180, 99, 255)', 'rgb(255, 99, 190)','rgb(145, 83, 55)'],
		  borderWidth: 2,
		  data: chart1_bt_item
		 }],
	   },
	   options: {
		 cutoutPercentage: 30,
		 legend: {
		  position:'bottom',
		  padding:5, 
		  labels: {
			pointStyle:'circle',
			usePointStyle:true
		  }
		 }, 
		 responsive: true,
		 title: {
		  display: true,
		  text: '[ '+chart1_year_value+'년 ]'
		 },
		 tooltips: {
		  callbacks: {
			label: function(tooltipItem, data) {
			 let value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
			 value = value.toString();
			 value = value.split(/(?=(?:...)*$)/);
			 value = value.join(',');
			 value = data.labels[tooltipItem.index]+': '+value;
			 return value;
			}
		  },
		 },
	   }
	}
   return chart1_config;
  }
  
  function chart1_bt_clicked(chart1_bt_year, chart1_bt_id){
	document.getElementsByClassName("chart1_bt, chart1_bt_selected").item(0).className="chart1_bt";
	document.getElementById(chart1_bt_id).className = "chart1_bt, chart1_bt_selected";
	
	chart1_year_value=chart1_bt_year;
	document.getElementById("chart1_chartContainer").innerHTML = '&nbsp;';
	document.getElementById("chart1_chartContainer").innerHTML = '<canvas id="chart1"></canvas>';
	chart_canvas1 = document.getElementById("chart1").getContext("2d");
	chart1 = new Chart(chart_canvas1, chart1_createChart());
  }

  function chart1_bt2_clicked(chart1_bt_val, chart1_bt_id){
	document.getElementsByClassName("chart1_bt2, chart1_bt_selected").item(0).className="chart1_bt2";
	document.getElementById(chart1_bt_id).className = "chart1_bt2, chart1_bt_selected";
	
	chart1_val=chart1_bt_val;
	document.getElementById("chart1_chartContainer").innerHTML = '&nbsp;';
	document.getElementById("chart1_chartContainer").innerHTML = '<canvas id="chart1"></canvas>';
	chart_canvas1 = document.getElementById("chart1").getContext("2d");
	chart1 = new Chart(chart_canvas1, chart1_createChart());
  }
   //<=chart1

//chart2=>
function chart2_createChart(){
	var chart2_country_values = [];
	var chart2_amount_of_export_values = [];
	var chart2_Totalsum_of_amount = 0;

	for(var i=0; i<data2.length; i++) {
		if(parseInt(data2[i]['기간']) == chart2_year_value){
			chart2_country_values.push(data2[i]['국가명'])
			chart2_amount_of_export_values.push(parseInt(data2[i]['수출금액']))
			chart2_Totalsum_of_amount = parseInt(data2[i]['총수출금액'])
		}
	}

	var chart2_sum_of_amount = chart2_amount_of_export_values.reduce((a, b) => a + b);

	chart2_country_values.push('기타')
	chart2_amount_of_export_values.push(chart2_Totalsum_of_amount-chart2_sum_of_amount)

	var chart2_config = {
		type: 'pie',
		data: {
			labels: chart2_country_values,
			datasets: [{
				backgroundColor: ['rgb(255, 99, 99)', 'rgb(255, 161, 99)', 'rgb(255, 245, 99)', 'rgb(182, 255, 99)','rgb(99, 255, 125)','rgb(99, 245, 255)','rgb(115, 99, 255)','rgb(180, 99, 255)', 'rgb(255, 99, 190)','rgb(145, 83, 55)','rgb(151, 140, 151)'],
				borderWidth: 2,
				data: chart2_amount_of_export_values
			}]
		},
		options: {
			cutoutPercentage: 30,
			legend: {
				position:'bottom',
				padding:5, 
				labels: {
					pointStyle:'circle',
					usePointStyle:true
				}
			}, 
			responsive: true,
			title: {
				display: true,
				text: '[ '+chart2_year_value+'년 ]'
			},
			tooltips: {
				callbacks: {
					label: function(tooltipItem, data) {
						let value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
						value = value.toString();
						value = value.split(/(?=(?:...)*$)/);
						value = value.join(',');
						value = data.labels[tooltipItem.index]+': '+value;
						return value;
					}
				},
			},

		}
	}
	return chart2_config;
}

function chart2_bt_clicked(chart2_bt_year, chart2_bt_id){
    document.getElementsByClassName("chart2_bt, chart2_bt_selected").item(0).className="chart2_bt";
    document.getElementById(chart2_bt_id).className = "chart2_bt, chart2_bt_selected";

    chart2_year_value=chart2_bt_year;
    document.getElementById("chart2_chartContainer").innerHTML = '&nbsp;';
    document.getElementById("chart2_chartContainer").innerHTML = '<canvas id="chart2"></canvas>';
    chart_canvas2 = document.getElementById("chart2").getContext("2d");
    chart2 = new Chart(chart_canvas2, chart2_createChart());
}
//<=chart2


//chart3=>
function chart3_createChart(){
	if(chart3_country_value == '미국') var data3 = data3_usa;
	else if(chart3_country_value == '중국') var data3 = data3_china;
	else if(chart3_country_value == '일본') var data3 = data3_japan;
	else var data3 = data3_eu;

	var chart3_year_values = [];
	var chart3_total_amount_of_trade_values = [];
	var chart3_korea_amount_of_trade_values = [];
	var chart3_trade_weight = [];
	var chart3_total_amount_of_import_values = [];
	var chart3_korea_amount_of_import_values = [];
	var chart3_import_weight = [];
	var chart3_total_amount_of_export_values = [];
	var chart3_korea_amount_of_export_values = [];
	var chart3_export_weight = [];

	for(var i=0; i<data3.length; i++) {
		chart3_year_values.push(data3[i]['연도'])
		chart3_total_amount_of_trade_values.push(parseInt(data3[i]['총무역금액']))
		chart3_korea_amount_of_trade_values.push(parseInt(data3[i]['한국무역금액']))
		chart3_trade_weight.push(parseFloat(data3[i]['무역비중']))
		chart3_total_amount_of_import_values.push(parseInt(data3[i]['총수입금액']))
		chart3_korea_amount_of_import_values.push(parseInt(data3[i]['한국수입금액']))
		chart3_import_weight.push(parseFloat(data3[i]['수입비중']))
		chart3_total_amount_of_export_values.push(parseInt(data3[i]['총수출금액']))
		chart3_korea_amount_of_export_values.push(parseInt(data3[i]['한국수출금액']))
		chart3_export_weight.push(parseFloat(data3[i]['수출비중']))
	}

	var chart3_config = {
		type: 'bar',
		data: {
			labels: chart3_year_values,
			datasets: [{
				type: 'bar',
				label: '총무역금액',
				borderColor: "rgb(100, 207, 132)",
				backgroundColor: "rgba(100, 207, 132, 0.5)",
				yAxisID: 'A',
				data: chart3_total_amount_of_trade_values,
				fill: false,
				borderWidth: 2
			}, {
				type: 'bar',
				label: '한국무역금액',
				borderColor: "rgb(11, 206, 70)",
				backgroundColor: "rgba(11, 206, 70, 0.5)",
				yAxisID: 'A',
				data: chart3_korea_amount_of_trade_values,
				fill: false,
				borderWidth: 2
			}, {
				type: 'bar',
				label: '총수입금액',
				borderColor: "rgb(54, 162, 235)",
				backgroundColor: "rgba(54, 162, 235, 0.5)",
				yAxisID: 'A',
				data: chart3_total_amount_of_import_values,
				fill: false,
				borderWidth: 2
			}, {
				type: 'bar',
				label: '한국수입금액',
				borderColor: "rgb(4, 48, 241)",
				backgroundColor: "rgba(4, 48, 241, 0.5)",
				yAxisID: 'A',
				data: chart3_korea_amount_of_import_values,
				fill: false,
				borderWidth: 2
			}, {
				type: 'bar',
				label: '총수출금액',
				borderColor: "rgb(255, 99, 132)",
				backgroundColor: "rgba(255, 99, 132, 0.5)",
				yAxisID: 'A',
				data: chart3_total_amount_of_export_values,
				fill: false,
				borderWidth: 2
			}, {
				type: 'bar',
				label: '한국수출금액',
				borderColor: "rgb(248, 23, 71)",
				backgroundColor: "rgba(248, 23, 71, 0.5)",
				yAxisID: 'A',
				data: chart3_korea_amount_of_export_values,
				fill: false,
				borderWidth: 2
			}, {
				type: 'line',
				label: '무역비중',
				borderColor: "mediumseagreen",
				pointBackgroundColor: "mediumseagreen",
				yAxisID: 'B',
				data: chart3_trade_weight,
				fill: false,
				borderWidth: 2
			}, {
				type: 'line',
				label: '수입비중',
				borderColor: "mediumslateblue",
				pointBackgroundColor: "mediumslateblue",
				yAxisID: 'B',
				data: chart3_import_weight,
				fill: false,
				borderWidth: 2
			}, {
				type: 'line',
				label: '수출비중',
				borderColor: "indianred",
				pointBackgroundColor: "indianred",
				yAxisID: 'B',
				data: chart3_export_weight,
				fill: false,
				borderWidth: 2
			}]
		},
			options: {
				responsive: true,
				title: {
					display: true,
					text: '[ '+chart3_country_value+' ]'
				},
				legend: {
					position: 'bottom'
				},
				tooltips: {
					mode: 'index',
					intersect: false,
					callbacks: {
						label: function(tooltipItem, data) {
							let value = data.datasets[tooltipItem.datasetIndex].data[tooltipItem.index];
							if(value > 100){
								value = value.toString();
								value = value.split(/(?=(?:...)*$)/);
								value = value.join(',');
							}
							else value = tooltipItem.yLabel+'%';
							value = data.datasets[tooltipItem.datasetIndex].label+': '+value;
							return value;
						}
					}
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
							//labelString: 'x'
						},
					}],
					yAxes: [{
						id: 'A',
						type: 'linear',
						position: 'left',
						display: true,
						scaleLabel: {
							display: true,
							// labelString: 'y'
						},
						ticks: {
							beginAtZero: true,
							userCallback: function(value, index, values) {
								value = value.toString();
								value = value.split(/(?=(?:...)*$)/);
								value = value.join(',');
								return value;
							}
						}
					},{
						id: 'B',
						type: 'linear',
						position: 'right',
						display: true,
						scaleLabel: {
							display: true,
							// labelString: 'y'
						},
						ticks: {
							//max: 11,
							min: 0
						}
					}]
				}
			}
		}
	return chart3_config;
}

function chart3_bt_clicked(chart3_bt_country, chart3_bt_id){
    document.getElementsByClassName("chart3_bt, chart3_bt_selected").item(0).className="chart3_bt";
    document.getElementById(chart3_bt_id).className = "chart3_bt, chart3_bt_selected";

	chart3_country_value=chart3_bt_country;
	document.getElementById("chart3_Text").innerHTML = '&nbsp;';
	if(chart3_country_value == 'EU') document.getElementById("chart3_Text").innerHTML = '금액 단위: 백만€';
	else if (chart3_country_value == '일본') document.getElementById("chart3_Text").innerHTML = '금액 단위: 백만￥';
	else document.getElementById("chart3_Text").innerHTML = '금액 단위: 백만불';

    document.getElementById("chart3_chartContainer").innerHTML = '&nbsp;';
    document.getElementById("chart3_chartContainer").innerHTML = '<canvas id="chart3"></canvas>';
    chart_canvas3 = document.getElementById("chart3").getContext("2d");
    chart3 = new Chart(chart_canvas3, chart3_createChart());
}
//<=chart3


//chart4=>
var chart4_year_values = [];
var chart4_country_values = [];
var chart4_num_of_export_values = [];
var chart4_amount_of_export_values = [];

for(var i=0; i<data4.length; i++) {
	chart4_year_values.push(parseInt(data4[i]['기간']))
	chart4_country_values.push(data4[i]['국가명'])
	chart4_num_of_export_values.push(parseInt(data4[i]['수출건수']))
	chart4_amount_of_export_values.push(parseInt(data4[i]['수출금액']))
}

var chart4_config = {
	type: 'bar',
	data: {
		labels: chart4_country_values,
		datasets: [{
			label: '수출건수',
			borderColor: "rgb(54, 162, 235)",
 			backgroundColor: "rgba(54, 162, 235, 0.5)",
			data: chart4_num_of_export_values,
			fill: false,
			borderWidth: 2
		}, {
			label: '수출금액',
			borderColor: "rgb(255, 99, 132)",
			backgroundColor: "rgba(255, 99, 132, 0.5)",
			data: chart4_amount_of_export_values,
			fill: false,
			borderWidth: 2
		}]
	},
		options: {
			responsive: true,
			title: {
				display: true,
				text: 'Chart No.4'
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
						labelString: 'x'
					}
				}],
				yAxes: [{
					display: true,
					scaleLabel: {
						display: true,
						labelString: 'y'
					}
				}]
			}
	 	}
	}
//<=chart4



window.onload = function() {
	var chart_canvas1 = document.getElementById("chart1").getContext("2d");
    var chart = new Chart(chart_canvas1, chart1_createChart());

    var chart_canvas2 = document.getElementById("chart2").getContext("2d");
	var chart2 = new Chart(chart_canvas2, chart2_createChart());

    var chart_canvas3 = document.getElementById("chart3").getContext("2d");
    var chart3 = new Chart(chart_canvas3, chart3_createChart());

    var chart_canvas4 = document.getElementById("chart4").getContext("2d");
    var chart4 = new Chart(chart_canvas4, chart4_config);
};
