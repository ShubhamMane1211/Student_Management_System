from database.db import db


class Mark(db.Model):

    __tablename__ = "marks"

    id = db.Column(db.Integer, primary_key=True)

    student_id = db.Column(
        db.Integer,
        db.ForeignKey("students.id"),
        nullable=False,
    )

    subject_id = db.Column(
        db.Integer,
        db.ForeignKey("subjects.id"),
        nullable=False,
    )

    marks = db.Column(db.Float,nullable=False)

    grade = db.Column(db.String(5))

    remarks = db.Column(db.String(255))

    def __repr__(self):
        return f"<Mark {self.id}>"