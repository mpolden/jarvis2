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
  if (state.current) {
    current = [
      m('h1', jrvs.truncate(state.current.artist, 14) + ' - ' +
        jrvs.truncate(state.current.title, 16)),
      m('p', {'class': 'fade duration'}, state.current.position + ' / ' +
        state.current.duration)
    ];
  }
  var next = [];
  if (state.next) {
    next = [
      m('p', {'class': 'fade next'}, 'Neste i kø:'),
      m('p', jrvs.truncate(state.next.artist, 15) + ' - ' +
        jrvs.truncate(state.next.title, 20))
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
