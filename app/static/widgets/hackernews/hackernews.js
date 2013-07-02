var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('HackerNewsCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('hackernews', function (ev, body) {
      if (body.items && body.items.length > 0) {
        body.items = body.items.slice(1, 11);
      }
      angular.extend($scope, body);
    });

  }
]);
