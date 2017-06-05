var yr = yr || {};

yr.formatWind = function (wind) {
  if (wind === null) {
    return '';
  }
  return wind.description + ' (' +
    wind.speed + ' m/s) fra ' +
    wind.direction.toLowerCase();
};

yr.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  return [
    m('p.fade', 'Været i ' + state.today.location),
    m('h1', state.today.temperature + '°'),
    m('p', state.today.description),
    m('p.wind', yr.formatWind(state.today.wind)),
    m('p.tomorrow', 'I morgen: ' + state.tomorrow.temperature +
      '° (' + state.tomorrow.description.toLowerCase() + ')'),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
