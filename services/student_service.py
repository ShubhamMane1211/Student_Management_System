from sqlalchemy import or_

from database.db import db
from models.student import Student


class StudentService:
    @staticmethod
    def create_student(form):

        # Check duplicate roll number
        existing = Student.query.filter_by(roll_no=form.roll_no.data).first()

        print(existing)

        if existing:
            return None

        student = Student(
            roll_no=form.roll_no.data,
            first_name=form.first_name.data,
            last_name=form.last_name.data,
            gender=form.gender.data,
            dob=form.dob.data,
            phone=form.phone.data,
            email=form.email.data,
            address=form.address.data,
            class_name=form.class_name.data,
            division=form.division.data,
            admission_date=form.admission_date.data,
        )

        db.session.add(student)
        db.session.commit()

        return student

    @staticmethod
    def get_student(student_id):
        return Student.query.get_or_404(student_id)

    @staticmethod
    def update_student(student, form):

        existing = Student.query.filter(
            Student.roll_no == form.roll_no.data, Student.id != student.id
        ).first()

        if existing:
            return None

        student.roll_no = form.roll_no.data
        student.first_name = form.first_name.data
        student.last_name = form.last_name.data
        student.gender = form.gender.data
        student.dob = form.dob.data
        student.phone = form.phone.data
        student.email = form.email.data
        student.address = form.address.data
        student.class_name = form.class_name.data
        student.division = form.division.data
        student.admission_date = form.admission_date.data

        db.session.commit()

        return student

    @staticmethod
    def delete_student(student_id):

        student = Student.query.get_or_404(student_id)

        db.session.delete(student)

        db.session.commit()

    @staticmethod
    def search_students(search):

        if not search:
            return Student.query.order_by(Student.roll_no).all()

        return (
            Student.query.filter(
                or_(
                    Student.roll_no.ilike(f"%{search}%"),
                    Student.first_name.ilike(f"%{search}%"),
                    Student.last_name.ilike(f"%{search}%"),
                    Student.email.ilike(f"%{search}%"),
                    Student.class_name.ilike(f"%{search}%"),
                )
            )
            .order_by(Student.roll_no)
            .all()
        )
