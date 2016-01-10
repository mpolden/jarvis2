(function () {
  'use strict';

  var stockquotes = {
    'el': document.getElementById('stockquotes')
  };

  stockquotes.controller = function () {
    var ctrl = this;
    ctrl.data = {};
    stockquotes.el.addEventListener('stockquotes', function (event) {
      ctrl.data = event.detail;
      m.render(stockquotes.el, stockquotes.view(ctrl));
    });
  };

  stockquotes.view = function (ctrl) {
    if (Object.keys(ctrl.data).length === 0) {
      return m('p', 'Waiting for data');
    }
    var rows = ctrl.data.map(function (quote) {
      return m('tr', [
        m('td', quote.symbol),
        m('td', quote.ask),
        m('td', quote.change + ' (' + quote.percent_change + ')')
      ]);
    });
    return [
      m('h1', 'Stock quotes'),
      m('table', [
        m('tr.fade', [
          m('th', 'Ticker'),
          m('th', 'Price'),
          m('th', 'Change')
        ])
      ].concat(rows)),
      m('p', {'class': 'fade updated-at'}, 'Sist oppdatert: ' +
        ctrl.data.updatedAt)
    ];
  };

  if (stockquotes.el !== null) {
    m.mount(stockquotes.el, stockquotes);
  }
})();
