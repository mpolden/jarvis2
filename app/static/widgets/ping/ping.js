/* jshint nonew: false */

var ping = {
  'el': document.getElementById('ping')
};

ping.controller = function () {
  var ctrl = this;
  ctrl.data = {};
  ping.el.addEventListener('ping', function (event) {
    ctrl.data = event.detail;
    m.render(ping.el, ping.view(ctrl));
  });
};

ping.view = function (ctrl) {
  if (Object.keys(ctrl.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  return [
    m('div#y-axis'),
    m('div#chart', {
      'config': function (element, isInitialized) {
        if (isInitialized) {
          ping.graph.series.addData(ctrl.data.values);
        } else {
          ping.graph = ping.createGraph(element, ctrl.data.values);
        }
        ping.graph.render();
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

if (ping.el !== null) {
  m.module(ping.el, ping);
}
