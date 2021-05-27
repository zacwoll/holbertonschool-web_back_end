const { expect } = require("chai");
const request = require('request')

describe('Index page', () => {
	describe('GET /', () => {
		it('checks output of GET /', (done) => {
			request('http://localhost:7865/', (error, response, body) => {
				expect(response.statusCode).to.equal(200)
				expect(body).to.equal('Welcome to the payment system')
			}, done())
		})
	})

	describe('GET /cart/:id', () => {
		it('checks output of curling server for index page with valid cart number', (done) => {
			request('http://localhost:7865/cart/12', (error, response, body) => {
				expect(response.statusCode).to.equal(200)
				expect(body).to.equal('Payment methods for cart 12')
			}, done())
		})
	})

	describe('GET /cart/hello', () => {
		it('checks output of curling server for index page with invalid cart number', (done) => {
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
			}, done())
		})
	})
})

describe('Login page', () => {
	describe('GET /login', () => {
		it('checks output of curling login page with userName data', (done) => {
			const options = {
				url: 'http://localhost:7865/login',
				method: 'POST',
				json: { 'userName': 'Betty' }
			}
			request(options, (error, response, body) => {
				expect(response.statusCode).to.equal(200)
				expect(body).to.equal('Welcome Betty')
			}, done())
		})
	})
})


describe('Available payments page', () => {
	describe('GET /available_payments', () => {
		it('checks output of curling available_payments page', (done) => {
			request('http://localhost:7865/available_payments', (error, response, body) => {
				expect(response.statusCode).to.equal(200)
				expect(body).to.deep.equal(JSON.stringify({
					payment_methods: {
						credit_cards: true,
						paypal: false
					}
				}))
			}, done())
		})
	})
})