export default function iterateThroughObject(reportWithIterator) {
    let output = '';
    for (const item of reportWithIterator) {
        output += `${item} | `;
    }
    return output.slice(0, -3);
}
