var calendar = calendar || {};

calendar.parseState = function (data) {
  var body = data;
  if (body.events.length === 0) {
    return;
  }
  body.events.forEach(function (e) {
    e.date = moment(e.date).locale('nb');
  });
  var eventDate = body.events[0].date,
      now = moment();
  if (eventDate.isBefore(now) || eventDate.isSame(now, 'day')) {
    body.today = body.events.shift() || null;
  } else {
    body.today = null;
  }
  body.events = body.events.slice(0, 4);
  return body;
};

calendar.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = calendar.parseState(vnode.attrs.data);
  var rows = state.events.map(function (event) {
    return m('tr', [
      m('td', {'class': 'fade summary'}, jrvs.truncate(event.summary, 19)),
      m('td.start', event.date.format('DD. MM HH:mm'))
    ]);
  });
  return [
    m('p.fade', 'I dag:'),
    m('h1', state.today ? state.today.date.format('HH:mm') : '--:--'),
    m('h2', state.today ?
      jrvs.truncate(state.today.summary, 20) : 'Ingen hendelser'),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
