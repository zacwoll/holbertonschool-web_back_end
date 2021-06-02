const redis = require('redis');

const client = redis.createClient();
const { promisify } = require('util');

const promisifiedSet = promisify(client.set).bind(client);
const promisifiedGet = promisify(client.get).bind(client);

function reserveSeat(number) {
  promisifiedSet('available_seats', number);
}

async function getCurrentAvailableSeats() {
  return promisifiedGet('available_seats');
}

client.on('error', (err) => console.error(`Redis client not connected to the server: ${err.message}`));
client.on('connect', () => {
  console.log('Redis client connected to the server');
  reserveSeat(50);
});

const kue = require('kue');

const queue = kue.createQueue();

const express = require('express');

const app = express();
const port = 1245;
let reservationEnabled = true;

app.listen(port, console.log(`Stock app listening at http://localhost:${port}`));

app.get('/available_seats', async (req, res) => {
  const seats = await getCurrentAvailableSeats();
  res.json({ numberOfAvailableSeats: seats });
});

app.get('/reserve_seat', (req, res) => {
  if (!reservationEnabled) {
    res.json({ status: 'Reservation are blocked' });
    return;
  }
  const newJob = queue.create('reserve_seat').save((err) => {
    if (err) res.json({ status: 'Reservation failed' });
    res.json({ status: 'Reservation in process' });
  });
  newJob.on('complete', () => console.log(`Seat reservation job ${newJob.id} completed`))
    .on('failed', (err) => console.log(`Seat reservation job ${newJob.id} failed: ${err}`));
});

app.get('/process', (req, res) => {
  queue.process('reserve_seat', async (job, done) => {
    const seatCount = await getCurrentAvailableSeats();
    if (seatCount > 0) reserveSeat(seatCount - 1);
    if ((seatCount - 1) === 0) reservationEnabled = false;
    if ((seatCount - 1) >= 0) done();
    else return done(new Error('Not enough seats available'));
    return done();
  });
  res.json({ status: 'Queue processing' });
});
