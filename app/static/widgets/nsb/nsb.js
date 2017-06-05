var nsb = nsb || {};

nsb.parseState = function (data) {
  var body = data;
  if (body.departures.length > 0) {
    body.next = body.departures[0];
    body.upcoming = body.departures.slice(1, 5);
  } else {
    body.next = null;
    body.upcoming = [];
  }
  return body;
};

nsb.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = nsb.parseState(vnode.attrs.data);
  var rows = state.upcoming.map(function (departure) {
    return m('tr', [
      m('td', departure.departure),
      m('td', departure.arrival),
      m('td', departure.duration)
    ]);
  });
  return [
    m('p.fade', [
      'Neste tog fra ',
      m('em', state.from),
      ' til ',
      m('em', state.to),
      ' går ',
      m('em', state.date)
    ]),
    m('h1', state.next.departure),
    m('h2.fade', [
      'Ankomst: ',
      m('em', state.next.arrival),
      ' (',
      m('em', state.next.duration),
      ')'
    ]),
    m('table', [
      m('tr.fade', [
        m('th', 'Avgang'),
        m('th', 'Ankomst'),
        m('th', 'Reisetid')
      ])
    ].concat(rows)),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
