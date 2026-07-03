from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from forms.subject_form import SubjectForm
from services.subject_service import SubjectService

subject = Blueprint("subject", __name__, url_prefix="/subjects")


@subject.route("/")
@login_required
def subjects():

    subjects = SubjectService.get_all_subjects()

    return render_template("subject/subjects.html", subjects=subjects)


@subject.route("/add", methods=["GET", "POST"])
@login_required
def add_subject():

    form = SubjectForm()

    if form.validate_on_submit():
        subject = SubjectService.create_subject(form)

        if subject is None:
            flash("Subject Code already exists.", "danger")

            return render_template("subject/add_subject.html", form=form)

        flash("Subject Added Successfully!", "success")

        return redirect(url_for("subject.subjects"))

    return render_template("subject/add_subject.html", form=form)


@subject.route("/edit/<int:subject_id>", methods=["GET", "POST"])
@login_required
def edit_subject(subject_id):

    subject = SubjectService.get_subject(subject_id)

    form = SubjectForm(obj=subject)

    if form.validate_on_submit():
        updated = SubjectService.update_subject(subject, form)

        if updated is None:
            flash("Subject Code already exists.", "danger")

            return render_template("subject/edit_subject.html", form=form)

        flash("Subject Updated Successfully!", "success")

        return redirect(url_for("subject.subjects"))

    return render_template("subject/edit_subject.html", form=form)


@subject.route("/delete/<int:subject_id>", methods=["POST"])
@login_required
def delete_subject(subject_id):

    SubjectService.delete_subject(subject_id)

    flash("Subject Deleted Successfully!", "success")

    return redirect(url_for("subject.subjects"))
