var gmail = gmail || {};

gmail.state = {
  data: {},
  update: function (event) {
    gmail.state.data = event.detail;
    m.redraw();
  }
};

gmail.view = function () {
  if (Object.keys(gmail.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  return [
    m('h1', 'Uleste eposter'),
    m('p.fade', [
      m('span', gmail.state.data.email),
      m('br'),
      m('span', gmail.state.data.folder)
    ]),
    m('p.count', gmail.state.data.unread),
    m('p.fade', 'Totalt i ' + gmail.state.data.folder + ': ' + gmail.state.data.count),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      gmail.state.data.updatedAt)
  ];
};

gmail.oncreate = function () {
  jrvs.subscribe('gmail');
};

jrvs.mount('gmail');
