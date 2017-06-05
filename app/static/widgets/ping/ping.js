/* jshint nonew: false */

var ping = ping || {};

ping.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  return [
    m('div#y-axis'),
    m('div#chart', {
      oncreate: function (vnode) {
        vnode.state.graph = ping.createGraph(vnode.dom, state.values);
        vnode.state.graph.render();
      },
      onupdate: function (vnode) {
        vnode.state.graph.series.addData(state.values);
        vnode.state.graph.render();
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
