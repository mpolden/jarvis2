var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('TimeCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var setTime = function () {
      var now = moment().lang('nb');

      $scope.$apply(function () {
        $scope.time = now.format('HH:mm');
        $scope.date = now.format('D. MMMM YYYY');
        $scope.day = now.format('dddd');
      });
    };

    setInterval(setTime, 500);

  }
]);
