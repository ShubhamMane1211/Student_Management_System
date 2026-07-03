from database.db import db


class Subject(db.Model):
    __tablename__ = "subjects"

    id = db.Column(db.Integer, primary_key=True)

    subject_name = db.Column(
        db.String(100),
        unique=True,
        nullable=False,
    )

    subject_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
    )

    marks = db.relationship(
        "Mark",
        backref="subject",
        cascade="all,delete-orphan",
    )

    def __repr__(self):
        return f"<Subject {self.subject_name}>"
