/* jshint camelcase: false */
var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('AvinorCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var getMonthName = function (month) {
      return ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli',
        'august', 'september', 'oktober', 'november',
        'desember'][month - 1];
    };

    $scope.$on('avinor', function (ev, body) {
      body.flights.map(function (d) {
        var date = moment(d.schedule_time);
        d.day = date.format('D');
        d.month = getMonthName(date.format('M'));
        d.monthShort = d.month.substring(0, 3);
        d.time = date.format('HH:mm');
      });
      if (body.flights.length > 0) {
        body.next = body.flights[0];
        body.flights = body.flights.slice(1, 6);
      } else {
        body.next = null;
        body.flights = [];
      }
      angular.extend($scope, body);
    });

  }
]);
