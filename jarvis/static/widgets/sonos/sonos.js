var sonos = sonos || {};

sonos.stateName = function (state) {
  if (state === 'PAUSED_PLAYBACK') {
    return 'pause';
  }
  if (state === 'PLAYING') {
    return 'spiller av';
  }
  if (state === 'STOPPED') {
    return 'stoppet';
  }
  return '';
};

sonos.applyAlbumArt = function (vnode) {
  var defaultValue = 'none';
  var image = defaultValue;
  var state = vnode.attrs.data;
  if (state.display_album_art && state.current && state.current.album_art) {
    image = 'url(' + state.current.album_art + ')';
  }
  vnode.attrs.el.style.backgroundImage = image;
  return image !== defaultValue;
};

sonos.view = function (vnode) {
  var hasAlbumArt = sonos.applyAlbumArt(vnode);
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var current = [];
  var state = vnode.attrs.data;
  if (Object.keys(state.current).length > 0) {
    var position = state.current.position + ' / ' + state.current.duration;
    if (state.state !== 'PLAYING') {
      position += ' (' + sonos.stateName(state.state) + ')';
    }
    var textClass = {'class': hasAlbumArt ? 'outline' : ''};
    current = [
      m('h1', textClass, jrvs.truncate(state.current.title, 28)),
      m('p.fade', state.current.artist.length > 0 ? 'av' : ''),
      m('h2', textClass, jrvs.truncate(state.current.artist, 20)),
      m('p.fade', m('small', position))
    ];
  }
  var next = [];
  if (Object.keys(state.next).length > 0) {
    next = [
      m('p.fade', m('small', 'Neste: ' + state.next.title)),
    ];
  }
  return [
    m('div', current),
    m('div', next),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
