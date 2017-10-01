var atb = atb || {};

atb.parseState = function (data) {
  var body = data;
  body.departures.forEach(function (d) {
    var departureTime = moment(d.registeredDepartureTime).locale('nb'),
        now = moment();
    if (departureTime.isBefore(now)) {
      // BusBuddy sometimes returns dates in the past
      departureTime.set('year', now.get('year'));
      departureTime.set('month', now.get('month'));
      departureTime.set('date', now.get('date'));
    }
    d.departureTime = departureTime;
  });
  if (body.departures.length > 0) {
    body.next = body.departures[0];
    body.upcoming = body.departures.slice(1, 5);
  } else {
    body.next = null;
    body.upcoming = [];
  }
  return body;
};

atb.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = atb.parseState(vnode.attrs.data);
  var rows = state.upcoming.map(function (departure) {
    return m('tr', [
      m('td', {'class': 'destination'}, departure.line + ' ' +
        departure.destination),
      m('td.time', departure.departureTime.format('HH:mm'))
    ]);
  });
  return [
    m('p.fade', 'Buss ' + state.next.line + ' til ' +
      state.next.destination + ' går'),
    m('h1', state.next.departureTime.format('HH:mm')),
    m('h2', state.next.departureTime.fromNow()),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
