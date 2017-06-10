/* jshint maxstatements: 50 */

var ping = ping || {};

ping.graph = function (vnode, update) {
  var margin = {top: 20, right: 50, bottom: 50, left: 60};
  var width = vnode.dom.clientWidth - margin.left - margin.right;
  var height = 300 - margin.top - margin.bottom;

  var x = d3.scaleTime().range([0, width]);
  var y = d3.scaleLinear().range([height, 0]);
  var z = d3.scaleOrdinal(d3.schemeCategory10);

  var line = d3.line()
      .curve(d3.curveBasis)
      .x(function(d) { return x(d.time); })
      .y(function(d) { return y(d.latency); });

  var data = Object.keys(vnode.state.data).map(function (k) {
    return {id: k, values: vnode.state.data[k]};
  });

  // Scale according to ranges of the data
  var times = Object.keys(vnode.state.data).reduce(function (acc, k) {
    return acc.concat(vnode.state.data[k]);
  }, []).map(function (v) {
    return v.time;
  });
  x.domain(d3.extent(times));
  y.domain([
    d3.min(data, function (d) {
      return d3.min(d.values, function (v) { return v.latency; });
    }),
    d3.max(data, function (d) {
      return d3.max(d.values, function (v) { return v.latency; });
    })
  ]);
  z.domain(data.map(function(d) { return d.id; }));

  var xAxis = d3.axisBottom(x)
      .tickValues(times)
      .tickFormat(d3.timeFormat(':%S'));
  var yAxis = d3.axisLeft(y)
      .tickFormat(function (v) { return v + ' ms'; });
  var svg;
  var device;
  if (update) {
    svg = d3.select(vnode.dom);
    device = svg.selectAll('.device').data(data);

    // Update each line
    device.select('.line')
      .transition()
      .duration(750)
      .attr('d', function (d) { return line(d.values); });

    // Update line label
    device.select('text')
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr('transform', function(d) {
        return 'translate(' + x(d.value.time) + ',' + y(d.value.latency) + ')';
      })
      .attr('x', 3)
      .attr('dy', '0.35em')
      .style('font', '10px sans-serif')
      .text(function(d) { return d.id; });

    // Update X axis
    svg.select('.x-axis')
      .transition()
      .duration(750)
      .call(xAxis)
      // Re-draw tick labels with same rotation
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('dx', '-.8em')
      .attr('dy', '.15em')
      .attr('transform', 'rotate(-45)');

    // Update Y axis
    svg.select('.y-axis')
      .transition()
      .duration(750)
      .call(yAxis);
  } else {
    // Create SVG
    svg = d3.select(vnode.dom).append('svg')
      .attr('width', width + margin.left + margin.right)
      .attr('height', height + margin.top + margin.bottom)
      .append('g')
      .attr('transform',
            'translate(' + margin.left + ',' + margin.top + ')');

    device = svg.selectAll('.device')
      .data(data)
      .enter().append('g')
      .attr('class', 'device');

    // Draw each line
    device.append('path')
      .attr('class', 'line')
      .attr('d', function (d) { return line(d.values); });

    device.append('text')
      .datum(function(d) { return {id: d.id, value: d.values[d.values.length - 1]}; })
      .attr('transform', function(d) {
        return 'translate(' + x(d.value.time) + ',' + y(d.value.latency) + ')';
      })
      .attr('x', 3)
      .attr('dy', '0.35em')
      .style('font', '10px sans-serif')
      .text(function(d) { return d.id; });

    // X axis
    svg.append('g')
      .attr('class', 'x-axis')
      .attr('transform', 'translate(0,' + height + ')')
      .call(xAxis)
      .selectAll('text')
      .style('text-anchor', 'end')
      .attr('dx', '-.8em')
      .attr('dy', '.15em')
      .attr('transform', 'rotate(-45)');

    // Y axis
    svg.append('g')
      .attr('class', 'y-axis')
      .call(yAxis);
  }
};

ping.updateState = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return;
  }
  vnode.attrs.data.forEach(function (d) {
    if (typeof vnode.state.data[d.label] === 'undefined') {
      vnode.state.data[d.label] = [];
    }
    var timeParse = d3.timeParse('%H:%M:%S');
    d.time = timeParse(d.time);
    vnode.state.data[d.label].push(d);
    if (vnode.state.data[d.label].length > 10) {
      vnode.state.data[d.label].shift();
    }
  });
};

ping.oninit = function(vnode) {
  vnode.state.data = {};
};

ping.oncreate = ping.updateState;

ping.onupdate = ping.updateState;

ping.view = function (vnode) {
  if (Object.keys(vnode.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  return [
    m('div', {
      oncreate: function () {
        ping.graph(vnode, false);
      },
      onupdate: function () {
        ping.graph(vnode, true);
      }
    }),
  ];
};
