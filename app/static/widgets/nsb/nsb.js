var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('NsbCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('nsb', function (ev, body) {
      if (body.departures.length > 0) {
        body.next = body.departures[0];
        body.upcoming = body.departures.slice(1, 5);
      } else {
        body.next = null;
        body.upcoming = [];
      }
      angular.extend($scope, body);
    });

  }
]);
