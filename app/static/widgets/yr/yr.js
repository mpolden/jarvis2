var yr = yr || {};

yr.state = {
  data: {},
  update: function (event) {
    yr.state.data = event.detail;
    m.redraw();
  }
};

yr.formatWind = function (wind) {
  if (wind === null) {
    return '';
  }
  return wind.description + ' (' +
    wind.speed + ' m/s) fra ' +
    wind.direction.toLowerCase();
};

yr.view = function () {
  if (Object.keys(yr.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  return [
    m('p.fade', 'Været i ' + yr.state.data.today.location),
    m('h1', yr.state.data.today.temperature + '°'),
    m('p', yr.state.data.today.description),
    m('p.wind', yr.formatWind(yr.state.data.today.wind)),
    m('p.tomorrow', 'I morgen: ' + yr.state.data.tomorrow.temperature +
      '° (' + yr.state.data.tomorrow.description.toLowerCase() + ')'),
    m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
      yr.state.data.updatedAt)
  ];
};

yr.oncreate = function () {
  jrvs.subscribe('yr');
};

jrvs.mount('yr');
