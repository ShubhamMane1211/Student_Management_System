from sqlalchemy import or_

from database.db import db
from models.subject import Subject


class SubjectService:
    @staticmethod
    def get_all_subjects():

        return Subject.query.order_by(Subject.subject_name).all()

    @staticmethod
    def create_subject(form):

        existing = Subject.query.filter_by(subject_code=form.subject_code.data).first()

        if existing:
            return None

        subject = Subject(
            subject_name=form.subject_name.data, subject_code=form.subject_code.data
        )

        db.session.add(subject)
        db.session.commit()

        return subject

    @staticmethod
    def get_subject(subject_id):
        return Subject.query.get_or_404(subject_id)

    @staticmethod
    def update_subject(subject, form):

        existing = Subject.query.filter(
            Subject.subject_code == form.subject_code.data, Subject.id != subject.id
        ).first()

        if existing:
            return None

        subject.subject_name = form.subject_name.data
        subject.subject_code = form.subject_code.data

        db.session.commit()

        return subject

    @staticmethod
    def delete_subject(subject_id):

        subject = Subject.query.get_or_404(subject_id)

        db.session.delete(subject)

        db.session.commit()

    @staticmethod
    def search_subjects(search, page):

        query = Subject.query

        if search:
            query = query.filter(
                or_(
                    Subject.subject_name.ilike(f"%{search}%"),
                    Subject.subject_code.ilike(f"%{search}%"),
                )
            )

        return query.order_by(Subject.subject_name).paginate(
            page=page, per_page=10, error_out=False
        )
