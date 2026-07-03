from io import BytesIO

from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


class PDFService:
    @staticmethod
    def generate_student_report(report):

        buffer = BytesIO()

        doc = SimpleDocTemplate(buffer)

        styles = getSampleStyleSheet()

        elements = []

        elements.append(Paragraph("<b>Student Report Card</b>", styles["Title"]))

        elements.append(Spacer(1, 12))

        elements.append(
            Paragraph(
                f"Name: {report['student'].first_name} {report['student'].last_name}",
                styles["Normal"],
            )
        )

        elements.append(
            Paragraph(f"Roll No: {report['student'].roll_no}", styles["Normal"])
        )

        elements.append(Spacer(1, 12))

        data = [["Subject", "Marks"]]

        for mark in report["marks"]:
            data.append([mark.subject.subject_name, str(mark.marks)])

        table = Table(data)

        table.setStyle(
            TableStyle(
                [
                    ("BACKGROUND", (0, 0), (-1, 0), colors.grey),
                    ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                    ("GRID", (0, 0), (-1, -1), 1, colors.black),
                    ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
                ]
            )
        )

        elements.append(table)

        elements.append(Spacer(1, 20))

        elements.append(Paragraph(f"Total : {report['total']}", styles["Normal"]))

        elements.append(Paragraph(f"Average : {report['average']}%", styles["Normal"]))

        elements.append(Paragraph(f"Grade : {report['grade']}", styles["Normal"]))

        elements.append(Paragraph(f"Result : {report['result']}", styles["Normal"]))

        doc.build(elements)

        buffer.seek(0)

        return buffer
