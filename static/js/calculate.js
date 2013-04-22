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

function submitSelections() {

	var selectionsField = document.getElementById('selections')
	// are we in non-survey mode?
	if(selectionsField == null) {
		return;
	}
	if( typeof selectionsArr === 'undefined') {
		// variable is undefined  - no interactions, previously
		return;
	}
	
	selectionsField.value = JSON.stringify(selectionsArr)
}

function addSelectionToSession() {
	if( typeof selectionsArr === 'undefined') {
		// variable is undefined
		selectionsArr = new Array()
	}
	selectionsArr.push(currentSelection)
}

String.prototype.capitalize = function() {
   	return this.charAt(0).toUpperCase() + this.slice(1);
}


function calc() {

	
	var selection = {}

	// duration
	var durationMinsUI = document.getElementById('duration')
	var durationSecs = 60

	// power user device
	if(durationMinsUI.value != "") {
		durationMins = durationMinsUI.value
		durationSecs = durationMins * 60
	}

	selection['duration'] = durationMins
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
			p_device = 115
			deviceType = 'PC'
			break;
		default:
			// default is laptop
			p_device = 32
	}

	// service type
	var serviceType = document.getElementById('service_selected').value
	serviceType = serviceType.trim()
	selection['service'] = 'W'
	
	// default for text
	var dataVolume = 8000000

	// change page every minute
	pageLoads = durationMins
	if(serviceType == 'video') {
		// average for video
		dataVolume = durationSecs * 1100000
		// when watching video =- only one page
		pageLoads = 1
		p_device = p_device * 1.15	
		selection['service'] = 'V'
	}

	// power access network
	var connectionType = document.getElementById('connection_selected').value
	connectionType = connectionType.trim()
	selection['connection'] = 'W'
	var e_origin_per_request = 306 
	var e_origin = e_origin_per_request * pageLoads
	var e_3rdp = 6.9E-006 * dataVolume * pageLoads
	var e_serv = e_3rdp + e_origin
	// 0.000045 J/b = 0.1 kWh/GB
	var e_network = 0.000045 * dataVolume * pageLoads 

	var e_acc_net = 0
	switch(connectionType) {
		case '3G mobile':
			e_acc_net = dataVolume * 4.55e-05 * pageLoads
			selection['connection'] = 'M'
			break;
		default:
			// default is wifi
			e_acc_net = 10 * durationSecs
	}
	
	var e_user = p_device * durationSecs
	var e_total_joule = e_serv + e_network + e_acc_net + e_user

	// convert to watthour
	e_total = e_total_joule / 3600
	e_total = Math.round(e_total * 100) / 100

	// update the page to show the results
	document.getElementById('bignr').innerHTML = "<h1><big>" + e_total + "</big><br/> watt hours</h1>"

	// calc percentages
	var p_user = (e_user * 100) / e_total_joule
	var p_network = (e_network * 100) / e_total_joule
	var p_serv = (e_serv * 100) / e_total_joule
	var p_acc_net = (e_acc_net * 100) / e_total_joule

	switch(connectionType) {
		case '3G mobile':
			var e_internet = e_network + e_serv + e_acc_net
			var p_internet = (e_internet * 100) / e_total_joule
			break;
		default:
			var e_internet = e_network + e_serv
			var p_internet = (e_internet * 100) / e_total_joule		
	}	
		

	// create circles
	var max_size = 8000	
	switch(connectionType) {
		case '3G mobile':
	
			var circle_user = Math.round(Math.sqrt(max_size * (e_user / 3600) / 3.1416))
			margin = (100 - circle_user) / 2
			margintop = (100 - circle_user) / 3
			document.getElementById('circle_device').innerHTML = '<div style="width:' + circle_user + 'px; height:' + circle_user + 'px;margin-left:' + margin + 'px;margin-top:' + margintop + 'px; background:#C7E2EC; border-radius:400px; -moz-border-radius:400px;"></div>'
			document.getElementById('text_device').innerHTML = "<h2>" + deviceType.capitalize() + "<br/><br/></h2><p>" + Math.round(e_user / 36) / 100 + " Wh</p><p> " + Math.round(p_user) + " &#37;</p>"


			var circle_internet = Math.round(Math.sqrt(max_size * (e_internet / 3600) / 3.1416))
			margin = (100 - circle_internet) / 2
			margintop = (100 - circle_internet) / 3
			document.getElementById('circle_infra').innerHTML = '<div style="width:' + circle_internet + 'px; height:' + circle_internet + 'px; margin-left:' + margin + 'px;margin-top:' + margintop + 'px; background:#51A1B7; border-radius:300px; -moz-border-radius:300px;"></div>'
			document.getElementById('text_infra').innerHTML = "<h2>Internet   <br/><br/></h2><p>" + Math.round(e_internet / 36) / 100 + " Wh</p><p> " + Math.round(p_internet) + " &#37;</p>"

			document.getElementById('circle_access').innerHTML = '<div> </div>'
			document.getElementById('text_access').innerHTML = "<h2></h2>"


			break;
		default:
		
		var circle_user = Math.round(Math.sqrt(max_size * (e_user / 3600) / 3.1416))
		margin = (100 - circle_user) / 2
		margintop = (100 - circle_user) / 3
		document.getElementById('circle_device').innerHTML = '<div style="width:' + circle_user + 'px; height:' + circle_user + 'px;margin-left:' + margin + 'px;margin-top:' + margintop + 'px; background:#C7E2EC; border-radius:400px; -moz-border-radius:400px;"></div>'
		document.getElementById('text_device').innerHTML = "<h2>" + deviceType.capitalize() + "<br/><br/></h2><p>" + Math.round(e_user / 36) / 100 + " Wh</p><p> " + Math.round(p_user) + " &#37;</p>"
		
		var circle_acc_net = Math.round(Math.sqrt(max_size * (e_acc_net / 3600) / 3.1416))
		margin = (100 - circle_acc_net) / 2
		margintop = (100 - circle_acc_net) / 3
		
		document.getElementById('circle_access').innerHTML = '<div style="width:' + circle_acc_net + 'px; height:' + circle_acc_net + 'px;margin-left:' + margin + 'px;margin-top:' + margintop + 'px; background:#A3C3D8; border-radius:300px; -moz-border-radius:300px;"></div>'
		document.getElementById('text_access').innerHTML = "<h2>Home WiFi<br/><br/></h2><p>" + Math.round(e_acc_net / 36) / 100 + " Wh</p><p> " + Math.round(p_acc_net) + " &#37;</p>"

		var circle_internet = Math.round(Math.sqrt(max_size * (e_internet / 3600) / 3.1416))
		margin = (100 - circle_internet) / 2
		margintop = (100 - circle_internet) / 3
		document.getElementById('circle_infra').innerHTML = '<div style="width:' + circle_internet + 'px; height:' + circle_internet + 'px; margin-left:' + margin + 'px;margin-top:' + margintop + 'px; background:#51A1B7; border-radius:300px; -moz-border-radius:300px;"></div>'
		document.getElementById('text_infra').innerHTML = "<h2>Internet<br/><br/></h2></h2><p>" + Math.round(e_internet / 36) / 100 + " Wh</p><p> " + Math.round(p_internet) + " &#37;</p>"
	
		
	
	}
	if(connectionType == "3G mobile"){
		connectionType = "3G mobile connection"
	}



	//drawChart(e_serv, e_network, e_acc_net, e_user)
	calcLightBulbsAndCarbon(e_total_joule, durationSecs)
	currentSelection = selection
	setBlurb()
}

