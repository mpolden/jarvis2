var sonos = sonos || {};

sonos.stateName = function (state) {
  if (state === 'PAUSED_PLAYBACK') {
    return 'Pause:';
  }
  if (state === 'PLAYING') {
    return 'Spiller av:';
  }
  if (state === 'STOPPED') {
    return 'Stoppet';
  }
  return '';
};

sonos.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var current = [];
  var state = vnode.attrs.data;
  state.state = sonos.stateName(state.state);
  if (Object.keys(state.current).length > 0) {
    current = [
      m('h1', jrvs.truncate(state.current.title, 28)),
      m('p.fade', 'av'),
      m('h2', jrvs.truncate(state.current.artist, 20)),
      m('p.fade',
        m('small', state.current.position + ' / ' + state.current.duration)
       )
    ];
  }
  var next = [];
  if (Object.keys(state.next).length > 0) {
    next = [
      m('p.fade', m('small', 'Neste: ' + state.next.title)),
    ];
  }
  return [
    m('p.fade', state.state),
    m('div', current),
    m('div', next),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
