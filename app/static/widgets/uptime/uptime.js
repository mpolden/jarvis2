var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('UptimeCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('uptime', function (ev, body) {
      body.forEach(function (host) {
        host.active = host.active ? 'aktiv' : 'inaktiv';
      });
      $scope[ev.name] = body;
    });

  }
]);
