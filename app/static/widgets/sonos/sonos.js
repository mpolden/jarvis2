var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('SonosCtrl', ['$scope',
  function ($scope) {
    'use strict';

    var stateName = function (state) {
      if (state === 'PAUSED_PLAYBACK') {
        return 'Pause';
      }
      if (state === 'PLAYING') {
        return 'Spiller av';
      }
      if (state === 'STOPPED') {
        return 'Stoppet';
      }
      return '';
    };

    $scope.$on('sonos', function (ev, body) {
      body.state = stateName(body.state);
      angular.extend($scope, body);
    });

  }
]);
