from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required

from forms.student_form import StudentForm
from services.student_service import StudentService

student = Blueprint("student", __name__, url_prefix="/students")


@student.route("/")
@login_required
def students():

    search = request.args.get("search", "")

    students = StudentService.search_students(search)

    return render_template("student/students.html", students=students, search=search)
    return render_template("student/students.html", students=students)


@student.route("/add", methods=["GET", "POST"])
@login_required
def add_student():

    form = StudentForm()

    if form.validate_on_submit():
        student = StudentService.create_student(form)

        if student is None:
            flash("Roll Number already exists.", "danger")
            return render_template("student/add_student.html", form=form)

        flash("Student Added Successfully!", "success")

        return redirect(url_for("student.students"))

    return render_template("student/add_student.html", form=form)


@student.route("/edit/<int:student_id>", methods=["GET", "POST"])
@login_required
def edit_student(student_id):

    student = StudentService.get_student(student_id)

    form = StudentForm(obj=student)

    if form.validate_on_submit():
        updated_student = StudentService.update_student(student, form)

        if updated_student is None:
            flash("Roll Number Already exists.", "danger")
            return render_template("student/edit_student.html", form=form)

        flash("Student Updated Successfully!", "success")

        return redirect(url_for("student.students"))

    return render_template("student/edit_student.html", form=form)


@student.route("/delete/<int:student_id>", methods=["POST"])
@login_required
def delete_student(student_id):

    StudentService.delete_student(student_id)

    flash("Student Deleted Successfully!", "success")

    return redirect(url_for("student.students"))
