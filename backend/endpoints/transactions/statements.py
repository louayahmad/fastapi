import io

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle


def create_bank_statement_pdf(account_holder, transactions):
    buffer = io.BytesIO()
    pdf = SimpleDocTemplate(buffer, pagesize=letter)

    elements = []

    title = f"Bank Statement for {account_holder}"
    elements.append(Paragraph(title, getSampleStyleSheet()["Heading1"]))
    elements.append(Spacer(1, 12))

    data = [["Date", "Description", "Amount", "Account Number"]]
    for transaction in transactions:
        data.append(list(transaction))

    table = Table(data)
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), colors.gray),
                ("TEXTCOLOR", (0, 0), (-1, 0), colors.whitesmoke),
                ("ALIGN", (0, 0), (-1, -1), "CENTER"),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("BOTTOMPADDING", (0, 0), (-1, 0), 12),
                ("BACKGROUND", (0, 1), (-1, -1), colors.beige),
            ]
        )
    )

    elements.append(table)

    pdf.build(elements)

    buffer.seek(0)

    return buffer.getvalue()
