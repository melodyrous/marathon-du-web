
//Jeux de données
var data = [
	// Article
	{"name" : "Article 1", "parent": "Mot clef 1"},
	{"name" : "Article 2", "parent": "Mot clef 1"},
	{"name" : "Article 3", "parent": "Mot clef 1"},
	{"name" : "Article 4", "parent": "Mot clef 2"},
	{"name" : "Article 5", "parent": "Mot clef 2"},
	{"name" : "Article 6", "parent": "Mot clef 2"},
	{"name" : "Article 7", "parent": "Mot clef 2"},
	{"name" : "Article 8", "parent": "Mot clef 3"},
	// Mot clef
	{"name" : "Mot clef 1", "parent": "Auteur 1"},
	{"name" : "Mot clef 2", "parent": "Auteur 3"},
	{"name" : "Mot clef 3", "parent": "Auteur 3"},
	// Auteur
	{"name" : "Auteur 1", "parent": "Type publication 2"},
	{"name" : "Auteur 2", "parent": "Type publication 5"},
	{"name" : "Auteur 3", "parent": "Type publication 5"},
	// Publication
	{"name" : "Type publication 1", "parent": "Revue 1"},
	{"name" : "Type publication 2", "parent": "Revue 1"},
	{"name" : "Type publication 3", "parent": "Revue 1"},
	{"name" : "Type publication 4", "parent": "Revue 2"},
	{"name" : "Type publication 5", "parent": "Revue 3"},
	// Revue
	{"name" : "Revue 1", "parent": "Champs 1"},
	{"name" : "Revue 2", "parent": "Champs 1"},
	{"name" : "Revue 3", "parent": "Champs 1"},
	{"name" : "Revue 4", "parent": "Champs 2"},
	{"name" : "Revue 5", "parent": "Champs 2"},
	{"name" : "Revue 6", "parent": "Champs 3"},
	// Champs
	{"name" : "Champs 1", "parent": ""},
	{"name" : "Champs 2", "parent": ""},
	{"name" : "Champs 3", "parent": ""},
	{"name" : "Champs 4", "parent": ""}
	];

// *********** Convert flat data into a nice tree ***************
// create a name: node map
var dataMap = data.reduce(function(map, node) {
	map[node.name] = node;
	return map;
	});

// create the tree array
var treeData = [];
data.forEach(function(node) {
	// add to parent
	var parent = dataMap[node.parent];
	if (parent) {
		// create child array if it doesn't exist
		(parent._children || (parent._children = []))
			// add node to child array
			.push(node);
	} else {
		// parent is null or missing
		treeData.push(node);
	}
});


// ************** Generate the tree diagram	 *****************
	// ************** Generate the tree diagram	 *****************
	var margin = {top: 20, right: 120, bottom: 20, left: 120},
		width = 1200 - margin.right - margin.left,
		height = 800 - margin.top - margin.bottom;
		
	var i = 0,
		duration = 750,
		root;


	var tree = d3.layout.tree()
		.size([height, width]);

	var diagonal = d3.svg.diagonal()
		.projection(function(d) { return [d.y, d.x]; });

	var svg = d3.select("#graphic").append("svg")
		.attr("width", width + margin.right + margin.left)
		.attr("height", height + margin.top + margin.bottom)
		.attr("class", "border border-warning rounded")
		.call(d3.behavior.zoom().on("zoom", function () {
    		svg.attr("transform", "translate(" + d3.event.translate + ")" + " scale(" + d3.event.scale + ")")
  		}))
		.append("g")
			.attr("transform", "translate(" + margin.left + "," + margin.top + ")");



	root = treeData[0];
	root.x0 = height / 2;
	root.y0 = 0;
	  
	update(root);

	d3.select(self.frameElement).style("height", "500px");

	function update(source) {

	  // Compute the new tree layout.
	  var nodes = tree.nodes(root).reverse(),
		  links = tree.links(nodes);

	  // Normalize for fixed-depth.
	  nodes.forEach(function(d) { d.y = d.depth * 180; });

	  // Update the nodes…
	  var node = svg.selectAll("g.node")
		  .data(nodes, function(d) { return d.id || (d.id = ++i); });

	  // Enter any new nodes at the parent's previous position.
	  var nodeEnter = node.enter().append("g")
		  .attr("class", "node")
		  .attr("transform", function(d) { return "translate(" + source.y0 + "," + source.x0 + ")"; })
		  .on("click", click);

	  nodeEnter.append("circle")
		  .attr("r", 1e-6)
		  .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

	  nodeEnter.append("text")
		  .attr("x", function(d) { return d.children || d._children ? -13 : 13; })
		  .attr("dy", ".35em")
		  .attr("text-anchor", function(d) { return d.children || d._children ? "end" : "start"; })
		  .text(function(d) { return d.name; })
		  .style("fill-opacity", 1e-6);

	  // Transition nodes to their new position.
	  var nodeUpdate = node.transition()
		  .duration(duration)
		  .attr("transform", function(d) { return "translate(" + d.y + "," + d.x + ")"; });

	  nodeUpdate.select("circle")
		  .attr("r", 10)
		  .style("fill", function(d) { return d._children ? "lightsteelblue" : "#fff"; });

	  nodeUpdate.select("text")
		  .style("fill-opacity", 1);

	  // Transition exiting nodes to the parent's new position.
	  var nodeExit = node.exit().transition()
		  .duration(duration)
		  .attr("transform", function(d) { return "translate(" + source.y + "," + source.x + ")"; })
		  .remove();

	  nodeExit.select("circle")
		  .attr("r", 1e-6);

	  nodeExit.select("text")
		  .style("fill-opacity", 1e-6);

	  // Update the links…
	  var link = svg.selectAll("path.link")
		  .data(links, function(d) { return d.target.id; });

	  // Enter any new links at the parent's previous position.
	  link.enter().insert("path", "g")
		  .attr("class", "link")
		  .attr("d", function(d) {
			var o = {x: source.x0, y: source.y0};
			return diagonal({source: o, target: o});
		  });

	  // Transition links to their new position.
	  link.transition()
		  .duration(duration)
		  .attr("d", diagonal);

	  // Transition exiting nodes to the parent's new position.
	  link.exit().transition()
		  .duration(duration)
		  .attr("d", function(d) {
			var o = {x: source.x, y: source.y};
			return diagonal({source: o, target: o});
		  })
		  .remove();

	  // Stash the old positions for transition.
	  nodes.forEach(function(d) {
	  	console.log(d.x + " " + d.y);
		d.x0 = d.x;
		d.y0 = d.y;
	  });
	}

	// Toggle children on click.
	function click(d) {
	  if (d.children) {
		d._children = d.children;
		d.children = null;
	  } else {
		d.children = d._children;
		d._children = null;
	  }
	  update(d);
	}

