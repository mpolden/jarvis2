var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('CalendarCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('calendar', function (ev, body) {
      if (body.today === null) {
        body.today = {
          summary: 'Ingen hendelser',
          start: '--:--'
        };
      }
      if (body.events.length > 4) {
        body.events = body.events.slice(0, 4);
      }
      angular.extend($scope, body);
    });

  }
]);
