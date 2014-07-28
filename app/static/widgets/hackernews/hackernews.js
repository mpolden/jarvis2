var hn = {
  'el': document.getElementById('hackernews')
};

hn.controller = function () {
  this.data = {};
  hn.el.addEventListener('hackernews', function (event) {
    var body = event.detail;
    if (body.items && body.items.length > 0) {
      body.items = body.items.slice(0, 10);
    }
    this.data = body;
    m.render(hn.el, hn.view(this));
  });
};

hn.view = function (c) {
  if (Object.keys(c.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = c.data.items.map(function (item) {
    return m('tr', [
      m('td.title', jrvs.truncate(item.title, 24)),
      m('td.points', item.points)
    ]);
  });
  return [
    m('p.fade', 'Hacker News'),
    m('table', rows),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      c.data.updatedAt)
  ];
};

if (hn.el !== null) {
  m.module(hn.el, hn);
}
