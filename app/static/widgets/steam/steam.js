var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('SteamCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('steam', function (ev, body) {
      angular.extend($scope, body);
    });

    setInterval(function () {
      $('.deal:first').fadeOut(500)
        .next()
        .fadeIn(1000)
        .end()
        .appendTo('#deals');
    }, 10000);

  }
]);
