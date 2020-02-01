var flybussen = flybussen || {};

flybussen.parse = function (data) {
  var now = moment();
  var result = {};
  var departures = data.departures.map(function (d) {
    d.departure_time = moment.unix(d.departure_time).locale('nb');
    return d;
  }).filter(function (d) {
    // Ignore departures that have passed
    return d.departure_time.isAfter(now);
  });
  result.to = data.to;
  result.from = data.from;
  result.next = null;
  if (departures.length > 0) {
    result.next = departures[0];
  }
  result.upcoming = departures.slice(1, 5);
  result.updatedAt = data.updatedAt;
  return result;
};

flybussen.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var data = flybussen.parse(vnode.attrs.data);
  if (data.next === null) {
    return m('p', 'Waiting for data');
  }
  var rows = data.upcoming.map(function (departure) {
    return m('tr', [
      m('td.destination', departure.stop_name),
      m('td.time', departure.departure_time.format('HH:mm'))
    ]);
  });
  return [
    m('p.fade', 'Flybuss til ' + data.to + ' går'),
    m('h1', data.next.departure_time.format('HH:mm')),
    m('h2', data.next.departure_time.fromNow()),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' + data.updatedAt)
  ];
};
