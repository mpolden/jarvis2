var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('AtbCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('atb', function (ev, body) {
      body.departures.map(function (d) {
        var departureTime = moment(d.registeredDepartureTime).lang('nb'),
          now = moment();
        if (departureTime.isBefore(now)) {
          // BusBuddy sometimes returns dates in the past
          departureTime.set('year', now.get('year'));
          departureTime.set('month', now.get('month'));
          departureTime.set('date', now.get('date'));
        }
        d.departureTime = departureTime;
      });
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
