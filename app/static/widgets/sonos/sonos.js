(function () {
  'use strict';

  var sonos = {
    'el': document.getElementById('sonos')
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

  sonos.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    sonos.el.addEventListener('sonos', function (event) {
      var body = event.detail;
      body.state = sonos.stateName(body.state);
      ctrl.data = body;
      m.render(sonos.el, sonos.view(ctrl));
    });
  };

  sonos.view = function (c) {
    if (Object.keys(c.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    var current = [];
    if (c.data.current) {
      current = [
        m('h1', jrvs.truncate(c.data.current.artist, 14) + ' - ' +
          jrvs.truncate(c.data.current.title, 16)),
        m('p', {'class': 'fade duration'}, c.data.current.position + ' / ' +
          c.data.current.duration)
      ];
    }
    var next = [];
    if (c.data.next) {
      next = [
        m('p', {'class': 'fade next'}, 'Neste i kø:'),
        m('p', jrvs.truncate(c.data.next.artist, 15) + ' - ' +
          jrvs.truncate(c.data.next.title, 20))
      ];
    }
    return [
      m('p.fade', c.data.state),
      m('div', current),
      m('div', next),
      m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
        c.data.updatedAt)
    ];
  };

  if (sonos.el !== null) {
    m.mount(sonos.el, sonos);
  }
})();
