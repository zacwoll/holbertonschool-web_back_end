const { expect } = require("chai");
const request = require('request');

describe('Index page', () => {
    describe('GET /', () => {
        it('checks output of GET /', (done) => {
            request('http://localhost:7865', (err, res, body) => {
                expect(res.statusCode).to.equal(200);
                expect(body).to.equal('Welcome to the payment system');
            }, done());
        });
    });

    describe('GET /cart/:id', () => {
        it('checks output of GET /cart/:id', (done) => {
            request('http://localhost:7865/cart/12', (err, res, body) => {
                expect(res.statusCode).to.equal(200);
                expect(body).to.equal('Payment methods for cart 12')
            }, done());
        });
    });

    describe('GET /cart/:id with id hello', () => {
        it('http://localhost:7865/cart/hello', (done) => {
            request('http://localhost:7865/cart/hello', (err, res, body) => {
                if (res) {
                    expect(res.statusCode).to.equal(404);
                    expect(body).to.equal('<!DOCTYPE html>\n' +
                    '<html lang="en">\n' +
                    '<head>\n' +
                    '<meta charset="utf-8">\n' +
                    '<title>Error</title>\n' +
                    '</head>\n' +
                    '<body>\n' +
                    '<pre>Cannot GET /cart/hello</pre>\n' +
                    '</body>\n' +
                    '</html>\n');
                }
            }, done());
        });
    });
});