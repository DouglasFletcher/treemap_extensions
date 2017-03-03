
// Douglas Fletcher
// 2016.06.08

/// ================
/// global variables
/// ================

// define positions
var margin = {
		top: 30,
		right: 10,
		bottom: 10,
		left: 10
	},
	width = 760 - margin.left - margin.right,
	height = 580 - margin.top - margin.bottom;

// tooltip init
var tip = d3.tip()
	.attr('class', 'd3-tip')
	.offset([-10, 0])
	.html(function(d) {
		return "<p><strong>Investment:</strong> <span style='color:red'>" + d.name + "</span></p>"
		+ "<p><strong>Conversions:</strong> <span style='color:red'>" + (Math.round(d.value * 10) / 10).toLocaleString('de-DE') + "</span></p>"
		;
	});


/// =============================================
/// __main__ to create graph based on user inputs
/// =============================================

/// ===========
/// user inputs
/// ===========

// set default values for graph
var recordtype = $("#RecordType").val();
var grouplevel = $("#grouplevel").val();

d3.json("json/treemap_contribs_test.json", function(error, jsonin) {
	if (error) throw error;

	/// ============
	/// create graph
	/// ============
	// populate graph with default values
	var filteredData = getdata(recordtype, grouplevel, jsonin);
	// append node elements to graph
	buildGraph(filteredData);

	/// ============
	/// update graph
	/// ============

	// record type update
	d3.selectAll("#RecordType").on("change", function change() {
		// get record level
		recordtype = this.value;
		// get new data
		var filteredData = getdata(recordtype, grouplevel, jsonin);
		// create new diagram
		buildGraph(filteredData);
	});

	// group level update
	d3.selectAll("#grouplevel").on("change", function change() {
		// get group level
		grouplevel = this.value;
		// get new data
		filteredData = getdata(recordtype, grouplevel, jsonin);
		// update diagram
		buildGraph(filteredData);
	});

	d3.selectAll("#attribmethod").on("change", function change() {
		// get attribute type
		attribmethod = this.value;
		// get new data
		filteredData = getdata(recordtype, grouplevel, jsonin);
		// update diagram
		//smoothTransition(filteredData);
		buildGraph(filteredData);
	});

});

/// ======================
/// all relevant functions
/// ======================


var setswitch = function(method){
	//=========================================
	//== purpose: get form input to filter data
	//== input: form inputs 
	//== output: data
	// NEED TO UPDATE WITH DATA VALUES
	//=========================================
	if (method == "method1"){
		var funcVal = function(d){return d.value.method1;}; 
	}
	if (method == "method2"){
		var funcVal = function(d){return d.value.method2;}; 
	}
	return funcVal;
}


function getdata(recordtype, grouplevel, jsonin) {
	//====================================
	//== purpose: get relavant data
	//== input: 1) form inputs, 
	//== 		2) original json in format
	//== 		processed from python file
	//== output: json data for d3 treemap
	//== (check it out with JSON.stringify)
	//====================================
	var filteredData = []
	// filter original data
	var successfilter = jsonin.children.filter(function (row) {
		// filter group type
		if(row.name[1] == grouplevel & row.name[0] == recordtype) {
			childfilter = []
			row.children.map(function (childrow){
				childfilter.push({"name": childrow.name, "value": childrow.value})
			})
			// collect data
			filteredData.push({"name": row.name[2], "children": childfilter});
		}
	});
	var outdata = {"name": "inputdata", "children": filteredData};
	console.log(JSON.stringify(outdata));
	return outdata;
};


function buildGraph(filteredData) {
	//====================================
	//== purpose: create plots for diagram
	//== success type & meta level buttons
	//== input: a) requred data
	//== output: creates diagrams
	//====================================

	// start with clean slate
	d3.select("body").select("#diagram").remove()

	// attrib method default
	var attribmethod = $("#attribmethod").val();

	// set value default
	var setvalue = setswitch(attribmethod);

	// tree map object
	var treemap = d3.layout.treemap()
		.size([width, height])
		.sticky(true)
		.value(function(d) {
			return d.value;
		});

	// add parent graph svg element
	var svg = d3.select("body").append("svg")
		.style("position", "relative")
		.style("width", (width + margin.left + margin.right) + "px")
		.style("height", (height + margin.top + margin.bottom) + "px")
		.style("left", margin.left + "px")
		.style("top", margin.top + "px")
		.attr("id", "diagram");

	// call tip method on svg
	svg.call(tip)

	// append group elements: for rect ?? text as well or text box sufficient?
	var gvals = svg.datum(filteredData).selectAll("g")
		.data(treemap.value(setvalue).nodes)
		.enter()
			.append("g")
			.attr("class", "node")
			.attr("id", setclass)
			.attr("transform", translateinit);

	// append rectangles
	gvals.append("rect")
		.call(objectSize)
		.on("mouseover", tip.show)
		.on("mouseout", tip.hide)
		.style("fill", setcolor)
		.style("fill-opacity", setfillopacity)
		.style("stroke-opacity", "1px")
		.style("stroke", setstroke)
		.style("stroke-width", setstrokewidth);

};


