var email = email || {};

email.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  return [
    m('h1', 'Uleste eposter'),
    m('p.fade', [
      m('span', state.email),
      m('br'),
      m('span', state.folder)
    ]),
    m('p.count', state.unread),
    m('p.fade', 'Totalt i ' + state.folder + ': ' + state.count),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
