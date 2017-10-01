var avinor = avinor || {};

avinor.parseState = function (data) {
  data.flights = data.flights.map(function (f) {
    f.date = moment(f.schedule_time).locale('nb');
    return f;
  }).filter(function (f) {
    return f.date.isAfter();
  });
  data.next = data.flights.shift() || null;
  data.flights = data.flights.slice(0, 4);
  return data;
};

avinor.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = avinor.parseState(vnode.attrs.data);
  var rows = state.flights.map(function (flight) {
    return m('tr', [
      m('td', flight.flight_id),
      m('td', flight.date.format('D. MMM HH:mm'))
    ]);
  });
  return [
    m('p.fade', [
      'Neste fly (',
      m('em', state.next.flight_id),
      ') fra ',
      m('em', state.from),
      ' til ',
      m('em', state.to),
      ' går ',
      m('em', state.next.date.format('dddd, D. MMMM'))
    ]),
    m('h1', state.next.date.format('HH:mm')),
    m('h2', state.next.date.fromNow()),
    m('table', [
      m('tr.fade', [
        m('th', 'Flight'),
        m('th', 'Avgang')
      ])
    ].concat(rows)),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
