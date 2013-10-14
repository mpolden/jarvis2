var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('CalendarCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('calendar', function (ev, body) {
      if (body.events.length === 0) {
        return;
      }
      body.events.forEach(function (e) {
        e.date = moment(e.date).lang('nb');
      });
      var eventDate = body.events[0].date,
        now = moment();
      if (eventDate.isBefore(now) || eventDate.isSame(now, 'day')) {
        body.today = body.events.shift() || null;
      } else {
        body.today = null;
      }
      body.events = body.events.slice(0, 4);
      angular.extend($scope, body);
    });

  }
]);
