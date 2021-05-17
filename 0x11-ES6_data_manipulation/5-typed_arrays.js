export default function createInt8TypedArray(length, position, value) {
  const buffer = new ArrayBuffer(length);
  const dataView = new DataView(buffer);
  if (position < length) {
    dataView.setUint8(position, value);
  } else {
    throw Error('Position outside range');
  }
  return dataView;
}
