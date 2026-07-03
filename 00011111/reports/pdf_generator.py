from reportlab.platypus import SimpleDocTemplate, Table


def generate_pdf(data, filename="report.pdf"):
    doc = SimpleDocTemplate(filename)

    table = Table(data)

    elements = [table]
    doc.build(elements)
