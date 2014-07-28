(function () {
  'use strict';

  var atb = {
    'el': document.getElementById('atb')
  };

  atb.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    atb.el.addEventListener('atb', function (event) {
      var body = event.detail;
      body.departures.forEach(function (d) {
        var departureTime = moment(d.registeredDepartureTime).lang('nb'),
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
      ctrl.data = body;
      m.render(atb.el, atb.view(ctrl));
    });
  };

  atb.view = function (c) {
    if (Object.keys(c.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    var rows = c.data.upcoming.map(function (departure) {
      return m('tr', [
        m('td', {'class': 'destination fade'}, departure.line + ' ' +
          departure.destination),
        m('td.time', departure.departureTime.format('HH:mm'))
      ]);
    });
    return [
      m('p.fade', 'Buss ' + c.data.next.line + ' til ' +
        c.data.next.destination + ' går'),
      m('h1', c.data.next.departureTime.format('HH:mm')),
      m('h2', c.data.next.departureTime.fromNow()),
      m('table', rows),
      m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
        c.data.updatedAt)
    ];
  };

  if (atb.el !== null) {
    m.module(atb.el, atb);
  }
})();
