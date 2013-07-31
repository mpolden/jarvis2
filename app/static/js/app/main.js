var jarvis = jarvis || angular.module('jarvis', ['truncate']);

jarvis.controller('EventCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var source = new EventSource('/events');

    source.addEventListener('message', function (message) {
      var o = JSON.parse(message.data);
      if (angular.isObject(o.body) && Object.keys(o.body).length > 1) {
        $scope.$apply(function () {
          $scope.$broadcast(o.widget, o.body);
        });
      }
    }, false);

  }
]);
