from database.db import db
from datetime import datetime


class Student(db.Model):

    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)

    roll_no = db.Column(
        db.String(20),
        unique=True,
        nullable=False,
    )

    first_name = db.Column(db.String(100), nullable=False)

    last_name = db.Column(db.String(100), nullable=False)

    gender = db.Column(db.String(10))

    dob = db.Column(db.Date)

    phone = db.Column(db.String(15))

    email = db.Column(
        db.String(150),
        unique=True,
    )

    address = db.Column(db.Text)

    class_name = db.Column(db.String(20))

    division = db.Column(db.String(10))

    admission_date = db.Column(
        db.Date,
        default=datetime.utcnow,
    )

    photo = db.Column(db.String(255))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow,
    )

    marks = db.relationship(
        "Mark",
        backref="student",
        lazy=True,
        cascade="all, delete-orphan",
    )

    def __repr__(self):
        return f"<Student {self.roll_no}>"