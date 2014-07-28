var calendar = {
  'el': document.getElementById('calendar')
};

calendar.controller = function () {
  var ctrl = this;
  ctrl.data = {};
  calendar.el.addEventListener('calendar', function (event) {
    var body = event.detail;
    if (body.events.length === 0) {
      return;
    }
    body.events.forEach(function (e) {
      e.date = moment(e.date).lang('nb');
    });
    var eventDate = body.events[0].date,
        now = moment();
    if (eventDate.isBefore(now) || eventDate.isSame(now, 'day')) {
      body.today = body.events.shift() || null;
    } else {
      body.today = null;
    }
    body.events = body.events.slice(0, 4);
    ctrl.data = body;
    m.render(calendar.el, calendar.view(ctrl));
  });
};

calendar.view = function (c) {
  if (Object.keys(c.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = c.data.events.map(function (event) {
    return m('tr', [
      m('td', {'class': 'fade summary'}, jrvs.truncate(event.summary, 20)),
      m('td.start', event.date.format('DD. MM HH:mm'))
    ]);
  });
  return [
    m('p.fade', 'I dag:'),
    m('h1', c.data.today ? c.data.today.date.format('HH:mm') : '--:--'),
    m('h2', c.data.today ?
      jrvs.truncate(c.data.today.summary, 20) : 'Ingen hendelser'),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      c.data.updatedAt)
  ];
};

if (calendar.el !== null) {
  m.module(calendar.el, calendar);
}
