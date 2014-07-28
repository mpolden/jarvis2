(function () {
  'use strict';

  var gmail = {
    'el': document.getElementById('gmail')
  };

  gmail.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    gmail.el.addEventListener('gmail', function (event) {
      ctrl.data = event.detail;
      m.render(gmail.el, gmail.view(ctrl));
    });
  };

  gmail.view = function (c) {
    if (Object.keys(c.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    return [
      m('h1', 'Uleste eposter'),
      m('p.fade', [
        m('span', c.data.email),
        m('br'),
        m('span', c.data.folder)
      ]),
      m('p.count', c.data.unread),
      m('p.fade', 'Totalt i ' + c.data.folder + ': ' + c.data.count),
      m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
        c.data.updatedAt)
    ];
  };

  if (gmail.el !== null) {
    m.module(gmail.el, gmail);
  }
})();
