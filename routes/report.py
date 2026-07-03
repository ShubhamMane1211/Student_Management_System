from flask import Blueprint, render_template, send_file
from flask_login import login_required

from services.pdf_services import PDFService
from services.report_service import ReportService

report = Blueprint("report", __name__, url_prefix="/reports")


@report.route("/student/<int:student_id>")
@login_required
def student_report(student_id):

    report = ReportService.get_student_report(student_id)

    return render_template("reports/student_report.html", report=report)


@report.route("/student/<int:student_id>/pdf")
@login_required
def student_report_pdf(student_id):

    report_data = ReportService.get_student_report(student_id)

    pdf = PDFService.generate_student_report(report_data)

    student = report_data["student"]

    return send_file(
        pdf,
        download_name=f"{student.roll_no}_Report.pdf",
        as_attachment=True,
        mimetype="application/pdf",
    )
