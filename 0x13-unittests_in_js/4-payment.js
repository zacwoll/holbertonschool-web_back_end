const Utils = require('./utils');

export default function sendPaymentRequestToApi(totalAmount, totalShipping) {
  const finalTotal = Utils.calculateNumber('SUM', totalAmount, totalShipping);
  console.log(`The total is: ${finalTotal}`);
}
