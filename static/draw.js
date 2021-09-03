// var ctx = document.getElementById('temp_chart').getContext('2d');
// var xmlhttp = new XMLHttpRequest();
// var url = "/plant";

// xmlhttp.addEventListener('load', dataLoaded)
// xmlhttp.open("GET", url, true);
// xmlhttp.send();
function makeD3Chart(){
  // set the dimensions and margins of the graph
  var margin = { top: 10, right: 30, bottom: 30, left: 60 },
    width = 600 - margin.left - margin.right,
    height = 600 - margin.top - margin.bottom;

  // append the svg object to the body of the page
  var svg = d3.select("#d3_chart")
    .append("svg")
    //.attr("preserveAspectRatio", "xMinYMin meet")
    //.attr("viewBox", "0 0 300 300")
    //.classed("svg-content", true);
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");

  var temp_svg = d3.select("#temp_chart")
    .append("svg")
    .attr("width", width + margin.left + margin.right)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform",
      "translate(" + margin.left + "," + margin.top + ")");



  //Read the data
  url = "/plant?name=" + plant;
  console.log('Getting url: ' + url)
  d3.json(url).then(x => x.values).then(function (data) {

      // Add X axis --> it is a date format
      var x = d3.scaleTime()
        .domain(d3.extent(data, function(d) {return Date.parse(d.timestamp)}))
        .range([0,width]);
      svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));
      temp_svg.append("g")
        .attr("transform", "translate(0," + height + ")")
        .call(d3.axisBottom(x));

      // Add Y axis
      var y = d3.scaleLinear()
        .domain(d3.extent(data, function (d) { return +d.temp }))
        .range([height, 0]);
      svg.append("g")
        .call(d3.axisLeft(y));
      temp_svg.append("g")
        .call(d3.axisLeft(y));

      var ymoist = d3.scaleLinear()
        .domain([d3.min(data, (d) => { return d.moisture }), d3.max(data, function (d) { return d.moisture })])
        .range([height, 0])
      svg.append("g")
        .attr("transform", "translate(" + width + ", 0)")
        .call(d3.axisRight(ymoist))

      
      temp_svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "crimson")
        .attr("stroke-width", 1.5)
        .attr("d", d3.line()
          .x(function (d) {return x(Date.parse(d.timestamp))})
          .y(function (d) {return y(d.temp)}))
      // Add the line
      svg.append("path")
        .datum(data)
        .attr("fill", "none")
        .attr("stroke", "blue")
        .attr("stroke-width", 1.5)
        .attr("class", "rawMoisture")
        .style("visibility", "hidden")
        .attr("d", d3.line()
          .x(function (d) {return x(Date.parse(d.timestamp))})
          .y(function (d) {return ymoist(d.moisture)}))
    })
  d3.json('/moisturesma/' + plant).then(x => x.values).then(function (data) {
    var x = d3.scaleTime()
      .domain(d3.extent(data, function(d) {return Date.parse(d.timestamp)}))
      .range([0,width]);
    var ymoist = d3.scaleLinear()
      .domain([300, d3.max(data, function (d) { return d.sma })])
      .range([height, 0])


    line = d3.line()
      .x(function(d) { return x(Date.parse(d.timestamp))})
      .y(function(d) { return ymoist(d.sma) });

    d3.select("svg").select("g").append("path")
      .attr("fill", "none")
      .attr("stroke", "steelblue")
      .attr("stroke-width", 1.5)
      .attr("d", line(data))
  });


}

$(document).ready(function() {

  makeD3Chart()

  $("input#rawMoisture").click(() => {
    cb = $("input#rawMoisture")
    d3.select(".rawMoisture").call((selection) => {
      selection.transition().duration(900).style("visibility", () => {
        let value = cb.prop("checked") ? "visible" : "hidden";
        return value
      })
    })
  })


})
