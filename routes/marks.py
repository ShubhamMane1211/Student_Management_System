from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from forms.marks_form import MarksForm
from models.marks import Mark
from services.marks_service import MarksService

marks = Blueprint("marks", __name__, url_prefix="/marks")


@marks.route("/add", methods=["GET", "POST"])
@login_required
def add_marks():

    form = MarksForm()

    students = MarksService.get_students()
    subjects = MarksService.get_subjects()

    form.student.choices = [
        (s.id, f"{s.roll_no} - {s.first_name} {s.last_name}") for s in students
    ]

    form.subject.choices = [(s.id, s.subject_name) for s in subjects]

    if form.validate_on_submit():
        mark = MarksService.create_mark(form)

        if mark is None:
            flash("Marks for this student and subject already exist.", "danger")

            return render_template("marks/add_marks.html", form=form)

        flash("Marks added successfully!", "success")

        return redirect(url_for("marks.view_marks"))

    return render_template("marks/add_marks.html", form=form)


@marks.route("/")
@login_required
def view_marks():

    marks = Mark.query.all()

    return render_template("marks/marks.html", marks=marks)


@marks.route("/edit/<int:mark_id>", methods=["GET", "POST"])
@login_required
def edit_marks(mark_id):

    mark = MarksService.get_mark(mark_id)

    form = MarksForm(obj=mark)

    students = MarksService.get_students()
    subjects = MarksService.get_subjects()

    form.student.choices = [
        (s.id, f"{s.roll_no} - {s.first_name} {s.last_name}") for s in students
    ]

    form.subject.choices = [(s.id, s.subject_name) for s in subjects]

    if form.validate_on_submit():
        updated = MarksService.update_mark(mark, form)

        if updated is None:
            flash("Marks already exist for this student and subject.", "danger")
            return render_template("marks/edit_marks.html", form=form)

        flash("Marks updated successfully!", "success")

        return redirect(url_for("marks.view_marks"))

    return render_template("marks/edit_marks.html", form=form)


@marks.route("/delete/<int:mark_id>", methods=["POST"])
@login_required
def delete_marks(mark_id):

    MarksService.delete_mark(mark_id)

    flash("Marks deleted successfully!", "success")

    return redirect(url_for("marks.view_marks"))
