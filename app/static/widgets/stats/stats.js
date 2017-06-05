var stats = stats || {};

stats.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
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
          m('span', state.stats.coffee),
          m('span.fade', ' / ' + state.max.coffee)
        ])
      ]),
      m('tr', [
        m('td', 'Øl'),
        m('td', [
          m('span', state.stats.beer),
          m('span.fade', ' / ' + state.max.beer)
        ])
      ])
    ]),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
