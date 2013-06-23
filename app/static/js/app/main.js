var jarvis = jarvis || angular.module('jarvis', ['truncate']);

jarvis.controller('EventCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var source = new EventSource('/events');

    source.addEventListener('message', function (message) {
      var o = JSON.parse(message.data);
      if (Object.keys(o.body).length > 0) {
        $scope.$broadcast(o.widget, o.body);
      }
    }, false);

  }
]);
