var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('SonosCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('sonos', function (ev, body) {
      $scope.$apply(function () {
        $scope[ev.name] = body;
      });
    });

  }
]);
