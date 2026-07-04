from sqlalchemy import func

from database.db import db
from models.marks import Mark
from models.student import Student
from models.subject import Subject


class DashboardService:
    @staticmethod
    def total_students():
        return Student.query.count()

    @staticmethod
    def total_subjects():
        return Subject.query.count()

    @staticmethod
    def total_marks():
        return Mark.query.count()

    @staticmethod
    def average_marks():
        avg = db.session.query(func.avg(Mark.marks)).scalar()
        return round(avg or 0, 2)

    @staticmethod
    def highest_marks():
        highest = db.session.query(func.max(Mark.marks)).scalar()
        return highest or 0

    @staticmethod
    def lowest_marks():
        lowest = db.session.query(func.min(Mark.marks)).scalar()
        return lowest or 0

    @staticmethod
    def recent_students(): ...

    @staticmethod
    def top_students():
        return (
            (db.session.query(Student, func.avg(Mark.marks).label("average")))
            .join(Mark)
            .group_by(Student.id)
            .order_by(func.avg(Mark.marks).desc())
            .limit(5)
            .all()
        )

    @staticmethod
    def subject_statistics():

        return (
            db.session.query(
                Subject.subject_name, func.avg(Mark.marks).label("average")
            )
            .join(Mark)
            .group_by(Subject.subject_name)
            .order_by(func.avg(Mark.marks).desc())
            .all()
        )

    @staticmethod
    def recent_students():

        return Student.query.order_by(Student.created_at.desc()).limit(5).all()

    @staticmethod
    def recent_marks():

        return Mark.query.order_by(Mark.id.desc()).limit(5).all()

    @staticmethod
    def grade_distribution():

        distribution = {"A+": 0, "A": 0, "B": 0, "C": 0, "D": 0, "F": 0}

        students = Student.query.all()

        for student in students:
            if not student.marks:
                continue

            average = sum(m.marks for m in student.marks) / len(student.marks)

            if average >= 90:
                distribution["A+"] += 1
            elif average >= 80:
                distribution["A"] += 1
            elif average >= 70:
                distribution["B"] += 1
            elif average >= 60:
                distribution["C"] += 1
            elif average >= 35:
                distribution["D"] += 1
            else:
                distribution["F"] += 1

        return distribution
