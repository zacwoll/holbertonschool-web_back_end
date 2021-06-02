const kue = require('kue');

const queue = kue.createQueue();
const jobObj = {
  phoneNumber: '123-456-7890',
  message: 'Hey, it\'s me!',
};
const job = queue.create('push_notification_code', jobObj).save();

job.on('enqueue', () => console.log(`Notification job created: ${job.id}`))
  .on('complete', () => console.log('Notification job completed'))
  .on('failed', () => console.log('Notification job failed'));
