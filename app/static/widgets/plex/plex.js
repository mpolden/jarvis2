var jarvis = jarvis || angular.module('jarvis', []);

jarvis.controller('PlexCtrl', ['$scope',
  function ($scope) {
    'use strict';

    $scope.$on('plex', function (ev, body) {
      if (body.movies.length > 5) {
        body.movies = body.movies.slice(0, 5);
      }
      if (body.shows.length > 5) {
        body.shows = body.shows.slice(0, 5);
      }
      angular.extend($scope, body);
    });

  }
]);
