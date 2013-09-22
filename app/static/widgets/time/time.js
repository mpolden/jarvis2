var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('TimeCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var setTime = function () {
      $scope.$apply(function () {
        $scope.now = moment().lang('nb');
      });
    };

    setInterval(setTime, 500);

  }
]);
