var avinor = avinor || {};

avinor.state = {
  data: {},
  update: function (event) {
    var data = event.detail;
    data.flights = data.flights.map(function (f) {
      f.date = moment(f.schedule_time).locale('nb');
      return f;
    }).filter(function (f) {
      return f.date.isAfter();
    });
    data.next = data.flights.shift() || null;
    data.flights = data.flights.slice(0, 4);
    avinor.state.data = data;
    m.redraw();
  }
};

avinor.view = function () {
  if (Object.keys(avinor.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = avinor.state.data.flights.map(function (flight) {
    return m('tr', [
      m('td', flight.flight_id),
      m('td', flight.date.format('D. MMM HH:mm'))
    ]);
  });
  return [
    m('p.fade', [
      'Neste fly (',
      m('em', avinor.state.data.next.flight_id),
      ') fra ',
      m('em', avinor.state.data.from),
      ' til ',
      m('em', avinor.state.data.to),
      ' går ',
      m('em', avinor.state.data.next.date.format('dddd, D. MMMM'))
    ]),
    m('h1', avinor.state.data.next.date.format('HH:mm')),
    m('h2', avinor.state.data.next.date.fromNow()),
    m('table', [
      m('tr.fade', [
        m('th', 'Flight'),
        m('th', 'Avgang')
      ])
    ].concat(rows)),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      avinor.state.data.updatedAt)
  ];
};

avinor.oncreate = function () {
  jrvs.subscribe('avinor');
};

jrvs.mount('avinor');
