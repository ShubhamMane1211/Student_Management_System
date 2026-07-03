from flask_wtf import FlaskForm

from wtforms import (
    StringField,
    SelectField,
    DateField,
    SubmitField
)

from wtforms.validators import (
    DataRequired,
    Email,
    Length
)


class StudentForm(FlaskForm):

    roll_no = StringField(
        "Roll Number",
        validators=[DataRequired()]
    )

    first_name = StringField(
        "First Name",
        validators=[DataRequired()]
    )

    last_name = StringField(
        "Last Name",
        validators=[DataRequired()]
    )

    gender = SelectField(
        "Gender",
        choices=[
            ("Male", "Male"),
            ("Female", "Female"),
            ("Other", "Other")
        ]
    )

    dob = DateField(
        "Date of Birth"
    )

    phone = StringField(
        "Phone",
        validators=[Length(max=15)]
    )

    email = StringField(
        "Email",
        validators=[Email()]
    )

    address = StringField(
        "Address"
    )

    class_name = StringField(
        "Class"
    )

    division = StringField(
        "Division"
    )

    admission_date = DateField(
        "Admission Date"
    )

    submit = SubmitField("Save Student")