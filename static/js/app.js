'use strict';

/* Setup Angular app */
var jarvis = angular.module('jarvis', []);

jarvis.controller('EventCtrl', ['$scope', function ($scope) {

  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    $scope.$apply(function () {
      var data = JSON.parse(message.data);
      $scope[data.widget] = data.body;
    });
  }, false);

}]);

/* Initialize gridster */
$(function () {
  $('.gridster ul').gridster({
    widget_margins: [10, 10],
    widget_base_dimensions: [140, 140]
  });
});
