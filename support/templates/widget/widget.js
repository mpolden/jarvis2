var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('{{ name|capitalize }}Ctrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('{{ name|lower }}', function (ev, body) {
      angular.extend($scope, body);
    });

  }
]);
