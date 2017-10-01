var time = time || {};

time.update = function (vnode) {
  vnode.state.data = {now: moment().locale('nb')};
  m.redraw();
};

time.view = function (vnode) {
  var state = vnode.state.data;
  return [
    m('h1', state.now.format('HH:mm')),
    m('h2', state.now.format('dddd')),
    m('p', state.now.format('D. MMMM YYYY'))
  ];
};

time.oninit = time.update;

time.oncreate = function (vnode) {
  setInterval(function () {
    time.update(vnode);
  }, 500);
};

(function () {
  var el = document.querySelector('[data-widget="time"]');
  if (el !== null) {
    m.mount(el, time);
  }
})();
