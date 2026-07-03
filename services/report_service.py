from sqlalchemy import func

from models.student import Student
from models.marks import Mark


class ReportService:

    @staticmethod
    def get_student_report(student_id):

        student = Student.query.get_or_404(student_id)

        marks = student.marks

        total = sum(mark.marks for mark in marks)

        average = round(
            total / len(marks), 2
        ) if marks else 0

        grade = ReportService.calculate_grade(average)

        result = "PASS" if average >= 35 else "FAIL"

        return {
            "student": student,
            "marks": marks,
            "total": total,
            "average": average,
            "grade": grade,
            "result": result
        }

    @staticmethod
    def calculate_grade(avg):

        if avg >= 90:
            return "A+"

        elif avg >= 80:
            return "A"

        elif avg >= 70:
            return "B"

        elif avg >= 60:
            return "C"

        elif avg >= 35:
            return "D"

        return "F"