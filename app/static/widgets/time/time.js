var time = time || {};

time.state = {
  now: null,
  update: function () {
    time.state.now = moment().locale('nb');
    m.redraw();
  }
};

time.view = function () {
  return [
    m('h1', time.state.now.format('HH:mm')),
    m('h2', time.state.now.format('dddd')),
    m('p', time.state.now.format('D. MMMM YYYY'))
  ];
};

time.oninit = time.state.update;

time.oncreate = function () {
  setInterval(time.state.update, 500);
};

jrvs.mount('time');
