from sqlalchemy import or_

from database.db import db
from models.marks import Mark
from models.student import Student
from models.subject import Subject


class MarksService:
    @staticmethod
    def get_students():

        return Student.query.order_by(Student.first_name).all()

    @staticmethod
    def get_subjects():

        return Subject.query.order_by(Subject.subject_name).all()

    @staticmethod
    def create_mark(form):

        # Prevent duplicate marks for same student & subject
        existing = Mark.query.filter_by(
            student_id=form.student.data, subject_id=form.subject.data
        ).first()

        if existing:
            return None

        mark = Mark(
            student_id=form.student.data,
            subject_id=form.subject.data,
            marks=form.marks.data,
        )

        db.session.add(mark)
        db.session.commit()

        return mark

    @staticmethod
    def get_mark(mark_id):
        return Mark.query.get_or_404(mark_id)

    @staticmethod
    def update_mark(mark, form):

        existing = Mark.query.filter(
            Mark.student_id == form.student.data,
            Mark.subject_id == form.subject.data,
            Mark.id != mark.id,
        ).first()

        if existing:
            return None

        mark.student_id = form.student.data
        mark.subject_id = form.subject.data
        mark.marks = form.marks.data

        db.session.commit()

        return mark

    @staticmethod
    def delete_mark(mark_id):

        mark = Mark.query.get_or_404(mark_id)

        db.session.delete(mark)

        db.session.commit()

    @staticmethod
    def search_marks(search, page):

        query = Mark.query.join(Student).join(Subject)

        if search:
            query = query.filter(
                or_(
                    Student.roll_no.ilike(f"%{search}%"),
                    Student.first_name.ilike(f"%{search}%"),
                    Student.last_name.ilike(f"%{search}%"),
                    Subject.subject_name.ilike(f"%{search}%"),
                )
            )

        return query.order_by(Mark.id.desc()).paginate(
            page=page, per_page=10, error_out=False
        )
