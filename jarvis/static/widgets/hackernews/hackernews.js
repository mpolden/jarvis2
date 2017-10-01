var hn = hn || {};

hn.parseState = function (data) {
  var body = data;
  if (body.items && body.items.length > 0) {
    body.items = body.items.slice(0, 10);
  }
  return body;
};

hn.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = hn.parseState(vnode.attrs.data);
  var rows = state.items.map(function (item) {
    return m('tr', [
      m('td.title', jrvs.truncate(item.title, 24)),
      m('td.points', item.points)
    ]);
  });
  return [
    m('p.fade', 'Hacker News'),
    m('table', rows),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
