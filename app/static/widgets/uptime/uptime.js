var uptime = uptime || {};

uptime.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
    body.hosts.forEach(function (host) {
      host.active = host.active ? 'aktiv' : 'inaktiv';
    });
    uptime.state.data = body;
    m.redraw();
  }
};

uptime.view = function () {
  if (Object.keys(uptime.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = uptime.state.data.hosts.map(function (host) {
    return m('tr', [
      m('td.label', host.label),
      m('td.active', host.active)
    ]);
  });
  return [
    m('p.fade', 'Enheter'),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      uptime.state.data.updatedAt)
  ];
};

uptime.oncreate = function () {
  jrvs.subscribe('uptime');
};

jrvs.mount('uptime');
