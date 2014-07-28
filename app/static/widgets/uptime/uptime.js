var uptime = {
  'el': document.getElementById('uptime')
};

uptime.controller = function () {
  var ctrl = this;
  ctrl.data = {};
  uptime.el.addEventListener('uptime', function (event) {
    var body = event.detail;
    body.hosts.forEach(function (host) {
      host.active = host.active ? 'aktiv' : 'inaktiv';
    });
    ctrl.data = body;
    m.render(uptime.el, uptime.view(ctrl));
  });
};

uptime.view = function (c) {
  if (Object.keys(c.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = c.data.hosts.map(function (host) {
    return m('tr', [
      m('td.label', host.label),
      m('td.active', host.active)
    ]);
  });
  return [
    m('p.fade', 'Enheter'),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      c.data.updatedAt)
  ];
};

if (uptime.el !== null) {
  m.module(uptime.el, uptime);
}
