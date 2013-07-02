var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('UptimeCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('uptime', function (ev, body) {
      body.hosts.forEach(function (host) {
        host.active = host.active ? 'aktiv' : 'inaktiv';
      });
      angular.extend($scope, body);
    });

  }
]);
