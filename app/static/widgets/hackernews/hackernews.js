var hn = hn || {};

hn.state = {
  data: {},
  update: function (event) {
    var body = event.detail;
    if (body.items && body.items.length > 0) {
      body.items = body.items.slice(0, 10);
    }
    hn.state.data = body;
    m.redraw();
  }
};

hn.view = function () {
  if (Object.keys(hn.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = hn.state.data.items.map(function (item) {
    return m('tr', [
      m('td.title', jrvs.truncate(item.title, 24)),
      m('td.points', item.points)
    ]);
  });
  return [
    m('p.fade', 'Hacker News'),
    m('table', rows),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      hn.state.data.updatedAt)
  ];
};

hn.oncreate = function () {
  jrvs.subscribe('hackernews', hn);
};

jrvs.mount('hackernews', hn);
