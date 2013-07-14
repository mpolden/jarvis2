var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('PlexCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('plex', function (ev, body) {
      if (body.movies.length > 4) {
        body.movies = body.movies.slice(0, 4);
      }
      if (body.shows.length > 4) {
        body.shows = body.shows.slice(0, 4);
      }
      angular.extend($scope, body);
    });

  }
]);
