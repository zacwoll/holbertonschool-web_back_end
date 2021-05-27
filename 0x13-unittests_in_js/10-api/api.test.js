const { expect } = require("chai");
const request = require('request')

describe('Index page', () => {
    it('GET /', (done) => {
        request('http://localhost:7865/', (error, response, body) => {
            expect(response.statusCode).to.equal(200)
            expect(body).to.equal('Welcome to the payment system')
        }, done())
    })

	it('GET /cart/:id', (done) => {
		request('http://localhost:7865/cart/12', (error, response, body) => {
			expect(response.statusCode).to.equal(200)
			expect(body).to.equal('Payment methods for cart 12')
		}, done())
	})

	it('GET /cart/hello', (done) => {
        request('http://localhost:7865/cart/hello', (error, response, body) => {
            if (response) {
                expect(response.statusCode).to.equal(404)
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

    it('POST /login', (done) => {
        const options = {
            url: 'http://localhost:7865/login',
            method: 'POST',
            json: { 'userName': 'Betty' }
        }
        request(options, (error, response, body) => {
            expect(response.statusCode).to.equal(200)
            expect(body).to.equal('Welcome Betty')
        }, done());
    });

    it('GET /available_payments', (done) => {
        request('http://localhost:7865/available_payments', (error, response, body) => {
            expect(response.statusCode).to.equal(200)
            expect(body).to.deep.equal(JSON.stringify({
                payment_methods: {
                    credit_cards: true,
                    paypal: false
                }
            }));
        }, done());
    });
});
