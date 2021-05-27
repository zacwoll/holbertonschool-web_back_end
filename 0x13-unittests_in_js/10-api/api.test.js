const { expect } = require("chai");
const request = require('request')
const url = 'http://localhost:7865';

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
});

describe('Available_Payments page', () => {
    it('GET /available_payments', (done) => {
        request(`${url}/available_payments`, (err, res, body) => {
            expect(res.statusCode).to.equal(200)
            expect(body).to.deep.equal(JSON.stringify({
                payment_methods: {
                    credit_cards: true,
                    paypal: false
                }
            }));
            done();
        });
    });
});

describe('Login page', () => {
    const options = {
        url: 'http://localhost:7865/login',
        method: 'POST',
        json: { 'userName': 'Betty' }
    }
    it('POST /login', (done) => {
        request(options, (err, res, body) => {
            expect(res.statusCode).to.equal(200);
            expect(body).to.equal('Welcome Betty');
            done();
        });
    });
});
