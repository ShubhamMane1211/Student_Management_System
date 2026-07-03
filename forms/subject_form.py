from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired


class SubjectForm(FlaskForm):
    subject_name = StringField("Subject Name", validators=[DataRequired()])

    subject_code = StringField("Subject Code", validators=[DataRequired()])

    submit = SubmitField("Save Subject")
