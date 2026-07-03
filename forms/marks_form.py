from flask_wtf import FlaskForm
from wtforms import FloatField, SelectField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class MarksForm(FlaskForm):
    student = SelectField("Student", coerce=int, validators=[DataRequired()])

    subject = SelectField("Subject", coerce=int, validators=[DataRequired()])

    marks = FloatField(
        "Marks", validators=[DataRequired(), NumberRange(min=0, max=100)]
    )

    submit = SubmitField("Save")
