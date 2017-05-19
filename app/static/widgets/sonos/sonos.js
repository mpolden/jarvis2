var sonos = sonos || {};

sonos.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
    body.state = sonos.stateName(body.state);
    sonos.state.data = body;
    m.redraw();
  }
};

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

sonos.view = function () {
  if (Object.keys(sonos.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var current = [];
  if (sonos.state.data.current) {
    current = [
      m('h1', jrvs.truncate(sonos.state.data.current.artist, 14) + ' - ' +
        jrvs.truncate(sonos.state.data.current.title, 16)),
      m('p', {'class': 'fade duration'}, sonos.state.data.current.position + ' / ' +
        sonos.state.data.current.duration)
    ];
  }
  var next = [];
  if (sonos.state.data.next) {
    next = [
      m('p', {'class': 'fade next'}, 'Neste i kø:'),
      m('p', jrvs.truncate(sonos.state.data.next.artist, 15) + ' - ' +
        jrvs.truncate(sonos.state.data.next.title, 20))
    ];
  }
  return [
    m('p.fade', sonos.state.data.state),
    m('div', current),
    m('div', next),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      sonos.state.data.updatedAt)
  ];
};

sonos.oncreate = function () {
  jrvs.subscribe('sonos');
};

jrvs.mount('sonos');
