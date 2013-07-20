/* jshint camelcase: false */
var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('GmailCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('gmail', function (ev, body) {
      var meter = $('#meter');
      if (meter.length !== 0) {
        if (meter.children().length === 0) {
          meter.knob({
            'min': 0,
            'max': body.count
          });
        }
        meter.val(body.unread_count).trigger('change');
      }
      angular.extend($scope, body);
    });

  }
]);
