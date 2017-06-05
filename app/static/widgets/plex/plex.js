var plex = plex || {};

plex.parseState = function (data) {
  var body = data;
  if (body.movies.length > 4) {
    body.movies = body.movies.slice(0, 4);
  }
  if (body.shows.length > 4) {
    body.shows = body.shows.slice(0, 4);
  }
  return body;
};

plex.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = plex.parseState(vnode.attrs.data);
  var shows = state.shows.map(function (show) {
    return m('tr', [
      m('td.title', jrvs.truncate(show.name, 24)),
      m('td.year', show.season + 'x' + show.episode),
    ]);
  });
  var movies = state.movies.map(function (movie) {
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
      state.updatedAt)
  ];
};
