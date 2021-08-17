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
        jrvs.truncate(departure.destination, 21)),
      m('td.time', departure.departureTime.format('HH:mm'))
    ]);
  });
  var nextText = 'Ingen avganger funnet';
  var nextDeparture = '';
  var nextDepartureFromNow = '';
  if (state.next !== null) {
    nextText = 'Buss ' + state.next.line + ' til ' +
      state.next.destination + ' går';
    nextDeparture = state.next.departureTime.format('HH:mm');
    nextDepartureFromNow = state.next.departureTime.fromNow();
  }
  return [
    m('p.fade', nextText),
    m('h1', nextDeparture),
    m('h2', nextDepartureFromNow),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