function calcLightBulbsAndCarbon(e_total_joule, durationSecs) {
	// 	to kWh
	e_total_Wh = e_total_joule / 3600
	e_total_kWh = e_total_Wh / 1000
	carbon = .525 * e_total_Wh
	document.getElementById('carbon').innerHTML = "<p><number>" + Math.round(carbon * 10) / 10 + "</number></p><p> grams carbon dioxide</p>";
	power_lightBulb = 11
	lightBulbs = e_total_joule / (power_lightBulb * durationSecs )
	document.getElementById('lightBulb').innerHTML = "<p><number>" + Math.round(lightBulbs) + "</number></p><p> 11W light bulbs for <number>" + durationSecs / 60 + " </number>minutes</p>";

	// kg per km
	carEmissions = 0.20864
	document.getElementById('carMeters').innerHTML = "<p><number>" + Math.round((carbon / carEmissions ) * 10) / 10 + "</number></p><p> meters driving an average petrol car</p>";
}

function setBlurb() {
	text = '<p>Reading normal web pages (no video) changing page every minute '
	if(currentSelection['service'] == 'V')
		text = '<p>Watching video continuously '
	switch(currentSelection['device']) {
		case 'phone':
			text = text + "using a mobile phone "
			break;
		case 'tablet':
			text = text + "using a tablet such as an iPad "
			break;
		case 'pc':
			text = text + "using a desktop computer "
			break;
		default:
			// default is laptop
			text = text + "using a laptop computer "
	}

	if(currentSelection['connection'] == 'M') {
		text = text + "connected to the Internet by a mobile network (GPRS, 3G, etc.) "
	} else {
		text = text + "connected to the Internet by domestic broadband modem and WiFi router "
	}

	if(currentSelection['service'] == 'V') {
		text = text + "viewing for " + currentSelection['duration'] + " minutes"
	} else {
		text = text + "reading for " + currentSelection['duration'] + " minutes"
	}
	text = text + "</p>"
	document.getElementById('blurb').innerHTML = text

}
