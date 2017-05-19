var plex = plex || {};

plex.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
    if (body.movies.length > 4) {
      body.movies = body.movies.slice(0, 4);
    }
    if (body.shows.length > 4) {
      body.shows = body.shows.slice(0, 4);
    }
    plex.state.data = body;
    m.redraw();
  }
};

plex.view = function () {
  if (Object.keys(plex.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var shows = plex.state.data.shows.map(function (show) {
    return m('tr', [
      m('td.title', jrvs.truncate(show.name, 24)),
      m('td.year', show.season + 'x' + show.episode),
    ]);
  });
  var movies = plex.state.data.movies.map(function (movie) {
    return m('tr', [
      m('td.title', jrvs.truncate(movie.title, 24)),
      m('td.year', '(' + movie.year + ')')
    ]);
  });
  return [
    m('p.fade', 'Plex'),
    m('table', shows),
    m('hr'),
    m('table', movies),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      plex.state.data.updatedAt)
  ];
};

plex.oncreate = function () {
  jrvs.subscribe('plex');
};

jrvs.mount('plex');
