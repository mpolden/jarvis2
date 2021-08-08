var yr2 = yr2 || {};

yr2.formatWind = function (wind) {
  if (wind === null) {
    return '';
  }
  return wind.description + ' (' + wind.speed + ' m/s) fra ' + wind.direction;
};

yr2.symbolIcon = (symbol) => {
  return '/widget/yr2/' + symbol + '.png';
};

yr2.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  var table_week = state.week.forecast.map((forecast) => {
    var time = moment(forecast.time).local();
    return m('tr', [
      m('td', time.locale('nb').format('dddd')),
      m('td', forecast.temperature + '°'),
      m(
        'td',
        m('img', { src: yr2.symbolIcon(forecast.symbol) })
      ),
    ]);
  });
  var table_today = state.today.forecast.map((forecast) => {
    var time = moment(forecast.time).local();
    return m('tr', [
      m('td', time.format('HH:mm')),
      m('td', forecast.temperature + '°'),
      m(
        'td',
        m('img', {
          src: yr2.symbolIcon(forecast.symbol),
        })
      ),
    ]);
  });
  return [
    m('p.fade', 'Været i ' + state.today.location),
    m(
      'header',
      m(
        'h1',
        state.today.temperature + '°    ',
        m('img', {
          src: yr2.symbolIcon(state.today.symbol),
        })
      ),
      m('p.wind', yr2.formatWind(state.today.wind))
    ),
    m(
      'table.wrap',
      m('td', m('table.today', table_today)),
      m('td', m('table.week', table_week))
    ),
    m('p', { class: 'fade updated-at' }, 'Sist oppdatert: ' + state.updatedAt),
  ];
};
