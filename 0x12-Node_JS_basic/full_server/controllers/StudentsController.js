const readDatabase = require('../utils');

class StudentsController {
    static getAllStudents(request, response) {
        response.statusCode = 200;
        response.setHeader('Content-Type', 'text/plain');
        // readDatabase returns { 'CS': ['Zac', 'Trevor', 'Spencer'] }
        await readDatabase('../../database.csv').then((data) => {
            response.write('This is the list of our students\n');
            response.write(`Number of students: \n`);
            response.write(`Number of students in CS: . List: \n`);
            response.write(`Number of students in SWE: . List: `);
            response.end();
        }).catch((err) => response.send(err.message));
    }
    static getAllStudentsByMajor(request, response, major) {
        response.statusCode = 200;
        response.setHeader('Content-Type', 'text/plain');
        await readDatabase('../../database.csv').then((data) => {
            response.write('This is the list of our students\n');
            response.write(`List: \n`);
            response.write(`List: `);
            response.end();
        }).catch((err) => response.send(err.message));
    }
}
