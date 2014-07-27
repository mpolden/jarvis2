/* jshint unused: false */
(function () {
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
})();

var jrvs = {
  'truncate': function (s, n) {
    if (s.length > n) {
      return s.substring(0, n) + '...';
    }
    return s;
  }
};
