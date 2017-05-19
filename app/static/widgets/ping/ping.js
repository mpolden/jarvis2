/* jshint nonew: false */

var ping = ping || {};

ping.element = document.getElementById('ping');

ping.state = {
  data: {},
  graph: null,
  update: function (event) {
    ping.state.data = event.detail;
    m.redraw();
  }
};

ping.view = function () {
  if (Object.keys(ping.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  return [
    m('div#y-axis'),
    m('div#chart', {
      oncreate: function (vnode) {
        ping.state.graph = ping.createGraph(vnode.dom, ping.state.data.values);
        ping.state.graph.render();
      },
      onupdate: function () {
        ping.state.graph.series.addData(ping.state.data.values);
        ping.state.graph.render();
      }
    }),
    m('div#legend')
  ];
};

ping.createGraph = function (element, values) {
  var labels = Object.keys(values).map(function (name) {
    return {
      name: name
    };
  });
  var series = new Rickshaw.Series.FixedDuration(
    labels,
    new Rickshaw.Color.Palette({
      scheme: 'colorwheel'
    }), {
      timeInterval: 5000,
      maxDataPoints: 100,
      timeBase: new Date().getTime() / 1000
    }
  );
  var graph = new Rickshaw.Graph({
    element: element,
    width: 535,
    height: 240,
    renderer: 'line',
    stroke: true,
    unstack: true,
    series: series
  });
  new Rickshaw.Graph.Legend({
    element: document.querySelector('#legend'),
    graph: graph
  });
  new Rickshaw.Graph.Axis.Y({
    element: document.querySelector('#y-axis'),
    graph: graph,
    orientation: 'left',
    ticks: 5,
    tickFormat: function (n) {
      return n + ' ms';
    }
  });
  return graph;
};

ping.oncreate = function () {
  jrvs.subscribe('ping');
};

jrvs.mount('ping');
