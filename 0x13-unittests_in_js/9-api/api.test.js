const { expect } = require("chai");
const request = require('request');
const url = 'http://localhost:7865';

describe('Index page', () => {
    it('GET / exists and outputs', (done) => {
        request(url, (err, res, body) => {
            expect(res.statusCode).to.equal(200);
            expect(body).to.equal('Welcome to the payment system');
            done();
        });
    });

    it('GET /cart/:id', (done) => {
        request(`${url}/cart/12`, (err, res, body) => {
            expect(res.statusCode).to.equal(200);
            expect(body).to.equal('Payment methods for cart 12');
            done();
        });
    });

    it('GET /cart/:id with id hello', (done) => {
        request(`${url}/cart/hello`, (err, res, body) => {
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
            done();
        });
    });
});