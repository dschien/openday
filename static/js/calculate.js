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
	data.addRows([['Servers', e_serv], ['Internet', e_network], ['Access Network', e_acc_net], ['User Device', e_user]]);

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

function addSelectionToSession(selection) {

	if( typeof selections === 'undefined') {
		// variable is undefined
		selections = new Array()
	}
	selections.push(selection)

	var form = document.getElementById('postForm')

	if(!form) {
		// this is not the survey mode - don't store interaction
		return;
	}
	// add the selection to the form

}

function calc() {

	var selection = {}

	// duration
	var durationMins = document.getElementById('duration')
	var durationSecs = 60

	// power user device
	if(durationMins.value != "")
		durationSecs = durationMins.value * 60
	selection['duration'] = durationMins.value
	var deviceType = document.getElementById('device_selected').value

	String.prototype.trim = function() {
		return this.replace(/^\s\s*/, '').replace(/\s\s*$/, '');
	};
	deviceType = deviceType.trim()
	selection['device'] = deviceType

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
	selection['service'] = serviceType

	// default for text
	var dataVolume = 1800000

	if(serviceType == 'video') {
		// average for video
		dataVolume = durationSecs * 450000
	}

	// power access network
	var connectionType = document.getElementById('connection_selected').value
	connectionType = connectionType.trim()
	selection['connection'] = connectionType
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
	var e_total_joule = e_serv + e_network + e_acc_net + e_user
	// convert to watthour
	e_total = e_total_joule / 3600
	e_total = Math.round(e_total * 100) / 100
	// update the page to show the results
	document.getElementById('bignr').innerHTML = "<h1><big>" + e_total + "</big> Wh</h1>"
	// create percentages
	var p_user = (e_user * 100) / e_total_joule
	var p_network = (e_network * 100) / e_total_joule
	var p_serv = (e_serv * 100) / e_total_joule
	var p_acc_net = (e_acc_net * 100) / e_total_joule
	// create circles
	var max_size=8000
	var circle_user= Math.round(Math.sqrt(max_size*(e_user/3600)/3.1416))
	margin = (100-circle_user)/2
	margintop = (100-circle_user)/3
	document.getElementById('circle_device').innerHTML = '<div style="width:'+circle_user+'px; height:'+circle_user+'px;margin-left:'+margin+'px;margin-top:'+margintop+'px; background:#C7E2EC; -moz-border-radius: 150px; -webkit-border-radius:150px;"></div>'
	document.getElementById('text_device').innerHTML = "<h2>" + deviceType + "</h2><p>" + Math.round(e_user / 36) / 100 + " Wh</p><p> " + Math.round(p_user) + " &#37;</p>"
	
	var circle_network= Math.round(Math.sqrt(max_size*(e_network/3600)/3.1416))
	margin = (100-circle_network)/2
	margintop = (100-circle_network)/3
	document.getElementById('circle_infra').innerHTML = '<div style="width:'+circle_network+'px; height:'+circle_network+'px; margin-left:'+margin+'px;margin-top:'+margintop+'px; background:#51A1B7; -moz-border-radius: 80px; -webkit-border-radius:80px;"></div>'
	document.getElementById('text_infra').innerHTML = "<h2>Internet infrastructure</h2><p>" + Math.round(e_network / 36) / 100 + " Wh</p>"
	
	var circle_serv= Math.round(Math.sqrt(max_size*(e_serv/3600)/3.1416))
	margin = (100-circle_serv)/2
	margintop = (100-circle_serv)/3
	document.getElementById('circle_server').innerHTML = '<div style="width:'+circle_serv+'px; height:'+circle_serv+'px;margin-left:'+margin+'px;margin-top:'+margintop+'px; background:#4998CE; -moz-border-radius: 80px; -webkit-border-radius:80px;"></div>'
	document.getElementById('text_server').innerHTML = "<h2>Servers</h2><p>" + Math.round(e_serv / 36) / 100 + " Wh</p>"
	
	var circle_acc_net= Math.round(Math.sqrt(max_size*(e_acc_net/3600)/3.1416))
	margin = (100-circle_acc_net)/2
	margintop = (100-circle_acc_net)/3
	document.getElementById('circle_access').innerHTML = '<div style="width:'+circle_acc_net+'px; height:'+circle_acc_net+'px;margin-left:'+margin+'px;margin-top:'+margintop+'px; background:#A3C3D8; -moz-border-radius: 40px; -webkit-border-radius:80px;"></div>'
	document.getElementById('text_access').innerHTML =  "<h2>" + connectionType + " connection</h2><p>" + Math.round(e_acc_net / 36) / 100 + " Wh</p>"

	//drawChart(e_serv, e_network, e_acc_net, e_user)
	calcLightBulbsAndCarbon(e_total_joule, durationSecs)
	currentSelection = selection
	addSelectionToSession(selection)
	setBlurb()
}

function calcLightBulbsAndCarbon(e_total_joule, durationSecs) {
	// 	to kWh
	e_total_Wh = e_total_joule / 3600
	e_total_kWh = e_total_Wh / 1000
	carbon = .53 * e_total_Wh
	$("div#carbon").text(Math.round(carbon * 10) / 10 + " gCO2-eq");
	power_lightBulb = 11
	lightBulbs = e_total_joule / (power_lightBulb * durationSecs )
	$("div#lightBulb").text(Math.round(lightBulbs * 100) / 100 + " 11W light bulbs for " + durationSecs / 60 + " minutes");

	// kg per km
	carEmissions = 0.20864
	$("div#carMeters").text(Math.round((carbon / carEmissions ) * 10) / 10 + " meter driving an average petrol car");
}

function setBlurb() {
	text = '<p>Reading normal web pages (no video) changing page every minute'
	if(currentSelection['service'] == 'video')
		text = '<p>Watching video continuously '
	switch(currentSelection['device']) {
		case 'phone':
			text = text + "using a mobile phone "
			break;
		case 'tablet':
			text = text + "using a tablet such as iPad "
			break;
		case 'pc':
			text = text + "using a desktop computer "
			break;
		default:
			// default is laptop
			text = text + "using a laptop computer "
	}

	if(currentSelection['connection'] == 'mobile') {
		text = text + "connected to the Internet by a mobile networks (GPRS, 3G, etc.) "
	} else {
		text = text + "connected to the Internet by domestic broadband modem and WiFi router "
	}

	if(currentSelection['service'] == 'video') {
		text = text + "viewing for " + currentSelection['duration'] + " minutes"
	} else {
		text = text + "reading for " + currentSelection['duration'] + " minutes"
	}
	text = text + "</p>"
	document.getElementById('blurb').innerHTML = text

}