var stats = stats || {};

stats.state = {
  data: {},
  update: function (event) {
    stats.state.data = event.detail;
    m.redraw();
  }
};

stats.view = function () {
  if (Object.keys(stats.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  return [
    m('h1', 'Dagens forbruk'),
    m('table', [
      m('tr.fade', [
        m('th', 'Drikke'),
        m('th', 'Antall')
      ]),
      m('tr', [
        m('td', 'Kaffe'),
        m('td', [
          m('span', stats.state.data.stats.coffee),
          m('span.fade', ' / ' + stats.state.data.max.coffee)
        ])
      ]),
      m('tr', [
        m('td', 'Øl'),
        m('td', [
          m('span', stats.state.data.stats.beer),
          m('span.fade', ' / ' + stats.state.data.max.beer)
        ])
      ])
    ]),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      stats.state.data.updatedAt)
  ];
};

stats.oncreate = function () {
  jrvs.subscribe('stats');
};

jrvs.mount('stats');
