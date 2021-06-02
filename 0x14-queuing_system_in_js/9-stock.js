const express = require('express');
const redis = require('redis');
const { promisify } = require('util');

const app = express();
const port = 1245;
const client = redis.createClient();

const promisifiedSet = promisify(client.set).bind(client);
const asyncGet = promisify(client.get).bind(client);
const listProducts = [
  {
    itemId: 1, itemName: 'Suitcase 250', price: 50, initialAvailableQuantity: 4,
  },
  {
    itemId: 2, itemName: 'Suitcase 450', price: 100, initialAvailableQuantity: 10,
  },
  {
    itemId: 3, itemName: 'Suitcase 650', price: 350, initialAvailableQuantity: 2,
  },
  {
    itemId: 4, itemName: 'Suitcase 1050', price: 50, initialAvailableQuantity: 5,
  },
];

function getItemById(id) {
  return listProducts.filter((product) => product.itemId === id)[0];
}

function reserveStockById(itemId, stock) {
  promisifiedSet(`item.${itemId}`, stock);
}
async function getCurrentReservedStockById(itemId) {
  return asyncGet(`item.${itemId}`);
}

app.listen(port, console.log(`Stock app listening at http://localhost:${port}`));
app.get('/list_products', (req, res) => res.json(listProducts));
app.get('/list_products/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  const currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock === null) {
    await reserveStockById(itemId, product.initialAvailableQuantity);
    product.currentQuantity = product.initialAvailableQuantity;
  } else product.currentQuantity = currentStock;
  res.json(product);
});

app.get('/reserve_product/:itemId', async (req, res) => {
  const itemId = parseInt(req.params.itemId, 10);
  const product = getItemById(itemId);
  if (!product) {
    res.json({ status: 'Product not found' });
    return;
  }
  const currentStock = await getCurrentReservedStockById(itemId);
  if (currentStock === null) {
    await reserveStockById(itemId, product.initialAvailableQuantity - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  } else if (currentStock > 0) {
    await reserveStockById(itemId, currentStock - 1);
    res.json({ status: 'Reservation confirmed', itemId });
  } else res.json({ status: 'Not enough stock available', itemId });
});

client.on('error', (err) => console.error(`Redis client not connected to the server: ${err.message}`));
client.on('connect', () => console.log('Redis client connected to the server'));
