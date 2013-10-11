/* jshint camelcase: false */
var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('AvinorCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('avinor', function (ev, body) {
      body.flights = body.flights.map(function (f) {
        f.date = moment(f.schedule_time).lang('nb');
        return f;
      }).filter(function (f) {
        return f.date.isAfter();
      });
      body.next = body.flights.shift() || null;
      body.flights = body.flights.slice(0, 4);
      angular.extend($scope, body);
    });

  }
]);
