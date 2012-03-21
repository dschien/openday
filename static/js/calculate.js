// Load the Visualization API and the piechart package.
google.load('visualization', '1.0', {
	'packages' : ['corechart']
});

// Set a callback to run when the Google Visualization API is loaded.
// google.setOnLoadCallback(drawChart);

// Callback that creates and populates a data table,
// instantiates the pie chart, passes in the data and
// draws it.

function drawChart(e_serv, e_network, e_acc_net, e_user) {

	// Create the data table.
	var data = new google.visualization.DataTable();
	data.addColumn('string', 'Component');
	data.addColumn('number', 'Energy');
	data.addRows([['Server', e_serv], ['Network', e_network], ['Access Network', e_acc_net], ['User Device', e_user]]);

	// Set chart options
	var options = {
		'title' : 'Energy of Components',
		'width' : 400,
		'height' : 300
	};

	// Instantiate and draw our chart, passing in some options.
	var chart = new google.visualization.PieChart(document.getElementById('chart_div'));
	chart.draw(data, options);
}

function saveSelectionToSession() {

}

function calc() {

	// duration
	var durationMins = document.getElementById('duration')
	var durationSecs = 60

	// power user device
	if(durationMins.value != "")
		durationSecs = durationMins.value * 60
	var deviceType = document.getElementById('device_selected').value
	String.prototype.trim = function() {
		return this.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
	};
	deviceType = deviceType.trim()

	var p_device = 0
	switch(deviceType) {
		case 'phone':
			p_device = 1
			break;
		case 'tablet':
			p_device = 3
			break;	
		case 'pc':
			p_device = 58
			break;
		default:
			// default is laptop
			p_device = 28
	}

	// service type
	var serviceType = document.getElementById('service_selected').value
	serviceType = serviceType.trim()
	// default for text
	var dataVolume = 1800000

	if(serviceType == 'video') {
		// average for video
		dataVolume = 57492000
	}

	// power access network
	var connectionType = document.getElementById('connection_selected').value
	connectionType = connectionType.trim()
	var e_acc_net = 0
	switch(connectionType) {
		case 'mobile':
			e_acc_net = dataVolume * 1.8144144197598379e-05
			break;

		default:
			// default is dsl
			e_acc_net = 10 * durationSecs
	}

	var e_origin = 102
	var e_3rdp = 5.3490346705157022e-06 * dataVolume
	var e_serv = e_3rdp + e_origin  
	var e_network = 5.8616855E-6 * dataVolume
	var e_user = p_device * durationSecs
	var e_total = e_serv + e_network + e_acc_net + e_user
	// convert to watthour
	e_total /= 3600
	e_total = Math.round(e_total * 100) / 100

	document.getElementById('bignr').innerHTML = "<h1><big>" + e_total + "</big> wh</h1>"
	drawChart(e_serv, e_network, e_acc_net, e_user)

	saveSelectionToSession()

}