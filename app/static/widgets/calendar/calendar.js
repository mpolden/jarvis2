var calendar = calendar || {};

calendar.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
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
    calendar.state.data = body;
    m.redraw();
  }
};

calendar.view = function () {
  if (Object.keys(calendar.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = calendar.state.data.events.map(function (event) {
    return m('tr', [
      m('td', {'class': 'fade summary'}, jrvs.truncate(event.summary, 19)),
      m('td.start', event.date.format('DD. MM HH:mm'))
    ]);
  });
  return [
    m('p.fade', 'I dag:'),
    m('h1', calendar.state.data.today ? calendar.state.data.today.date.format('HH:mm') : '--:--'),
    m('h2', calendar.state.data.today ?
      jrvs.truncate(calendar.state.data.today.summary, 20) : 'Ingen hendelser'),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      calendar.state.data.updatedAt)
  ];
};

calendar.oncreate = function () {
  jrvs.subscribe('calendar');
};

jrvs.mount('calendar');
