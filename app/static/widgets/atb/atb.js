var atb = atb || {};

atb.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
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
    atb.state.data = body;
    m.redraw();
  }
};

atb.view = function () {
    if (Object.keys(atb.state.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    var rows = atb.state.data.upcoming.map(function (departure) {
      return m('tr', [
        m('td', {'class': 'destination fade'}, departure.line + ' ' +
          departure.destination),
        m('td.time', departure.departureTime.format('HH:mm'))
      ]);
    });
    return [
      m('p.fade', 'Buss ' + atb.state.data.next.line + ' til ' +
        atb.state.data.next.destination + ' går'),
      m('h1', atb.state.data.next.departureTime.format('HH:mm')),
      m('h2', atb.state.data.next.departureTime.fromNow()),
      m('table', rows),
      m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
        atb.state.data.updatedAt)
    ];
};

atb.oncreate = function () {
  jrvs.subscribe('atb');
};

jrvs.mount('atb');
