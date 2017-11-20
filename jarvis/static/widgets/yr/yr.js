var yr = yr || {};

yr.formatWind = function (wind) {
  if (wind === null) {
    return '';
  }
  return wind.description + ' (' +
    wind.speed + ' m/s) fra ' +
    wind.direction.toLowerCase();
};

yr.formatTemperature = function(temperature) {
  if (temperature === null) {
    temperature = '-';
  }
  return temperature + '°';
};

yr.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  return [
    m('p.fade', 'Været i ' + state.today.location),
    m('h1', yr.formatTemperature(state.today.temperature)),
    m('h2', state.today.description),
    m('p.wind', yr.formatWind(state.today.wind)),
    m('p.tomorrow', 'I morgen: ' +
      yr.formatTemperature(state.tomorrow.temperature) +
      '(' + state.tomorrow.description.toLowerCase() + ')'),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
