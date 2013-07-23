var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('HackernewsCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('hackernews', function (ev, body) {
      if (body.items && body.items.length > 0) {
        body.items = body.items.slice(0, 10);
      }
      angular.extend($scope, body);
    });

  }
]);
