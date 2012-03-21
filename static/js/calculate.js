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
	
	if (!selections){
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
	var p_user = (e_user*100)/e_total
	var p_network = (e_network*100)e_total
	var p_serv = (e_serv*100)/e_total
	var p_acc_net = (e_acc_net*100)/e_total
	// create circles
	var max_size=30
	var circle_user= Math.round(Math.sqrt(max_size*e_user/3.1416))
	document.getElementById('circle1').innerHTML = '<div style="width:'+circle_user+'px; height:'+circle_user+'px;margin-left:0px;margin-top:0px; background:#000; -moz-border-radius: 40px; -webkit-border-radius:40px;"></div>'
	/*
	var size = round(sqrt($max*$impactAssessment['amount']/pi()));
	if ($size > 82) { $size = 82;}
	if ($size < 20) { $size = 20;}
	$margin = (100-$size)/2;
	$margintop = (100-$size)/3;
	// Create a circle
	echo '<div class="circle"></div>';
	echo '<div class="nr"><h1 class="nr">' . round($impactAssessment['amount'],2) .' '. $impactAssessment['unit']["abbr"] .'</h1></div>';
	echo '<div class="meta"><p class="category">Category: <b>'. $impactAssessment['impactCategory']['label'] . "</b><br/>";
	echo 'Indicator: <b>'. $impactAssessment['impactCategoryIndicator']['label'] . "</b></p></div>";
	} } ?>

	*/
	// document.getElementById('details').innerHTML = "<p>Device (" + deviceType + "):" + e_user + " Wh</p>" + "<p>Server: " + e_serv + " Wh</p>" + "<p>Access network (" + connectionType + "):" + e_acc_net + " Wh</p>" + "<p>Network:" + e_network + " Wh</p>"
	document.getElementById('details').innerHTML = "<p>" + deviceType + ":" + Math.round(e_user / 36) / 100 + " Wh, "+ p_user+" &#37;</p>" + "<p>servers: " + Math.round(e_serv / 36) / 100 + " Wh</p>" + "<p>" + connectionType + ":" + Math.round(e_acc_net / 36) / 100 + " Wh</p>" + "<p>internet:" + Math.round(e_network / 36) / 100 + " Wh</p>"
	drawChart(e_serv, e_network, e_acc_net, e_user)
	calcLightBulbsAndCarbon(e_total_joule, durationSecs)

	
	addSelectionToSession(selection)
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
