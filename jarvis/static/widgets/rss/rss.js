var rss = rss || {};

rss.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  var items = state.items.slice(0, 6).map(function (item) {
    return m('li', jrvs.truncate(item.title, 60));
  });
  return [
    m('p.fade', state.title),
    m('ul', items),
    m('p', {class: 'fade updated-at'}, 'Sist oppdatert: ' +
      state.updatedAt)
  ];
};
