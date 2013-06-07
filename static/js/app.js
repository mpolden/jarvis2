/* Setup Angular app */
var jarvis = angular.module('jarvis', []);

jarvis.controller('EventCtrl', ['$scope', function ($scope) {

  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    $scope.$apply(function () {
      $scope.event = JSON.parse(message.data);
    });
  }, false);

}]);

/* Initialize gridster */
$(function () {
  $(".gridster ul").gridster({
    widget_margins: [10, 10],
    widget_base_dimensions: [140, 140]
  });
});
