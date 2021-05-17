export const weakMap = new WeakMap();

export function queryAPI(endpoint) {
  const count = weakMap.get(endpoint);
  if (count === undefined) { weakMap.set(endpoint, 1); } else if (count + 1 >= 5) { throw Error('Endpoint load is high'); } else { weakMap.set(endpoint, count + 1); }
}
