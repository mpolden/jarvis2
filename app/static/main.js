var jrvs = jrvs || {};

jrvs.layout = function () {
  $('.gridster ul').gridster({
    widget_margins: [5, 5],
    widget_base_dimensions: [145, 145]
  });
};

jrvs.dispatch = function () {
  var source = new EventSource('/events');

  source.addEventListener('message', function (message) {
    var o = JSON.parse(message.data);

    if (typeof o === 'object' && Object.keys(o.body).length > 0) {
      var el = document.getElementById(o.widget);
      if (el === null) {
        return;
      }
      o.body.updatedAt = moment().format('HH:mm');
      var event = new CustomEvent(o.widget, {'detail': o.body});
      el.dispatchEvent(event);
    }
  }, false);
};

jrvs.truncate = function (s, n) {
  if (s.length > n) {
    return s.substring(0, n) + '...';
  }
  return s;
};

jrvs.subscribe = function (widget, namespace) {
  namespace = namespace || widget;
  if (typeof window[namespace].state.update !== 'function') {
    throw namespace + '.state.update is not a function';
  }
  var element = document.getElementById(widget);
  element.addEventListener(element.id, window[namespace].state.update);
};

jrvs.mount = function (elementId, namespace) {
  namespace = namespace || window[elementId];
  if (typeof namespace !== 'object') {
    throw 'expected namespace to be an object, but is ' + namespace;
  }
  var element = document.getElementById(elementId);
  if (element === null) {
    return;
  }
  m.mount(element, namespace);
};

document.addEventListener('DOMContentLoaded', function () {
  jrvs.layout();
  jrvs.dispatch();
});
