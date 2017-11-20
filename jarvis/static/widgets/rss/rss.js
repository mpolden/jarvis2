var rss = rss || {};

rss.parse = function (data) {
  var items = data.items.slice(0, 6).map(function (item) {
    return {'title': item.title, 'time': moment.unix(item.time).locale('nb')};
  });
  data.items = items;
  return data;
};

rss.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = rss.parse(vnode.attrs.data);
  var items = state.items.map(function (item) {
    return m('li', jrvs.truncate(item.title, 45),
             m('span', {class: 'fade age'}, ' — ' + item.time.fromNow(true))
            );
  });
  return [
    m('p.fade', state.title),
    m('ul', items),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
