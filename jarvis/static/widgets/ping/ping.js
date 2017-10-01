/* jshint maxstatements: 50 */

var ping = ping || {graph: {}};

ping.graph.create = function (vnode) {
  var margin = {top: 20, right: 50, bottom: 50, left: 60};
  var width = vnode.dom.clientWidth - margin.left - margin.right;
  var height = 300 - margin.top - margin.bottom;

  var x = d3.scaleTime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);
  var z = d3.scaleOrdinal(d3.schemeCategory10);

  var line = d3.line()
      .curve(d3.curveLinear)
      .x(function(d) { return x(d.time); })
      .y(function(d) { return y(d.latency); });

  var timeParse = d3.timeParse('%H:%M:%S');

  var xAxis = d3.axisBottom(x)
      .tickFormat(d3.timeFormat(':%S'));
  var yAxis = d3.axisLeft(y);

  // Create SVG
  var svg = d3.select(vnode.dom).append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform',
            'translate(' + margin.left + ',' + margin.top + ')');

  // X axis
  svg.append('g')
    .attr('class', 'x-axis')
    .attr('transform', 'translate(0,' + height + ')')
    .call(xAxis);

  // Y axis
  svg.append('g')
    .attr('class', 'y-axis')
    .call(yAxis)
    .append('text')
    .attr('y', -10)
    .attr('x', 40)
    .text('Latency (ms)');

  return function (data) {
    // Parse all times
    data = Object.keys(data).map(function (k) {
      return {
        id: k,
        values: data[k].map(function (v) {
          v.time = timeParse(v.time);
          return v;
        })
      };
    });

    // Set time values for X axis
    var times = Object.keys(data).reduce(function (acc, k) {
      return acc.concat(data[k].values);
    }, []).map(function (v) { return v.time; });
    xAxis.tickValues(times);

    // Set scale ranges
    x.domain(d3.extent(times));
    y.domain([
      0,
      d3.max(data, function (d) {
        return d3.max(d.values, function (v) { return v.latency; });
      })
    ]);
    z.domain(data.map(function(d) { return d.id; }));

    // Join data
    var device = svg.selectAll('.device')
        .data(data);

    var deviceGroups = device.enter()
        .append('g')
        .attr('class', 'device')
        .merge(device);

    // Update each line
    deviceGroups
      .append('path')
      .attr('class', 'line');

    device.select('.line')
      .transition()
      .duration(750)
      .attr('d', function (d) { return line(d.values); });

    // Update label for each line
    deviceGroups
      .append('text')
      .attr('class', 'label');

    device.select('.label')
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr('transform', function(d) {
        return 'translate(' + x(d.value.time) + ',' + y(d.value.latency) + ')';
      })
      .attr('x', 3)
      .attr('dy', '0.35em')
      .style('font', '10px sans-serif')
      .text(function(d) { return d.id; });

    // X axis
    svg.select('.x-axis')
      .transition()
      .call(xAxis)
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('dx', '-.8em')
      .attr('dy', '.15em')
      .attr('transform', 'rotate(-45)');

    // Y axis
    svg.select('.y-axis')
      .call(yAxis);
  };
};

ping.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var data = vnode.attrs.data.values;
  return m('div', {
    oncreate: function (vnode) {
      ping.graph.update = ping.graph.create(vnode);
      ping.graph.update(data);
    },
    onupdate: function () {
      ping.graph.update(data);
    }
  });
};
