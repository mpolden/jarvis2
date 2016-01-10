(function () {
  'use strict';

  var nsb = {
    'el': document.getElementById('nsb')
  };

  nsb.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    nsb.el.addEventListener('nsb', function (event) {
      var body = event.detail;
      if (body.departures.length > 0) {
        body.next = body.departures[0];
        body.upcoming = body.departures.slice(1, 5);
      } else {
        body.next = null;
        body.upcoming = [];
      }
      ctrl.data = body;
      m.render(nsb.el, nsb.view(ctrl));
    });
  };

  nsb.view = function (c) {
    if (Object.keys(c.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    var rows = c.data.upcoming.map(function (departure) {
      return m('tr', [
        m('td', departure.departure),
        m('td', departure.arrival),
        m('td', departure.duration)
      ]);
    });
    return [
      m('p.fade', [
        'Neste tog fra ',
        m('em', c.data.from),
        ' til ',
        m('em', c.data.to),
        ' går ',
        m('em', c.data.date)
      ]),
      m('h1', c.data.next.departure),
      m('h2.fade', [
        'Ankomst: ',
        m('em', c.data.next.arrival),
        ' (',
        m('em', c.data.next.duration),
        ')'
      ]),
      m('table', [
        m('tr.fade', [
          m('th', 'Avgang'),
          m('th', 'Ankomst'),
          m('th', 'Reisetid')
        ])
      ].concat(rows)),
      m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
        c.data.updatedAt)
    ];
  };

  if (nsb.el !== null) {
    m.mount(nsb.el, nsb);
  }
})();
