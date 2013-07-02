var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('SonosCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('sonos', function (ev, body) {
      angular.extend($scope, body);
    });

  }
]);
