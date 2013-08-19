var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('StatsCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var gauges = {
      coffee: null,
      beer: null
    };
    var opts = {
      lines: 8,
      angle: 0.15,
      lineWidth: 0.3,
      pointer: {
        length: 0.85,
        strokeWidth: 0.045,
        color: '#ffffff'
      },
      limitMax: false,
      strokeColor: '#665847'
    };

    var updateGauge = function (gauge, body) {
      if (gauges[gauge] === null) {
        var target = document.querySelector('#stats #' + gauge);
        var textField = document.querySelector('#stats #' + gauge + '-count');
        gauges[gauge] = new Gauge(target).setOptions(opts);
        gauges[gauge].setTextField(textField);
      }
      gauges[gauge].maxValue = body.max[gauge];
      gauges[gauge].set(body.stats[gauge]);
    };

    $scope.$on('stats', function (ev, body) {
      updateGauge('coffee', body);
      updateGauge('beer', body);
      angular.extend($scope, body);
    });
  }
]);
