var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('GmailCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var gauge = null;
    var opts = {
      lines: 8,
      angle: 0.15,
      lineWidth: 0.3,
      pointer: {
        length: 0.85,
        strokeWidth: 0.045,
        color: '#ffffff'
      },
      limitMax: 'true',
      strokeColor: '#9caac6'
    };

    $scope.$on('gmail', function (ev, body) {
      if (gauge === null) {
        var target = document.querySelector('#gmail canvas');
        var textField = document.querySelector('#gmail #unread');
        gauge = new Gauge(target).setOptions(opts);
        gauge.setTextField(textField);
      }
      gauge.maxValue = body.count;
      gauge.set(body.unread);
      angular.extend($scope, body);
    });

  }
]);