function smoothTransition(filteredData){
	//====================================
	//== purpose: create plots for diagram
	//== with transitioning/phasing
	//== attribution type button
	//== input: a) required data
	//== output: creates diagrams
	//====================================

	// attrib method default
	var attribmethod = $("#attribmethod").val();

	// set value default
	var setvalue = setswitch(attribmethod);

	// set value default

	// __init__ treemap
	var treemap = d3.layout.treemap()
		.size([width, height])
		.sticky(false)
		.value(function(d) {
			return d.value;
		});

	// get existing elements
	var gvals = d3.select("#diagram").datum(filteredData).selectAll("#node")
		.data(treemap.value(setvalue).nodes)
		.enter()
			.center(0, 0)
			.translate()

	var gvals = d3.select("#diagram").datum(filteredData).selectAll("rect");

	/*
	gvals
		.data(treemap.value(setvalue).nodes);

		.call(objectSize);

	// update existing
	selectgs
		.style("background", setcolor)
		.on("mouseover", tip.show)
		.on("mouseout", tip.hide)
		.attr("class", "node")
		.attr("id", setclass)
		.attr("transform", translateval);
	*/

};

///////////////////////
// css return functions
///////////////////////

var channelFlag = function (d){
	//==========================================
	//== purpose: return flag for dimension type
	//== input: dimension variable
	//== output: 1 or 0
	//== THIS FUNCTION NEEDS TO BE UPDATED
	//== ACCORDING TO YOUR INPUTS
	//====================================
	if (d.name == "Action01"){
		return 1;
	}
	else if (d.name == "Action02"){
		return 2;
	}
	else if (d.name == "Action03"){
		return 3;
	}
	else if (d.name == "Action04"){
		return 4;
	}
	else if (d.name == "Action05"){
		return 5;
	}
	else{
		return 0;
	}
}



var setstroke = function(d){
	// set rectangle properties
	var channelflag = channelFlag(d);
	if (channelflag == 0){
		return "white";		
	}
}


var setstrokewidth = function(d){
	// set rectangle properties
	var channelflag = channelFlag(d);
	if (channelflag == 0){
		return "1.2px";
	} else {
		return "0px";
	}
}


var setfillopacity = function(d){
	// set opacity
	var channelflag = channelFlag(d);
	if (channelflag > 0 && channelflag < 5){
		return 1;
	} else {
		return 0;
	}
};

var setcolor = function(d){
	// set color
	var channelflag = channelFlag(d);
	if (channelflag == 1){
		return "#d62728";
	} 
	else if (channelflag == 2){
		return "#ff7f0e";
	}
	else if (channelflag == 3){
		return "#9467bd";
	}
	else if (channelflag == 4){
		return "#8c564b";
	}
	else{
		return null;
	}
};

var setnames = function(d){
	// set name
	var channelflag = channelFlag(d);
	if (channelflag == 0){
		return d;
	}
	else {
		return "";
	}
};

var setclass = function(d){
	// set class
	var channelflag = channelFlag(d);
	if (channelflag == 0){
		return "node";
	}
	else {
		return "parentnode";
	}
};


var translateinit = function(d){
	// translate position
	return "translate(" + d.x + "," + d.y +")";
};

var translatemove = function(d){
	// translate position
	return "translate(" + d.x + "," + d.y +")";
};



function objectSize() {
	//==============================
	//== purpose: update size values
	//== output: size attributes
	//==============================
	this
		.style("width", function(d) { return Math.max(0, d.dx - 1) + "px"; })
		.style("height", function(d) { return Math.max(0, d.dy - 1) + "px"; })
}


//===============
//== other stuff
//===============

// append text
/*
gvals.append("text")
	.call(objectSize)
	.on("mouseover", tip.show)
	.on("mouseout", tip.hide)
	.text(setnames);

var node = svg.datum(filteredData).selectAll(".node")
	.append("g")
		.append("rect")

svg.datum(filteredData).selectAll("g")
	.data(treemap.value(setvalue).nodes)
	.enter()
	.append("text").text(setnames)
		.call(position);
*/


	//d3.selectAll("g")

			//.style("opacity", 0);
			//.text(setnames)
			//.style("color", "white");
