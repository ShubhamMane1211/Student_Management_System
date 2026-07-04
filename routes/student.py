import csv
from io import BytesIO

from flask import (
    Blueprint,
    Response,
    flash,
    redirect,
    render_template,
    request,
    send_file,
    url_for,
)
from flask_login import login_required
from openpyxl import Workbook

from forms.student_form import StudentForm
from models.student import Student
from services.student_service import StudentService

student = Blueprint("student", __name__, url_prefix="/students")


class Echo:
    def write(self, value):
        return value


@student.route("/")
@login_required
def students():

    page = request.args.get("page", 1, type=int)

    search = request.args.get("search", "")

    students = StudentService.search_students(search, page)

    return render_template("student/students.html", students=students, search=search)


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


@student.route("/export/excel")
@login_required
def export_students_excel():

    students = Student.query.order_by(Student.roll_no).all()

    workbook = Workbook()

    sheet = workbook.active

    sheet.title = "Students"

    sheet.append(
        ["Roll No", "First Name", "Last Name", "Class", "Division", "Email", "Phone"]
    )

    for student in students:
        sheet.append(
            [
                student.roll_no,
                student.first_name,
                student.last_name,
                student.class_name,
                student.division,
                student.email,
                student.phone,
            ]
        )

    output = BytesIO()

    workbook.save(output)

    output.seek(0)

    return send_file(
        output,
        download_name="students.xlsx",
        as_attachment=True,
        mimetype="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    )


@student.route("/export/csv")
@login_required
def export_students_csv():

    students = Student.query.order_by(Student.roll_no).all()

    def generate():

        data = csv.writer(Echo())

        yield data.writerow(
            [
                "Roll No",
                "First Name",
                "Last Name",
                "Class",
                "Division",
                "Email",
                "Phone",
            ]
        )

        for student in students:
            yield data.writerow(
                [
                    student.roll_no,
                    student.first_name,
                    student.last_name,
                    student.class_name,
                    student.division,
                    student.email,
                    student.phone,
                ]
            )

    return Response(
        generate(),
        mimetype="text/csv",
        headers={"Content-Disposition": "attachment; filename=students.csv"},
    )
