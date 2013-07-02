var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('AtbCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var eta = function (departure) {
      var n = departure !== null ? departure.eta : 0,
        unit = n > 1 ? 'minutter' : 'minutt';
      return n === 0 ? 'L\u00d8P!' : 'om ' + n + ' ' + unit;
    };

    $scope.$on('atb', function (ev, body) {
      if (body.departures.length > 0) {
        body.next = body.departures[0];
        body.next.eta = eta(body.next);
        body.upcoming = body.departures.slice(1, 5);
      } else {
        body.next = null;
        body.upcoming = [];
      }
      angular.extend($scope, body);
    });

  }
]);
