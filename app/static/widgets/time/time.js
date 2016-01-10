(function () {
  'use strict';

  var time = {
    'el': document.getElementById('time')
  };

  time.controller = function () {
    var ctrl = this;
    ctrl.now = moment().lang('nb');
    var setTime = function () {
      ctrl.now = moment().lang('nb');
      m.render(time.el, time.view(ctrl));
    };
    setInterval(setTime, 500);
  };

  time.view = function (ctrl) {
    return [
      m('h1', ctrl.now.format('HH:mm')),
      m('h2', ctrl.now.format('dddd')),
      m('p', ctrl.now.format('D. MMMM YYYY'))
    ];
  };

  if (time.el !== null) {
    m.mount(time.el, time);
  }
})();
