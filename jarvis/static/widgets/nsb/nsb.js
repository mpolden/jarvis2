var nsb = nsb || {};

nsb.parse = function (data) {
  var body = data;
  body.departures.forEach(function (d) {
    d.duration = moment.duration(d.duration, 'seconds').locale('nb').humanize();
    d.departure = moment(d.departure).format('HH:mm');
    d.arrival = moment(d.arrival).format('HH:mm');
  });
  if (body.departures.length > 0) {
    body.next = body.departures[0];
    body.upcoming = body.departures.slice(1, 5);
  } else {
    body.next = null;
    body.upcoming = [];
  }
  return body;
};

nsb.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var data = nsb.parse(vnode.attrs.data);
  var rows = data.upcoming.map(function (departure) {
    return m('tr', [
      m('td', departure.departure),
      m('td', departure.arrival),
      m('td', departure.duration)
    ]);
  });
  return [
    m('p.fade', [
      'Neste tog fra ',
      m('em', data.from),
      ' til ',
      m('em', data.to),
      ' går ',
      m('em', data.date)
    ]),
    m('h1', data.next.departure),
    m('h2.fade', [
      'Ankomst: ',
      m('em', data.next.arrival),
      ' (',
      m('em', data.next.duration),
      ')'
    ]),
    m('table', [
      m('tr.fade', [
        m('th', 'Avgang'),
        m('th', 'Ankomst'),
        m('th', 'Reisetid')
      ])
    ].concat(rows)),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      data.updatedAt)
  ];
};
