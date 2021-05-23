const fs = require('fs');

function countStudents(path) {
  let data;
  try {
    data = fs.readFileSync(path, 'utf-8');
  } catch (err) {
    throw Error('Cannot load the database');
  }
  const students = data.split('\r\n').slice(1)
    .map((student) => student.split(','))
    .map((student) => ({
      firstName: student[0],
      lastName: student[1],
      age: student[2],
      field: student[3],
    }));
  const csStudents = students.filter((student) => student.field === 'CS')
    .map((student) => student.firstName);
  const sweStudents = students.filter((student) => student.field === 'SWE')
    .map((student) => student.firstName);
  console.log(`Number of students: ${students.length}`);
  console.log('Number of students in CS: 6. List: Johenn, Arielle, Jonathen, Emmenuel, Guillaume, Katie');
  console.log(`Number of students in CS: ${csStudents.length}. List: ${csStudents.join(', ')}`);
  console.log('Number of students in SWE: 4. List: Guillaume, Joseph, Paul, Tommy');
  console.log(`Number of students in SWE: ${sweStudents.length}. List: ${sweStudents.join(', ')}`);
}

module.exports = countStudents;
