var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('AtbCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var fmtMessage = function (departure) {
      var n = departure !== null ? departure.remaining : 0,
        unit = n > 1 ? 'minutter' : 'minutt';
      return n === 0 ? 'LØP!' : 'om ' + n + ' ' + unit;
    };

    var processMessage = function (ev, body) {
      var widget = ev.name;

      if (body.departures.length > 0) {
        body.first = body.departures[0];
        body.first.remainingMessage = fmtMessage(body.first);
        body.rest = body.departures.slice(1, 5);
      } else {
        body.first = null;
        body.rest = [];
      }

      angular.extend($scope, body);
    };

    $scope.$on('atb', processMessage);

  }
]);
