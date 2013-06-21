var jarvis = jarvis || angular.module('jarvis', ['truncate']);

jarvis.controller('EventCtrl', ['$scope', function ($scope) {
  'use strict';

  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    var o = JSON.parse(message.data);
    $scope.$broadcast(o.widget, o.body);
  }, false);

}]);
