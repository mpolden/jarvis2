var stats = {
  'el': document.getElementById('stats')
};

stats.controller = function () {
  var ctrl = this;
  ctrl.data = {};
  stats.el.addEventListener('stats', function (event) {
    ctrl.data = event.detail;
    m.render(stats.el, stats.view(ctrl));
  });
};

stats.view = function (c) {
  if (Object.keys(c.data).length === 0) {
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
          m('span', c.data.stats.coffee),
          m('span.fade', ' / ' + c.data.max.coffee)
        ])
      ]),
      m('tr', [
        m('td', 'Øl'),
        m('td', [
          m('span', c.data.stats.beer),
          m('span.fade', ' / ' + c.data.max.beer)
        ])
      ])
    ]),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      c.data.updatedAt)
  ];
};

if (stats.el !== null) {
  m.module(stats.el, stats);
}
