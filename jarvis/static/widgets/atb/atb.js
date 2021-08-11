var atb = atb || {};

atb.parseState = function (data) {
  var body = data;
  body.departures.forEach(function (d) {
    d.departureTime = moment(d.scheduledDepartureTime).locale('nb');
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
