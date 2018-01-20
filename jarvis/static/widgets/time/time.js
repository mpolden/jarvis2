var time = time || {};

time.update = function (vnode) {
  vnode.state.data = {now: moment().locale('nb')};
  m.render(vnode.attrs.el, m(time, vnode.attrs));
};

time.view = function (vnode) {
  var state = vnode.state.data;
  return [
    m('h1', state.now.format('HH:mm')),
    m('h2', state.now.format('dddd')),
    m('h3', state.now.format('D. MMMM YYYY'))
  ];
};

time.oninit = time.update;

time.oncreate = function (vnode) {
  setInterval(function () {
    time.update(vnode);
  }, 500);
};
