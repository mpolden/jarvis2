var nsb = nsb || {};

nsb.parse = function (data) {
  var now = moment();
  data.departures = data.departures.map(function (d) {
    d.departure = moment(d.departure);
    d.arrival = moment(d.arrival);
    return d;
  }).filter(function (d) {
    // Ignore departures that have passed
    return d.departure.isAfter(now);
  });
  if (data.departures.length > 0) {
    data.next = data.departures[0];
    data.upcoming = data.departures.slice(1, 5);
  } else {
    data.next = null;
    data.upcoming = [];
  }
  return data;
};

nsb.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var data = nsb.parse(vnode.attrs.data);
  var rows = data.upcoming.map(function (departure) {
    return m('tr', [
      m('td.destination', data.from),
      m('td', departure.departure.format('HH:mm')),
      m('td', m.trust('&mdash;')),
      m('td', departure.arrival.format('HH:mm'))
    ]);
  });
  return [
    m('p.fade', 'Neste tog til ' + data.to + ' går'),
    m('h1', data.next.departure.format('HH:mm')),
    m('h2', data.next.departure.fromNow()),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      data.updatedAt)
  ];
};
