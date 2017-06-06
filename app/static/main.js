var jrvs = jrvs || {};

jrvs.subscribe = function () {
  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    var o = JSON.parse(message.data);

    if (typeof o === 'object' && Object.keys(o.body).length > 0) {
      var el = document.querySelector('[data-job="' + o.widget + '"]');
      // If no specific job name is given, just use widget name for the job name
      if (el === null) {
        el = document.querySelector('[data-widget="' + o.widget + '"]');
      }
      if (el === null) {
        return;
      }
      o.body.updatedAt = moment().format('HH:mm');
      m.render(el, m(window[el.dataset.widget], {data: o.body}));
    }
  }, false);
};

jrvs.truncate = function (s, n) {
  if (s.length > n) {
    return s.substring(0, n) + '...';
  }
  return s;
};

document.addEventListener('DOMContentLoaded', jrvs.subscribe);
