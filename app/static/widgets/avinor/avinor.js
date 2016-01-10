(function () {
  'use strict';

  var avinor = {
    'el': document.getElementById('avinor')
  };

  avinor.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    avinor.el.addEventListener('avinor', function (event) {
      var data = event.detail;

      data.flights = data.flights.map(function (f) {
        f.date = moment(f.schedule_time).lang('nb');
        return f;
      }).filter(function (f) {
        return f.date.isAfter();
      });
      data.next = data.flights.shift() || null;
      data.flights = data.flights.slice(0, 4);
      ctrl.data = data;

      m.render(avinor.el, avinor.view(ctrl));
    });
  };

  avinor.view = function (ctrl) {
    if (Object.keys(ctrl.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    var rows = ctrl.data.flights.map(function (flight) {
      return m('tr', [
        m('td', flight.flight_id),
        m('td', flight.date.format('D. MMM HH:mm'))
      ]);
    });
    return [
      m('p.fade', [
        'Neste fly (',
        m('em', ctrl.data.next.flight_id),
        ') fra ',
        m('em', ctrl.data.from),
        ' til ',
        m('em', ctrl.data.to),
        ' går ',
        m('em', ctrl.data.next.date.format('dddd, D. MMMM'))
      ]),
      m('h1', ctrl.data.next.date.format('HH:mm')),
      m('h2', ctrl.data.next.date.fromNow()),
      m('table', [
        m('tr.fade', [
          m('th', 'Flight'),
          m('th', 'Avgang')
        ])
      ].concat(rows)),
      m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
        ctrl.data.updatedAt)
    ];
  };

  if (avinor.el !== null) {
    m.mount(avinor.el, avinor);
  }
})();
