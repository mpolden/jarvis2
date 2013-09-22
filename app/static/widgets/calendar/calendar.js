var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('CalendarCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('calendar', function (ev, body) {
      body.events.map(function (e) {
        e.date = moment(e.date).lang('nb');
      });
      if (body.events.length > 0) {
        var eventDate = body.events[0].date,
          now = moment();
        if (eventDate.isBefore(now) || eventDate.isSame(now, 'day')) {
          body.today = body.events[0];
          body.events = body.events.slice(1, 5);
        } else {
          body.events = body.events.slice(0, 4);
        }
      }
      angular.extend($scope, body);
    });

  }
]);
