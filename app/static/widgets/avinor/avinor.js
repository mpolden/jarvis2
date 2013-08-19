/* jshint camelcase: false */
var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('AvinorCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('avinor', function (ev, body) {
      body.flights.map(function (flight) {
        flight.date = moment(flight.schedule_time);
      });
      if (body.flights.length > 0) {
        body.next = body.flights[0];
        body.flights = body.flights.slice(1, 5);
      } else {
        body.next = null;
        body.flights = [];
      }
      angular.extend($scope, body);
    });

  }
]);
