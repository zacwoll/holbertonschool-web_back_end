const fs = require('fs');

function countStudents(path) {
  let data;
  try {
    data = fs.readFileSync(path, 'utf-8');
  } catch (err) {
    throw Error('Cannot load the database');
  }
  const students = data.split('\n')
    .map((student) => student.split(','))
    .filter((student) => student.length > 1 && student[0] !== 'firstname')
    .map((student) => ({
      firstName: student[0],
      lastName: student[1],
      age: student[2],
      field: student[3].slice(0, -1),
    }));
  const csStudents = students.filter((student) => student.field === 'CS')
    .map((student) => student.firstName);
  const sweStudents = students.filter((student) => student.field === 'SWE')
    .map((student) => student.firstName);
  console.log(`Number of students: ${students.length}`);
  console.log(`Number of students in CS: ${csStudents.length}. List: ${csStudents.join(', ')}`);
  console.log(`Number of students in SWE: ${sweStudents.length}. List: ${sweStudents.join(', ')}`);
}

module.exports = countStudents;
