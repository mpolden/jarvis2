var stockquotes = stockquotes || {};

stockquotes.view = function (vnode) {
  if (Object.keys(vnode.attrs.data).length === 0) {
    return m('p', 'Waiting for data');
  }
  var state = vnode.attrs.data;
  var rows = state.map(function (quote) {
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
      state.updatedAt)
  ];
};
