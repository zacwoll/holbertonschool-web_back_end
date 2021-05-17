export default function updateStudentGradeByCity(students, city, newGrades) {
  return students.filter((student) => student.location === city)
    .map((student) => {
      let newGrade = 'N/A';
      newGrades.forEach((grade) => {
        if (grade.studentId === student.id) {
          newGrade = grade.grade;
        }
      });
      return { ...student, grade: newGrade };
    });
}
