var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('TimeCtrl', ['$scope', function ($scope) {
  'use strict';

  var fmtTime = function (n) {
    return n < 10 ? '0' + n : n;
  };

  var getDayName = function (date) {
    return ['søndag', 'mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag',
            'lørdag'][date.getDay()];
  };

  var getMonthName = function (date) {
    return ['januar', 'februar', 'mars', 'april', 'mai', 'juni', 'juli',
            'august', 'september', 'oktober', 'november',
            'desember'][date.getMonth()];
  };

  var setTime = function () {
    var today = new Date(),
        h = fmtTime(today.getHours()),
        m = fmtTime(today.getMinutes()),
        y = today.getFullYear();

    $scope.$apply(function () {
      $scope.time = h + ':' + m;
      $scope.date = today.getDate() + '. ' + getMonthName(today) + ' ' + y;
      $scope.day = getDayName(today);
    });
  };

  setInterval(setTime, 500);
 
}]);

