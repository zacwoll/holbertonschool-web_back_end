const { expect } = require('chai');
const sinon = require('sinon');

const getPaymentTokenFromApi = require('./6-payment_token');

describe('getPaymentTokenFromApi', () => {
  it('checks output of getPaymentTokenFromApi with true as success', (done) => {
    getPaymentTokenFromApi(true)
      .then((res) => {
        expect(res).to.deep.equal({ data: 'Successful response from the API' });
      }).then(done);
  });
  it('checks output of getPaymentTokenFromApi with false as success', () => {
    expect(getPaymentTokenFromApi(false)).to.be.undefined;
  });
});
