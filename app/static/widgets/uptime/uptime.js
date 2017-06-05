var uptime = uptime || {};

uptime.parseState = function (data) {
  var body = data;
  body.hosts.forEach(function (host) {
    host.active = host.active ? 'aktiv' : 'inaktiv';
  });
  return body;
};

uptime.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = uptime.parseState(vnode.attrs.data);
  var rows = state.hosts.map(function (host) {
    return m('tr', [
      m('td.label', host.label),
      m('td.active', host.active)
    ]);
  });
  return [
    m('p.fade', 'Enheter'),
    m('table', rows),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
