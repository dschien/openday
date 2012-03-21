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

	function calc() {

		var textField = document.getElementById('amount')
		var duration = 60
		if(textField.value != "")
			duration = textField.value*60
		var deviceType = document.getElementById('device_selected').value
		var p_device = 0
		switch(deviceType) {
			case 'phone':
				p_device = 1
				break;
			case 'tablet':
				p_device = 3
				break;
			case 'laptop':
				p_device = 28
				break;
			case 'pc':
				p_device = 58
				break;
			default:
				// default is laptop
				p_device = 28
		}

		var connectionType = document.getElementById('connection_selected').value
		var e_acc_net = 0
		switch(connectionType) {
			case 'dsl':
				e_acc_net = 5 * duration
				break;
			case 'mobile':
				e_acc_net = 70
				break;
			default:
				// default is dsl
				e_acc_net = 5 * duration
		}

		var e_serv = 104
		var e_network = 6
		var e_user = p_device * duration
		var e_total = e_serv + e_network + e_acc_net + e_user
		// convert to watthour
		e_total *= 0.000277777778
		e_total = Math.round(e_total*100)/100
		document.getElementById('bignr').innerHTML = "<h1><big>"+ e_total +"</big> wh</h1>"
		document.getElementById('bignr').innerHTML = "<h1><big>"+ e_total +"</big> wh</h1>"
		drawChart(e_serv, e_network, e_acc_net, e_user)
		// alert('total energy :' + e_total)

	}