var nsb = nsb || {};

nsb.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
    if (body.departures.length > 0) {
      body.next = body.departures[0];
      body.upcoming = body.departures.slice(1, 5);
    } else {
      body.next = null;
      body.upcoming = [];
    }
    nsb.state.data = body;
    m.redraw();
  }
};

nsb.view = function () {
  if (Object.keys(nsb.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = nsb.state.data.upcoming.map(function (departure) {
    return m('tr', [
      m('td', departure.departure),
      m('td', departure.arrival),
      m('td', departure.duration)
    ]);
  });
  return [
    m('p.fade', [
      'Neste tog fra ',
      m('em', nsb.state.data.from),
      ' til ',
      m('em', nsb.state.data.to),
      ' går ',
      m('em', nsb.state.data.date)
    ]),
    m('h1', nsb.state.data.next.departure),
    m('h2.fade', [
      'Ankomst: ',
      m('em', nsb.state.data.next.arrival),
      ' (',
      m('em', nsb.state.data.next.duration),
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
      nsb.state.data.updatedAt)
  ];
};

nsb.oncreate = function () {
  jrvs.subscribe('nsb');
};

jrvs.mount('nsb');
