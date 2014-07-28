/* jshint nonew: false */

var ping = {
  'el': document.getElementById('ping')
};

ping.controller = function () {
  var ctrl = this;
  ctrl.graph = null;
  ping.el.addEventListener('ping', function (event) {
    ctrl.data = event.detail;
    m.render(ping.el, ping.view(ctrl));
    if (ctrl.graph === null) {
      ctrl.graph = ping.createGraph(ping.el, ctrl.data.values);
    } else {
      ctrl.graph.series.addData(ctrl.data.values);
    }
    ctrl.graph.render();
  });
};

ping.view = function () {
  return [
    m('div#y-axis'),
    m('div#chart'),
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
  var _ = new Rickshaw.Graph.Legend({
    element: document.querySelector('#legend'),
    graph: graph
  });
  var _ = new Rickshaw.Graph.Axis.Y({
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

if (ping.el !== null) {
  m.module(ping.el, ping);
}
