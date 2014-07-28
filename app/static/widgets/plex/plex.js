var plex = {
  'el': document.getElementById('plex')
};

plex.controller = function () {
  var ctrl = this;
  ctrl.data = {};
  plex.el.addEventListener('plex', function (event) {
    var body = event.detail;
    if (body.movies.length > 4) {
      body.movies = body.movies.slice(0, 4);
    }
    if (body.shows.length > 4) {
      body.shows = body.shows.slice(0, 4);
    }
    ctrl.data = body;
    m.render(plex.el, plex.view(ctrl));
  });
};

plex.view = function (c) {
  if (Object.keys(c.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var shows = c.data.shows.map(function (show) {
    return m('tr', [
      m('td.title', jrvs.truncate(show.name, 24)),
      m('td.year', show.season + 'x' + show.episode),
    ]);
  });
  var movies = c.data.movies.map(function (movie) {
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
      c.data.updatedAt)
  ];
};

if (plex.el !== null) {
  m.module(plex.el, plex);
}
