const Utils = require('./utils');

module.exports = function sendPaymentRequestToApi(totalAmount, totalShipping) {
  const finalTotal = Utils.calculateNumber('SUM', totalAmount, totalShipping);
  console.log(`The total is: ${finalTotal}`);
};
