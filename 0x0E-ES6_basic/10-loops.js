export default function appendToEachArrayValue(array, appendString) {
    let a = []
    for (const idx of array) {
      a.push(appendString + idx);
    }
  
    return a;
  }
