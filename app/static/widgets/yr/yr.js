(function () {
  'use strict';

  var yr = {
    'el': document.getElementById('yr')
  };

  yr.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    yr.el.addEventListener('yr', function (event) {
      ctrl.data = event.detail;
      m.render(yr.el, yr.view(ctrl));
    });
  };

  yr.view = function (ctrl) {
    if (Object.keys(ctrl.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    return [
      m('p.fade', 'Været i ' + ctrl.data.today.location),
      m('h1', ctrl.data.today.temperature + '°'),
      m('p', ctrl.data.today.description),
      m('p.wind', ctrl.data.today.wind.description + ' (' +
        ctrl.data.today.wind.speed + ' m/s) fra ' +
        ctrl.data.today.wind.direction.toLowerCase()),
      m('p.tomorrow', 'I morgen: ' + ctrl.data.tomorrow.temperature +
        '° (' + ctrl.data.tomorrow.description.toLowerCase() + ')'),
      m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
        ctrl.data.updatedAt)
    ];
  };

  if (yr.el !== null) {
    m.mount(yr.el, yr);
  }
})();
