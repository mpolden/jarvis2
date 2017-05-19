var stockquotes = stockquotes || {};

stockquotes.state = {
  data: {},
  update: function (event) {
    stockquotes.state.data = event.detail;
    m.redraw();
  }
};

stockquotes.view = function () {
  if (Object.keys(stockquotes.state.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var rows = stockquotes.state.data.map(function (quote) {
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
      stockquotes.state.data.updatedAt)
  ];
};

stockquotes.oncreate = function () {
  jrvs.subscribe('stockquotes');
};

jrvs.mount('stockquotes');
