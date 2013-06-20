'use strict';

var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('EventCtrl', ['$scope', function ($scope) {

  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    var o = JSON.parse(message.data);
    $scope.$broadcast(o.widget, o.body);
  }, false);

}]);
