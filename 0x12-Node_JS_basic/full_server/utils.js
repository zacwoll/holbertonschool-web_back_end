const fs = require('fs');

async function readDatabase(path) {
    if (!fs.existsSync(path)) {
        throw Error('Cannot load the database');
    }
    const data = await fs.promises.readFile(path, 'utf-8');
    const students = data.split('\r\n').slice(1)
    .map((student) => student.split(','))
    .map((student) => ({
      firstName: student[0],
      lastName: student[1],
      age: student[2],
      field: student[3],
    }));
    let fields = students.map(student => student.field);
    let unique_fields = new Set(fields);
    let students_by_field = {}
    for (field of unique_fields) {
      students_by_field[field] = [];
    }
    for (student of students) {
        students_by_field[student.field].push(student.firstName);
    }
    // console.log(students_by_field);
}

module.exports = readDatabase;