(function () {
  'use strict';

  var {{ name }} = {
    'el': document.getElementById('{{ name }}')
  };

  {{ name }}.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    {{ name }}.el.addEventListener('{{ name }}', function (event) {
      ctrl.data = event.detail;
      m.render({{ name }}.el, {{ name }}.view(ctrl));
    });
  };

  {{ name }}.view = function (ctrl) {
    if (Object.keys(ctrl.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    return [
      m('pre', JSON.stringify(ctrl.data, null, '  '))
    ];
  };

  if ({{ name }}.el !== null) {
    m.module({{ name }}.el, {{ name }});
  }
})();
