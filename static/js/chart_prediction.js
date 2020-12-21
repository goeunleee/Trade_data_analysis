// 동적으로 색을 만드는 function
function dynamicColorGen() {
	let r = Math.floor(Math.random() * 255);
	let g = Math.floor(Math.random() * 255);
	let b = Math.floor(Math.random() * 255);

	return "rgb(" + r + "," + g + "," + b + ")";
}

function chart_prediction(json_data, predicted_data) {
	const columns = Object.keys(json_data);		// excel에서 columns에 해당 하는 값
	let labels = Object.values(json_data[columns[0]]);	// 첫번째 column에 해당하는 기간값
	labels[labels.length] = "예측값";
	
	// dataset을 동적으로 생성
	let datasets = [];
	for(let i=1; i<columns.length; i++) {
		color = dynamicColorGen();
	
		// 기존 데이터에 예측된 데이터 추가
		let data = Object.values(json_data[columns[i]]);
		data[data.length] = predicted_data[i-1]
	
		let dataset = {
			label: columns[i],
			data: data,
			borderColor: color,
			pointBackgroundColor: color,
			fill: false,
			borderWidth: 2,
		}
	
		datasets.push(dataset)
	}
		
	var config = {
		type: "line",
		data: {
			labels: labels,
			datasets: datasets
		},
		options: {
			responsive: true,
			tooltips: {
				mode: "index",
				intersect: false,
				callbacks: {
					label: function(tooltipItem, data) {
						return '$' + tooltipItem.yLabel.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
					}
				},
			},
			hover: {
				mode: "nearest",
				intersect: true,
			},
			scales: {
				xAxes: [{
					display: true,
				}],
				yAxes: [{
					display: true,
					ticks: {
						beginAtZero: true,
						callback: function(value, index, values) {
							if(parseInt(value) >= 1000){
								return '$' + value.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ',');
							} else {
								return '$' + value;
							}
						}
					}
				}]
			}
		}
	};

	document.getElementById("chart_wrapper").innerHTML = '<canvas id="predicted_chart"></canvas>';
	const predicted_chart_canvas = document.getElementById("predicted_chart").getContext("2d");
	const predicted_chart = new Chart(predicted_chart_canvas, config);
}
