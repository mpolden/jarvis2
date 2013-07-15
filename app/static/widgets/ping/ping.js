/* jshint nonew: false */

var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('PingCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var graph = null;

    var initGraph = function (element, values) {
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
      graph = new Rickshaw.Graph({
        element: element,
        width: 565,
        height: 240,
        renderer: 'area',
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
      graph.render();
    };

    $scope.$on('ping', function (ev, body) {
      if (graph === null) {
        var element = document.querySelector('#chart');
        if (element !== null) {
          initGraph(element, body.values);
        }
      } else {
        graph.series.addData(body.values);
        graph.render();
      }
    });
  }
]);
