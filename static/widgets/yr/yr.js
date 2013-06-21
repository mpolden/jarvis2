var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('YrCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('yr', function (ev, body) {
      $scope.$apply(function () {
        $scope[ev.name] = body;
      });
    });

  }
]);
